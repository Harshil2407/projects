### README.md

# DevSecOps Network Automation Toolkit

## Overview
This repository contains a suite of Python-based network automation and reconnaissance tools designed for DevSecOps environments. These utilities facilitate infrastructure auditing, automated host discovery, and secure remote server management, bridging the gap between network visibility and automated compliance checking.

## Included Tools

### 1. Auto-Recon & Compliance Auditor (`auto_recon.py`)
A high-performance, multi-threaded network scanner and auditing engine. It leverages a flattened tuple-queue threading architecture to rapidly scan thousands of ports across multiple subnets without risking CPU or memory exhaustion.

**Core Capabilities:**
* **TCP Host Discovery:** Probes common administrative ports to verify host availability, bypassing standard ICMP blocking.
* **Dynamic Banner Triggering:** Interrogates open sockets to extract service versions. Defeats non-standard port obfuscation by triggering automated audits based on service signatures.
* **Paramiko SSH Integration:** Securely authenticates via SSH Keys or Passwords to audit server hardening parameters (e.g., Root Login status, OS Version tracking) immediately upon service discovery.

**Usage Example:**
```bash
python3 auto_recon.py -t 192.168.1.0/24 -p nmap -w 50 --user admin --key ~/.ssh/id_rsa

```

### 2. TCP Interrogator (`tcp_interrogator.py`)

A lightweight, targeted socket programming utility designed for precise, single-host port analysis and manual banner extraction. It serves as a surgical tool for validating specific service configurations without the overhead of a multi-threaded engine.

**Usage Example:**

```bash
python3 tcp_interrogator.py <target_ip> <port>

```

## Prerequisites

Both tools rely heavily on the Python Standard Library but require `paramiko` for the automated SSH auditing module.

* Python 3.x
* Paramiko (`pip install paramiko`)

## Output Format

`auto_recon.py` compiles all findings into a structured JSON dictionary (`output.json`), mapping IPs to open ports, their respective service banners, and any successful compliance audit data, ensuring seamless integration into downstream automated security pipelines.

## Disclaimer

These utilities are designed strictly for educational purposes and authorized infrastructure auditing. Do not utilize this software against networks or systems for which you do not have explicit, written permission to test.

