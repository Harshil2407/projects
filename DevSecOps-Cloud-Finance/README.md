# AWS Resource Cleanup Auditor

A beginner-friendly Python automation project that scans AWS resources for unused infrastructure that may lead to unnecessary cloud costs.

The script identifies unused **Elastic IPs (EIPs)** and unattached **EBS Volumes**, then generates a cleanup report in JSON format.

---

## Features

- Connects to AWS using **Boto3**
- Detects unused Elastic IP addresses
- Detects unattached EBS volumes
- Generates a cleanup report (`cleanup_report.json`)
- Displays audit results using structured logging
- Supports LocalStack for safe local testing

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

Install the required dependency:

```bash
pip install boto3
```

Start LocalStack (or configure your AWS credentials if using a real AWS account).

---

## Usage

Run the auditor:

```bash
python cleanup_auditor.py
```

---

## Example Output

```text
2026-07-02 14:20:31 - INFO - Scanning for unused Elastic IPs...
2026-07-02 14:20:31 - WARNING - Found unused EIP: 54.12.34.56

2026-07-02 14:20:31 - INFO - Scanning for unattached EBS volumes...
2026-07-02 14:20:31 - WARNING - Found unattached Volume: vol-1234567890abcdef0 (20 GiB)

2026-07-02 14:20:31 - INFO - Audit complete. Summary: 1 EIPs, 1 Volumes.
```

---

## Generated Report

After execution, the script creates a JSON report:

```
cleanup_report.json
```

Example:

```json
{
    "unused_eips": [
        "54.12.34.56"
    ],
    "unattached_volumes": [
        {
            "VolumeId": "vol-1234567890abcdef0",
            "Size": 20
        }
    ]
}
```

---

## Project Structure

```text
.
├── cleanup_auditor.py
├── cleanup_report.json
└── README.md
```

---

## Learning Objectives

This project was built to practice:

- Python automation
- Working with the AWS SDK (Boto3)
- AWS EC2 resource management
- Cloud cost optimization
- JSON report generation
- Logging and exception handling

---

