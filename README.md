# Server System Validator

A Python-based server validation tool that checks simulated server hardware data and reports whether system components meet expected health and configuration requirements.

I built this project to learn more about server system validation, hardware monitoring, automated testing, and technologies such as BMC and Redfish.

## Features

The validator currently checks:

- Overall system health
- Processor count and health
- Installed memory and health
- CPU temperature thresholds
- Fan speed and health
- Power supply health

Each validation test reports a `PASS` or `FAIL`, followed by an overall validation summary.

## Example Output

```text
========================================
SERVER VALIDATION REPORT
========================================
[PASS] System health: OK
[PASS] Processors: 2 detected, health OK
[PASS] Memory: 256 GB detected, health OK
[PASS] CPU temperature: 62 C (limit: 85 C)
[PASS] Fan1: 8200 RPM, health OK
[PASS] Fan2: 7900 RPM, health OK
[FAIL] Fan3: 0 RPM, health Critical
[PASS] PSU1: health OK
[PASS] PSU2: health OK

========================================
VALIDATION SUMMARY
========================================
Test groups passed: 5
Test groups failed: 1
Overall result: FAIL
```

## Test Scenarios

The project includes JSON files representing different server states.

### Healthy Server

All monitored components are operating within their expected conditions. The validator should report an overall `PASS`.

### Failed Server

One or more components contain intentionally simulated failures, such as a fan reporting 0 RPM and a critical health status. The validator should detect the problem and report an overall `FAIL`.

These scenarios make it possible to verify that the validation logic correctly detects both normal and abnormal system conditions.

## How It Works

The current version reads server information from local JSON files:

```text
Simulated Server Data
        |
        v
    JSON File
        |
        v
 Python Validator
        |
        v
Validation Checks
        |
        v
  PASS / FAIL Report
```

The JSON data simulates hardware-management information that could be obtained from a server management interface.

In a production environment, similar information could be retrieved from a server's Baseboard Management Controller (BMC) using a management interface such as Redfish.

Redfish provides RESTful APIs that allow management software to retrieve server information using HTTP and JSON. A future version of this project could replace the local JSON input with data retrieved directly from a Redfish API.

## Project Structure

```text
supermicro-system-validator/
├── validator.py
├── healthy_server.json
├── failed_server.json
└── README.md
```

- `validator.py` - Performs the server validation checks and generates results
- `healthy_server.json` - Simulates a healthy server configuration
- `failed_server.json` - Simulates a server containing hardware failures
- `README.md` - Project documentation

## Running the Validator

Make sure Python 3 is installed.

Run the validator by providing a server data JSON file as a command-line argument.

To validate the healthy server scenario:

```bash
py validator.py healthy_server.json
```

To validate the failed server scenario:

```bash
py validator.py failed_server.json
```

The program loads the selected server data, performs each validation check, and displays individual `PASS` or `FAIL` results followed by an overall validation summary.

## Validation Approach

The project follows a basic system-validation workflow:

1. Collect system information.
2. Compare actual values against expected values or thresholds.
3. Report individual component results.
4. Identify failed subsystems.
5. Produce an overall validation result.

A detected failure would then be investigated further using hardware inspection, system logs, BMC event logs, component isolation, and repeated testing to determine the root cause.

## Technologies

- Python
- JSON
- Server hardware validation concepts
- BMC / out-of-band management concepts
- Redfish concepts

## Future Improvements

- Retrieve live server information through the Redfish API
- Add command-line selection of test scenarios
- Save validation results to report files
- Add additional storage and network validation
- Add automated test cases
- Improve error handling for missing or malformed server data
