### Step 1: The Documentation

Navigate to your new directory (`cd ~/Desktop/projects/DevSecOps-Secure-Transfer`) and create the `README.md` file. Here is the professional, portfolio-ready template for your exfiltration tool:

# 🔐 Automated SCP Secure Backup & Exfiltration Utility

## 📖 Overview
The **Automated SCP Utility** is a concurrent, multi-threaded DevSecOps tool designed for the secure extraction and backup of remote files over encrypted SSH tunnels. Built to operate without interactive prompts, it is ideal for automated server backups, remote log retrieval, and authorized red team exfiltration.

This project demonstrates advanced Python network programming, including dynamic DNS resolution, concurrent thread management, and encrypted transport layer manipulation using the `paramiko` and `scp` libraries.

## ✨ Core Features
* **Multi-Threaded Extraction:** Utilizes a custom threading architecture to pull files from dozens of remote servers simultaneously without locking.
* **Dynamic Authentication:** Intelligently handles both SSH Private Keys and standard password authentication on the fly.
* **Smart File Naming:** Automatically sanitizes remote target IPs/Hostnames and dynamically renames local loot files to prevent overwriting (e.g., `192_168_1_50_backup.log`).
* **Pre-Flight DNS Checks:** Resolves hostnames prior to connection attempts, gracefully skipping dead hosts or bad DNS entries without crashing the thread pool.

## 🛠️ Prerequisites
This tool requires Python 3.x and the following external libraries:

```bash
pip install paramiko scp

```

## 🚀 Usage

**Single Target (Password Authentication):**

```bash
python3 auto_backup.py -t 192.168.1.50 -u root -p "SuperSecret123" -r /var/log/auth.log

```

**Multiple Targets (SSH Key Authentication):**

```bash
python3 auto_backup.py -t "192.168.1.50, web-server-01.local" -u admin -k ~/.ssh/id_rsa -r /etc/passwd

```

**Bulk Extraction from a File (Custom Thread Count):**

```bash
python3 auto_backup.py -t targets.txt -u root -k ~/.ssh/id_rsa -r /etc/shadow -th 15

```

## 🔒 Security Disclaimer

This tool is intended for authorized systems administration, DevSecOps backups, and sanctioned penetration testing only. Ensure you have explicit, written permission before authenticating to or extracting data from any remote infrastructure.

