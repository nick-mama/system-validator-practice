import requests

BASE_URL = "http://127.0.0.1:8000"

def get_redfish_data(endpoint):
    url = BASE_URL + endpoint

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

def validate_system(server):
    health = server["Status"]["Health"]
    power_state = server["PowerState"]

    if health == "OK" and power_state == "On":
        print(
            f"[PASS] System: health {health}, "
            f"power state {power_state}"
        )
        return True
    else:
        print(
            f"[FAIL] System: health {health}, "
            f"power state {power_state}"
        )
        return False

def validate_processors(server):
    count = server["ProcessorSummary"]["Count"]
    coreCount = server["ProcessorSummary"]["CoreCount"]
    health = server["ProcessorSummary"]["Status"]["Health"]

    if count > 0 and coreCount > 0 and health == "OK":
        print(f"[PASS] Processors: {count} CPUs, {coreCount} cores, health OK")
        return True
    else:
        print(f"[FAIL] Processors: {count} CPUs, {coreCount} cores, health {health}")
        return False

def validate_memory(server):
    health = server["MemorySummary"]["Status"]["Health"]
    state = server["MemorySummary"]["Status"]["State"]
    memory = server["MemorySummary"]["TotalSystemMemoryGiB"]

    if memory > 0 and health == "OK" and state == "Enabled":
        print(f"[PASS] Memory: {memory} GiB, health OK, state {state}")
        return True
    else:
        print(f"[FAIL] Memory: {memory} GiB, health {health}, state {state}")
        return False

def validate_fans(fans_collection):
    all_passed = True

    for member in fans_collection["Members"]:
        fan_endpoint = member["@odata.id"]
        fan = get_redfish_data(fan_endpoint)

        name = fan["Name"]
        speed_percent = fan["SpeedPercent"]["Reading"]
        rpm = fan["SpeedPercent"].get("SpeedRPM")
        health = fan["Status"]["Health"]
        state = fan["Status"]["State"]

        if speed_percent > 0 and health == "OK" and state == "Enabled":
            if rpm is not None:
                print(
                    f"[PASS] {name}: {speed_percent}% ({rpm} RPM), "
                    f"health {health}, state {state}"
                )
            else:
                print(
                    f"[PASS] {name}: {speed_percent}%, "
                    f"health {health}, state {state}"
                )
        else:
            print(
                f"[FAIL] {name}: {speed_percent}%, "
                f"health {health}, state {state}"
            )
            all_passed = False
    return all_passed

def validate_power_supplies(power_supplies_collection):
    all_passed = True

    for member in power_supplies_collection["Members"]:
        psu_endpoint = member["@odata.id"]
        psu = get_redfish_data(psu_endpoint)

        name = psu["Name"]
        state = psu["Status"]["State"]

        if state == "Absent":
            print(f"[INFO] {name}: not installed")
            continue
        
        health = psu["Status"].get("Health")
        line_input = psu.get("LineInputStatus")

        if health == "OK" and state == "Enabled" and line_input == "Normal":
            print(
                f"[PASS] {name}: health {health}, "
                f"state {state}, input {line_input}"
            )
        else:
            print(
                f"[FAIL] {name}: health {health}, "
                f"state {state}, input {line_input}"
            )
            all_passed = False
    return all_passed

# Get system data
server = get_redfish_data(
    "/redfish/v1/Systems/437XR1138R2"
)

# Chassis from system
chassis_endpoint = server["Links"]["Chassis"][0]["@odata.id"]
chassis = get_redfish_data(chassis_endpoint)

# Thermal subsystem from chassis
thermal_endpoint = chassis["ThermalSubsystem"]["@odata.id"]
thermal = get_redfish_data(thermal_endpoint)

# Fan collection
fans_endpoint = thermal["Fans"]["@odata.id"]
fans_collection = get_redfish_data(fans_endpoint)

# Power subsystem from chassis
power_endpoint = chassis["PowerSubsystem"]["@odata.id"]
power = get_redfish_data(power_endpoint)

# Power supply collection
power_supplies_endpoint = power["PowerSupplies"]["@odata.id"]
power_supplies_collection = get_redfish_data(power_supplies_endpoint)

print("=" * 45)
print("REDFISH SERVER VALIDATION REPORT")
print("=" * 45)

results = {
    "System": validate_system(server),
    "Processors": validate_processors(server),
    "Memory": validate_memory(server),
    "Fans": validate_fans(fans_collection),
    "Power Supplies": validate_power_supplies(power_supplies_collection)
}

print("\n" + "=" * 45)
print("VALIDATION SUMMARY")
print("=" * 45)

for test, result in results.items():
    status = "PASS" if result else "FAIL"
    print(f"{test}: {status}")

if all(results.values()):
    print("\nOverall result: PASS")
else:
    print("\nOverall result: FAIL")