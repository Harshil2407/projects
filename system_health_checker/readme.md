#  FleetSec System Auditor

An automated, configuration-driven system health monitor built for DevSecOps environments. This tool actively tracks live CPU and RAM usage against strict thresholds defined in a YAML configuration file, logging system states to prevent resource exhaustion.

## Table of Contents
- [Project Architecture](#-project-architecture)
- [Architectural Differences: psutil vs Native](#-architectural-differences)
- [Installation & Requirements](#-installation--requirements)
- [Usage](#-usage)

## Project Architecture

```text
system_health_checker/
│
├── using_psutil.py       # Primary cross-platform health auditor
├── native_checker.py     # OS-native health monitor (no external libs)
├── mod_2.yaml            # Threshold configuration ruleset
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```

## Architectural Differences

This repository contains two distinct approaches to system monitoring to demonstrate different DevSecOps methodologies:

| Feature | `using_psutil.py` (Library-Driven) | `native_checker.py` (OS-Native) |
| --- | --- | --- |
| **Dependencies** | Requires `psutil` library via pip. | **Zero dependencies** (Uses Python Standard Library). |
| **Portability** | 100% Cross-Platform (Linux, Windows, macOS). | Highly OS-dependent (usually relies on Linux `/proc/`). |
| **Execution Method** | Direct API calls to the kernel via C-extensions. | Uses `subprocess` to parse shell commands (`free`, `top`). |
| **Best Use Case** | Enterprise environments requiring reliable, cross-platform scaling. | Highly restricted environments (air-gapped/no pip access). |

## Installation & Requirements

To run the primary `psutil` auditor, you need Python 3.x and the following external libraries:

> **Dependencies:**
> * `psutil` - For cross-platform hardware monitoring.
> * `PyYAML` - For parsing the configuration ruleset.
> 
> 

**1. Clone the repository:**

```bash
git clone [https://github.com/yourusername/system_health_checker.git](https://github.com/yourusername/system_health_checker.git)
cd system_health_checker

```

**2. Install requirements:**
If you are using the `psutil` version, you can quickly install the dependencies:

```bash
pip install psutil PyYAML

```

*(Note: If you are running `native_checker.py`, no installation is required).*

## Usage

The auditor is designed to be run via the CLI. It dynamically reads memory and CPU limits from the provided YAML file.

**Basic Execution (Defaults to `mod_2.yaml`):**

```bash
python3 using_psutil.py

```

**Custom Configuration:**
Pass a specific YAML ruleset using the `-y` or `--yaml` flag:

```bash
py``thon3 using_psutil.py -y custom_rules.yaml

```

**Example Output:**

```text
2026-06-20 19:25:10 - INFO - [info] : both cpu and memory usage are in the limits and better state
2026-06-20 19:26:45 - WARNING - [warning] : there is no problem yet but keep a close eye.
2026-06-20 19:27:12 - CRITICAL - [critical] system is in danger as cpu usage and ram usage both have hit the limit.

```

```

```
