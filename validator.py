import json
import sys

def load_server_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    return data


def validate_system_health(server):
    health = server["system"]["health"]

    if health == "OK":
        print("[PASS] System health: OK")
        return True
    else:
        print(f"[FAIL] System health: {health}")
        return False

def validate_processors(server):
    count = server["processors"]["count"]
    health = server["processors"]["health"]

    if count == 2 and health == "OK":
        print(f"[PASS] Processors: {count} detected, health OK")
        return True
    else:
        print(f"[FAIL] Processors: {count} detected, health {health}")
        return False

def validate_memory(server):
    total_gb = server["memory"]["total_gb"]
    health = server["memory"]["health"]

    if total_gb == 256 and health == "OK":
        print(f"[PASS] Memory: {total_gb} GB detected, health OK")
        return True
    else:
        print(f"[FAIL] Memory: {total_gb} GB detected, health {health}")
        return False

def validate_temperature(server):
    temperature = server["thermal"]["cpu_temperature_c"]
    max_temperature = server["thermal"]["max_temperature_c"]

    if temperature <= max_temperature:
        print(
            f"[PASS] CPU temperature: {temperature} C "
            f"(limit: {max_temperature} C)"
        )
        return True
    else:
        print(
            f"[FAIL] CPU temperature: {temperature} C "
            f"(exceeds limit of {max_temperature} C)"
        )
        return False

def validate_fans(server):
    MIN_FAN_RPM = 1000
    fans = server["fans"]
    all_passed = True

    for fan in fans:
        name = fan["name"]
        rpm = fan["rpm"]
        health = fan["health"]

        if rpm >= MIN_FAN_RPM and health == "OK":
            print(f"[PASS] {name}: {rpm} RPM, health OK")
        else:
            print(f"[FAIL] {name}: {rpm} RPM, health {health}")
            all_passed = False

    return all_passed

def validate_power_supplies(server):
    powers = server["power_supplies"]
    all_passed = True

    for power in powers:
        name = power["name"]
        health = power["health"]

        if health == "OK":
            print(f"[PASS] {name}: health OK")
        else:
            print(f"[FAIL] {name}: health {health}")
            all_passed = False
    
    return all_passed

if len(sys.argv) != 2:
    print("Usage: py validator.py <server_data.json>")
    sys.exit(1)

filename = sys.argv[1]
server = load_server_data(filename)

print("=" * 40)
print("SERVER VALIDATION REPORT")
print("=" * 40)

results = []

results.append(validate_system_health(server))
results.append(validate_processors(server))
results.append(validate_memory(server))
results.append(validate_temperature(server))
results.append(validate_fans(server))
results.append(validate_power_supplies(server))

passed = results.count(True)
failed = results.count(False)

print("\n" + "=" * 40)
print("VALIDATION SUMMARY")
print("=" * 40)

print(f"Test groups passed: {passed}")
print(f"Test groups failed: {failed}")

if failed == 0:
    print("Overall result: PASS")
else:
    print("Overall result: FAIL")