# AWS Security Group Auditor

A beginner-friendly Python automation project that audits AWS Security Groups and identifies potentially insecure firewall rules.

The script checks whether **SSH (22)** or **RDP (3389)** ports are publicly accessible (`0.0.0.0/0`) and reports them as security risks.

---

## Features

- Connects to AWS using **Boto3**
- Retrieves Security Groups
- Detects publicly exposed SSH (22) and RDP (3389) ports
- Displays security findings in the terminal
- Saves the complete AWS response to `response.json`
- Supports LocalStack for local AWS testing

---

## Technologies Used

- Python 3
- Boto3
- AWS EC2 API
- LocalStack
- JSON
- Logging

---

## Prerequisites

Install the required package:

```bash
pip install boto3
```

Start LocalStack (or configure your AWS credentials if using a real AWS account).

---

## Usage

Run the script:

```bash
python security_audit.py
```

---

## Example Output

```text
default              | 22     | 🚨 EXPOSED TO WORLD
web-server           | 3389   | 🚨 EXPOSED TO WORLD
```

---

## Project Structure

```
.
├── security_audit.py
├── response.json
└── README.md
```

---

## Learning Objectives

This project was built to practice:

- Python automation
- Working with the AWS SDK (Boto3)
- AWS Security Groups
- Cloud security auditing
- Parsing JSON responses
- Using Python logging

---


