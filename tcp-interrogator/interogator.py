import sys
import socket
import logging
import argparse

logging.basicConfig(
            level = logging.INFO,
            format = "%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def tcp_interogator(target,port):
    logger.info("attempt to try interogatting")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(4)
            s.connect((target,int(port)))
        
            logger.info(f"port {port} is open on the host {target}.")

    except ConnectionRefusedError:
        logger.info(f"port {port} is not open on the host {target} .")

    except socket.timeout:
        logger.error(f"either port:{port} is filtered or host:{target} is down")
    except Exception as e:
        logger.exception(f"[exception] : we got an exception {e} while connecting to the port:{port} in the host:{target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "it is the tcp interogator ")
    parser.add_argument("-t" , "--target" , help = "use -t or --target for inputing the target")
    parser.add_argument("-p", "--port", help = "use -p or --port for giveing the target port")

    args = parser.parse_args()

    tcp_interogator(args.target, args.port)

