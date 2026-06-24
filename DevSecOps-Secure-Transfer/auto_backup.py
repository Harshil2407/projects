import argparse
import paramiko
from scp import SCPClient
import logging
from pathlib import Path
import queue
import threading
import socket  

q = queue.Queue()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_targets(target_input):
    """Parses terminal input and returns a clean list of target IPs or Hostnames."""
    target_list = []
    target_path = Path(target_input)
    
    if target_path.is_file():
        with open(target_path, "r") as f:
            for line in f:
                clean_target = line.strip()
                if clean_target:
                    target_list.append(clean_target)
    else:
        for item in target_input.split(","):
            target_list.append(item.strip())

    return target_list
    
def backup_file(target_host, username, key_file, password, remote_file):
    """Resolves DNS, establishes an SSH tunnel, and executes the SCP transfer."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        logger.info(f"[*] Resolving target: {target_host}...")
        target_ip = socket.gethostbyname(target_host)
        
        logger.info(f"[*] Establishing tunnel to {target_ip} ({target_host})...")
        
        if key_file:
            ssh.connect(target_ip, username=username, key_filename=key_file, timeout=5)
        elif password:
            ssh.connect(target_ip, username=username, password=password, timeout=5)

        # Build the dynamic file name
        safe_name = target_host.replace('.', '_')
        file_ext = Path(remote_file).suffix
        local_name = f"{safe_name}_backup{file_ext}"

        with SCPClient(ssh.get_transport()) as scp:
            logger.info(f"[*] Downloading {remote_file} from {target_host}...")
            scp.get(remote_file, local_path=local_name)
            logger.info(f"[+] SUCCESS: Saved as {local_name}")

    except socket.gaierror:
        logger.error(f"[-] DNS Resolution Failed: Cannot find IP for '{target_host}'")
    except paramiko.AuthenticationException:
        logger.error(f"[-] Authentication failed for {target_host}. Bad password or key.")
    except Exception as e:
        logger.error(f"[-] Transfer failed for {target_host}: {e}")
    finally:
        ssh.close()

def worker(args):
    while True:
        target = q.get()
        backup_file(target, args.user, args.key, args.password, args.rfile)
        q.task_done()

def main():
    parser = argparse.ArgumentParser(description="Multi-Threaded DevSecOps SCP Backup Utility")
    parser.add_argument("-t", "--target", required=True, help="Single target, comma-separated, or file")
    parser.add_argument("-u", "--user", default="root", help="SSH Username (default: root)")
    
    parser.add_argument("-k", "--key", help="Path to the SSH private key")
    parser.add_argument("-p", "--password", help="SSH Password for authentication")
    
    parser.add_argument("-r", "--rfile", required=True, help="Exact path of the remote file to backup")
    parser.add_argument("-th", "--threads", type=int, default=5, help="Number of concurrent threads")

    args = parser.parse_args()

    if not args.key and not args.password:
        logger.error("FATAL: You must provide either a private key (-k) or a password (-p).")
        return

    targets = parse_targets(args.target)
    if not targets:
        logger.error("No valid targets found.")
        return

    logger.info(f"Loaded {len(targets)} targets. Starting thread pool...")

    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(args,), daemon=True)
        t.start()

    for target in targets:
        q.put(target)

    q.join()
    logger.info("[+] All backup operations completed cleanly.")

if __name__ == "__main__":
    main()
