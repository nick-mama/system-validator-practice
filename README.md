# Server System Validator

A Python-based server validation tool that performs automated health and configuration checks on server hardware data.

The project includes two validation approaches:

1. **Local JSON validation** using simulated healthy and failed server scenarios.
2. **Redfish API validation** using the DMTF Redfish Mockup Server and live HTTP requests.

I built this project to gain hands-on experience with server system validation, hardware monitoring, automated testing, BMC concepts, Redfish APIs, and troubleshooting.

## Features

The validator checks server components including:

- Overall system health and power state
- Processor count, core count, and health
- Installed memory and health
- CPU temperature thresholds in local test scenarios
- Fan speed, health, and state
- Power supply health and state

Each validation test reports a `PASS`, `FAIL`, or informational status and produces an overall validation result.

## Redfish Validation

`redfish_validator.py` communicates with a locally running DMTF Redfish Mockup Server using HTTP requests.

Rather than reading hardware information directly from a file, the validator retrieves Redfish resources and follows their `@odata.id` links to discover related server components.

```text
DMTF Redfish Mock Server
          |
          | HTTP GET
          v
     ComputerSystem
          |
          v
        Chassis
       /       \
      v         v
ThermalSubsystem   PowerSubsystem
      |                 |
      v                 v
     Fans          Power Supplies
       \               /
        \             /
         v           v
        Python Validation
               |
               v
          PASS / FAIL
```

The mock server simulates a Redfish-capable BMC/server. It runs locally for development purposes and does not represent the physical hardware of the computer running the validator.

## Redfish Resource Discovery

The validator begins with a Redfish `ComputerSystem` resource and follows links returned by the API.

For example:

```text
/redfish/v1/Systems/437XR1138R2
              |
              v
           Chassis
              |
       +------+------+
       |             |
       v             v
ThermalSubsystem  PowerSubsystem
       |             |
       v             v
      Fans       PowerSupplies
```

The script uses `@odata.id` values returned by Redfish instead of hardcoding every component endpoint.

Each component is retrieved using an HTTP `GET` request and the returned JSON data is evaluated against validation criteria.

## Example Redfish Output

```text
=============================================
REDFISH SERVER VALIDATION REPORT
=============================================
[PASS] System: health OK, power state On
[PASS] Processors: 2 CPUs, 8 cores, health OK
[PASS] Memory: 96 GiB, health OK, state Enabled
[PASS] Fan Bay 1: 45% (2200 RPM), health OK, state Enabled
[PASS] Fan Bay 2: 45% (2400 RPM), health OK, state Enabled
[PASS] Fan for CPU 1: 45%, health OK, state Enabled
[PASS] Fan for CPU 2: 45% (1490 RPM), health OK, state Enabled
[FAIL] Power Supply Bay 1: health Warning, state Enabled, input Normal
[INFO] Power Supply Bay 2: not installed

=============================================
VALIDATION SUMMARY
=============================================
System: PASS
Processors: PASS
Memory: PASS
Fans: PASS
Power Supplies: FAIL

Overall result: FAIL
```

This example demonstrates that the validator can identify an abnormal hardware status while continuing to evaluate the remaining components.

## Local JSON Test Scenarios

The project also includes two local JSON scenarios for testing validation logic without a running Redfish service.

### Healthy Server

`healthy_server.json` represents a server whose monitored components meet the expected configuration and health requirements.

The expected overall result is `PASS`.

### Failed Server

`failed_server.json` contains intentionally simulated hardware problems, such as a fan reporting 0 RPM and a critical health status.

The expected overall result is `FAIL`.

These scenarios provide a simple way to verify that the validation logic correctly distinguishes normal and abnormal system conditions.

## Project Structure

```text
server-system-validator/
├── validator.py
├── redfish_validator.py
├── healthy_server.json
├── failed_server.json
└── README.md
```

- `validator.py` - Validates local JSON server scenarios
- `redfish_validator.py` - Retrieves and validates server information through Redfish
- `healthy_server.json` - Simulated healthy server configuration
- `failed_server.json` - Simulated server configuration containing failures
- `README.md` - Project documentation

## Running the Local Validator

Make sure Python 3 is installed.

To validate the healthy scenario:

```bash
py validator.py healthy_server.json
```

To validate the failed scenario:

```bash
py validator.py failed_server.json
```

## Running the Redfish Validator

The Redfish validator requires the Python `requests` package and a running Redfish service.

This project was tested using the DMTF Redfish Mockup Server running locally at:

```text
http://127.0.0.1:8000
```

With the mock server running:

```bash
py redfish_validator.py
```

The validator sends HTTP requests to the Redfish service, parses the returned JSON, discovers related hardware resources, and performs validation checks.

## Error Handling and Troubleshooting

While developing the Redfish validator, different hardware resources exposed different sets of properties.

For example, some fan resources provided both speed percentage and RPM while others only provided a percentage reading. The validator handles RPM as an optional property rather than assuming it is always present.

The mock server also contained an unoccupied power supply bay whose state was reported as `Absent`. The validator handles this state separately instead of attempting to access health information that is not provided for an absent device.

These cases demonstrate the importance of inspecting actual API responses and accounting for differences between component states when building validation automation.

## Validation Approach

The project follows a basic system-validation workflow:

1. Collect system and component information.
2. Compare actual values against expected states or thresholds.
3. Report individual component results.
4. Identify failed or abnormal subsystems.
5. Continue testing other components when possible.
6. Produce an overall validation result.

A detected failure could then be investigated further using system logs, BMC event logs, hardware inspection, component isolation, and repeated testing to determine the root cause.

## Technologies and Concepts

- Python
- JSON
- HTTP
- REST APIs
- Redfish
- DMTF Redfish Mockup Server
- BMC and out-of-band management
- Server hardware monitoring
- Automated validation
- Failure detection and troubleshooting

## Future Improvements

- Connect the validator to physical Redfish-capable server hardware
- Add BIOS and firmware validation
- Add storage and network interface validation
- Add Redfish event and log analysis
- Add configurable validation requirements and thresholds
- Save validation results to report files
- Add automated unit and regression tests
- Improve handling of API connection failures and malformed responses
