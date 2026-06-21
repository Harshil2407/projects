import argparse
import threading
import queue
import socket
import logging
import json
import ipaddress
import paramiko
from ports import nmap_top_1000

logging.basicConfig(
            level = logging.INFO,
            format = "%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

q = queue.Queue()
alive_host_details = {}

discovery_ports = [22, 80, 443, 445, 3389]

def parse_targets(target_input):
    target_list = []
    for item in target_input.split(','):
        item = item.strip()
        try:
            if "-" in item:
                start_str,end_str = item.split('-')
                start_ip = int(ipaddress.IPv4Address(start_str.strip()))
                end_ip = int(ipaddress.IPv4Address(end_str.strip()))

                for ip_int in range(start_ip, end_ip + 1):
                    target_list.append(str(ipaddress.IPv4Address(ip_int)))
            else:
                netwrok = ipaddress.ip_network(item, strict= False)
                if netwrok.prefixlen == 32:
                    target_list.append(str(item))
                else:
                    for ip in netwrok.hosts():
                        target_list.append(str(ip))

        except Exception as e:
            logger.error(f"ivalid input format: {e}")

    return list(set(target_list))


def host_alive(target):
    for ports in discovery_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(4)
                s.connect((target, int(ports)))
                logger.info("host is alive")
                return True
        except ConnectionRefusedError:
            return True

        except socket.timeout:
            continue

        except Exception as e:
            logger.error(f"got an error {e} while trying to connect to the target {target}")
            continue
    logger.error(f"Phase 1 Failed: {target} appears to be DOWN or completely filtered.")
    return False

def ssh_audit(host, port, username, password=None, key_file=None):
    if not password and not key_file:
        return "Audit Skipped: No credentials provided in terminal."

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if key_file:
            key = paramiko.RSAKey.from_private_key_file(key_file)
            ssh.connect(hostname=host, port=port,username= username, pkey=key, timeout=4)
        else:
            ssh.connect(hostname= host,port= port, username= username, passphrase= password, timeout= 4)

        
        audit_results = {}

        stdin, stdout,stderr = ssh.exec_command("grep 'PermitRootLogin' /etc/ssh/sshd_config")
        root_login = stdout.read().decode('utf-8').strip()
        audit_results['root_login_status'] = root_login if root_login else "not explicitly defined"

        stdin, stdout, stderr = ssh.exec_command("cat /etc/os-release | grep PRETTY_NAME")
        os_version = stdout.read().decode('utf-8').strip().replace('PRETTY_NAME=' , '').replace('"', '')
        audit_results['os_version'] = os_version 

        ssh.close()
        return audit_results

    except paramiko.AuthenticationException :
        return f"Authentication calnceled ,bad credentials "

    except Exception as e:
        return f"audit failed {str(e)}"





def check_open_ports(host, port, args):
            banner = "Service Identified, No Banner"
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
                    so.settimeout(2)
                    res = so.connect_ex((host, port))

                    if res == 0:
                        if port in [80, 443, 8080]:
                            try:
                                so.send(b"HEAD / HTTP/1.0\r\n\r\n")
                            except:
                                pass
                        try:

                            raw_banner = so.recv(1024).decode('utf-8', errors='ignore').strip()
                            if raw_banner:
                                banner = raw_banner.split('\n')[0]
                        except socket.timeout:
                            banner = "Timeout waiting for banner"
            
                        alive_host_details[host][str(port)] = banner
                        logger.info(f"    -> Port {port} OPEN ({banner})")

                        if "SSH" in banner.upper():
                            logger.info(f"found the ssh service on {host}:{port}")
                            audit_data = ssh_audit(host,port,args.username, args.password, args.key_file)
                            alive_host_details[host]["SSH_Compliance_Audit"] = audit_data
                            logger.info(f"    -> {audit_data}")

            except Exception:
                pass


def worker(args):
    """This is the function each thread will run continuously."""
    while True:
        target_ip, target_port = q.get()
        check_open_ports(target_ip, target_port,args)  
        q.task_done()

def add_result():
    with open("output.json", "w") as out:
        json.dump(alive_host_details ,out,indent=4, sort_keys=True)
    logger.info("added the output in the output.json file")



def main():
    parser = argparse.ArgumentParser(description= "it is the devsecops project for leaning the netwoking in the python")
    parser.add_argument("-t" , "--target", help = "to add the host use the -t ot --target")
    parser.add_argument("-p", "--ports", default="common", help="Port range: 'common', '1000', or 'all'")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Number of concurrent threads")
    parser.add_argument("--user", default="root", help="SSH Username for Phase 4 Audit")
    parser.add_argument("--password", help="SSH Password")
    parser.add_argument("--key", help="Path to SSH Private Key")

    args = parser.parse_args()
    targets = parse_targets(args.target)

    ports_to_scan = []
    if args.ports == "common":
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 3306, 3389, 8080]
    elif args.ports == "1000":
        ports_to_scan = nmap_top_1000
    elif args.ports == "all":
        ports_to_scan = range(1, 65536)

    logger.info("starting the recon")


    for _ in range(args.workers):
        t = threading.Thread(target=worker, args= (args,), daemon=True)
        t.start()

    for t in targets:
        if host_alive(t):
            logger.info(f"[+] {t} is ALIVE. Loading queue...")
            if t not in alive_host_details:
                alive_host_details[t] = {}
                
            # Create a ticket for every single port and push it
            for p in ports_to_scan:
                q.put((t, p))
        else:
            logger.error(f"[-] {t} is DOWN. Skipping.")

    q.join()

    if alive_host_details:
        add_result()
    else:
        logger.info("No alive hosts found to save.")

if __name__ == "__main__" :
    main()
