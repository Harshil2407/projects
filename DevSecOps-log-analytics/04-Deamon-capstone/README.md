# Real-Time Log Analytics & Security Monitoring Daemon

A lightweight, multi-threaded **Python security monitoring daemon** that continuously watches one or more web server log files, detects suspicious activity in real time, and sends instant Slack alerts.

This project demonstrates practical DevSecOps concepts including log monitoring, concurrent programming, attack detection, rate limiting, and webhook integrations.

---

# Features

- Real-time log monitoring
- Multi-threaded architecture
- Producer–Consumer design pattern
- Thread-safe Queue communication
- Concurrent monitoring of multiple log files
- Path Traversal attack detection
- Brute Force attack detection
- Alert rate limiting
- Slack Webhook integration
- Configurable through environment variables
- Lightweight and easy to deploy

---

# Supported Attack Detection

## Path Traversal

Detects attempts to access sensitive system files such as:

```
../../etc/passwd
../../../etc/shadow
```

or requests containing

```
../
/etc/
```

---

## Brute Force Detection

Tracks repeated failed authentication attempts from the same IP address.

Current threshold:

- More than **3 failed requests**
- HTTP Status Codes:
  - 401
  - 402

After exceeding the threshold, an alert is generated.

---

# Architecture

The daemon follows a **Producer–Consumer** architecture.

```
                 Access Log
                      │
                      ▼
             File Monitoring Threads
                      │
                      ▼
               Thread-safe Queue
                      │
                      ▼
             Alert Processing Thread
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Path Traversal Detection    Brute Force Detection
        │                           │
        └─────────────┬─────────────┘
                      ▼
              Rate Limiting Check
                      ▼
                Slack Webhook Alert
```

---

# Technologies Used

- Python 3
- threading
- queue
- pathlib
- argparse
- logging
- requests
- JSON
- Regular Expressions (Regex)

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/log-analytics-daemon.git

cd log-analytics-daemon
```

Install dependencies

```bash
pip install requests
```

---

# Configuration

The Slack Webhook URL is loaded securely from an environment variable.

Linux/macOS

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXXXXX"
```

Windows (PowerShell)

```powershell
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXXXXX"
```

---

# Usage

Monitor a single log file

```bash
python daemon.py -f access.log
```

Monitor multiple log files

```bash
python daemon.py -f access.log,auth.log,error.log
```

---

# Command Line Arguments

| Argument | Description |
|----------|-------------|
| `-f` | Comma-separated list of log files to monitor |

Example

```bash
python daemon.py -f nginx.log,apache.log
```

---

# Example Log Entry

The daemon expects log entries similar to:

```text
192.168.1.25 - - [08/Jul/2025:12:40:15 +0000] "GET /index.html HTTP/1.1" 200 612

192.168.1.25 - - [08/Jul/2025:12:41:01 +0000] "GET ../../etc/passwd HTTP/1.1" 401 128
```

---

# Example Slack Alert

```
🚨 SECURITY ALERT 🚨

Possible Brute Force!

IP:
192.168.1.25

Failed Attempts:
4
```

---

# How It Works

1. The daemon starts one monitoring thread for each log file.
2. Each monitoring thread tails the file continuously.
3. Every new log entry is parsed using Regular Expressions.
4. Parsed events are pushed into a thread-safe Queue.
5. A consumer thread analyzes each event.
6. If suspicious activity is detected:
   - Path Traversal
   - Brute Force
7. Rate limiting is checked.
8. A Slack notification is sent if allowed.

---

# Project Structure

```
.
├── daemon.py
├── README.md
├── state.json
└── requirements.txt
```

---

# Rate Limiting

To avoid alert spam, every IP address is placed under a cooldown period after an alert is generated.

Current cooldown:

```
300 seconds
```

This information is stored inside

```
state.json
```

---

# Security Best Practices

This project follows several DevSecOps best practices.

- Uses environment variables for secrets
- Does not hardcode webhook URLs
- Thread-safe communication
- Structured logging
- Alert rate limiting
- Minimal external dependencies

---

# Current Limitations

- IPv4 only
- Supports Common Log Format
- Uses local JSON storage instead of a database
- Brute force detection is based only on HTTP status codes
- Slack is currently the only supported alert destination

---

# Future Improvements

- Email alerts
- Microsoft Teams integration
- Discord integration
- Elasticsearch support
- Prometheus metrics
- Grafana dashboards
- Docker support
- YAML configuration
- Unit tests
- SQLite/PostgreSQL event storage
- GeoIP lookup
- Automatic IP blocking
- Support for IPv6
- Machine Learning anomaly detection

---


