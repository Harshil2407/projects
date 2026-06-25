# Project 1: Regex Log Parser

## 🕵️‍♂️ What does it do?
The Regex Log Parser is a memory-efficient data extraction tool. It ingests massive, unstructured server logs (like Apache or Nginx access logs) and transforms them into clean, structured JSON data.

Instead of relying on fragile string splitting, it uses **Regular Expressions (Regex)** to surgically extract:
* The Source **IP Address**
* The **HTTP Method** (GET, POST, etc.)
* The Target **Endpoint**
* The **HTTP Status Code**

**Enterprise Feature:** This script utilizes Python generators (`yield`). It streams the log file line-by-line, meaning it can parse a 50GB log file while using almost zero RAM.

## ⚙️ Requirements & Installation
* **Python 3.x**
* **No external dependencies!** Built entirely with Python's standard library (`re`, `json`, `logging`, `argparse`, `pathlib`). No `pip install` is required.
* **Prerequisite Data:** You need a raw log file to parse (e.g., `access.log`).

## 🚀 How to Run
1. Navigate to the `01-Regex-Parser` directory.
2. Ensure you have a target log file ready.
3. Run the script via the terminal using the required `-f` flag:

`python3 log_parser.py -f access.log`

## 📊 Expected Output
The script will output progress to the terminal:

`2026-06-26 00:15:22,123 - INFO - Successfully saved parsed logs to result.json`

It will generate a `result.json` file in the same directory, beautifully grouping all requests by their source IP address:

{
    "10.0.0.15": [
        {
            "method": "POST",
            "endpoint": "/api/auth",
            "status_code": 401
        }
    ],
    "172.16.0.5": [
        {
            "method": "GET",
            "endpoint": "/etc/passwd",
            "status_code": 403
        }
    ]
}
