import pyeapi
import yaml
import requests
import json

# Disable SSL certificate verification globally (For self-signed certs)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Load hosts from YAML
with open("hosts.yaml", "r") as file:
    hosts = yaml.safe_load(file)

for host in hosts["hosts"]:
    print(f"Connecting to {host['name']} ({host['ip']})...")

    # Connect to EOS switch (Force HTTPS with ignored SSL warnings)
    conn = pyeapi.connect(
        transport="https",
        host=host["ip"],
        username=host["username"],
        password=host["password"],
        timeout=10,
        verify=False  # This disables SSL verification
    )

    try:
        # Execute the command to get IP interfaces
        response = conn.execute("show ip interface")

        # Extract results
        if "result" in response and isinstance(response["result"], list):
            interfaces = response["result"][0].get("interfaces", {})

            # Filter only Loopback0 and Loopback1
            for loopback in ["Loopback0", "Loopback1"]:
                if loopback in interfaces:
                    primary_ip = interfaces[loopback].get("interfaceAddress", {}).get("primaryIp", {}).get("address", "N/A")
                    print(f"{loopback}: {primary_ip}")

    except Exception as e:
        print(f"Failed to retrieve loopbacks from {host['name']}: {e}")
