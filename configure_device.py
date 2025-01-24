import pyeapi

# Define the target device for configuration
target_device = "BLS-001"
target_ip = "10.10.10.92"
enable_password = "Goobies83"  # 'enable' password (assuming cvpadmin has privilege 15)

# Device credentials
username = "cvpadmin"
password = "Bhara_8nath_ITCE"

# Connect to the target device
try:
    # Using HTTPS transport (most common for pyeapi)
    conn = pyeapi.connect(
        transport="https",  # Ensure that the transport is HTTPS
        host=target_ip,
        username=username,
        password=password,
        timeout=10,
        verify=False  # Disable SSL verification for testing
    )
    print(f"Connected to {target_device} at IP: {target_ip}")

    # Enter global configuration mode
    conn.execute("configure terminal")
    print(f"Entering config mode on {target_device}")

    # Apply configuration commands to the target device
    config_commands = [
        "interface Ethernet3",
        "description Spine1",
        "no switchport",
        "ip address 10.0.5.1/31",
        "mtu 9214",
        "no shutdown",
        "interface Ethernet4",
        "description Spine2",
        "no switchport",
        "ip address 10.0.6.1/31",
        "mtu 9214",
        "no shutdown",
        "interface Ethernet5",
        "description Spine2",
        "no switchport",
        "ip address 10.0.7.1/31",
        "mtu 9214",
        "no shutdown",
        "interface Ethernet6",
        "description Spine2",
        "no switchport",
        "ip address 10.0.8.1/31",
        "mtu 9214",
        "no shutdown",
        "vlan 4091",
        "name mlag-ibgp",
        "vlan 40",
        "name test-l2-vxlan",
        "vrf instance gold",
        "ip routing vrf gold",
        "interface vlan 4091",
        "ip address 10.0.9.4/31",
        "mtu 9214",
        "no shutdown",
        "interface loopback0",
        "ip address 10.0.250.15/32",
        "interface loopback1",
        "ip address 10.0.255.15/32",
        "router bgp 65003",
        "router-id 10.0.250.15",
        "no bgp default ipv4-unicast",
        "bgp log-neighbor-changes",
        "distance bgp 20 200 200",
        "neighbor underlay peer group",
        "neighbor underlay remote-as 65000",
        "neighbor underlay maximum-routes 12000 warning-only",
        "neighbor underlay send-community",
        "neighbor 10.0.5.0 peer group underlay",
        "neighbor 10.0.6.0 peer group underlay",
        "neighbor 10.0.7.0 peer group underlay",
        "neighbor 10.0.8.0 peer group underlay",
        "neighbor underlay_ibgp remote-as 65003",
        "neighbor underlay_ibgp maximum-routes 12000 warning-only",
        "neighbor underlay_ibgp next-hop-self",
        "neighbor underlay_ibgp send-community",
        "neighbor 10.0.9.5 peer group underlay_ibgp",
        "address-family ipv4",
        "neighbor underlay activate",
        "neighbor underlay_ibgp activate",
        "neighbor 10.90.90.1 activate",
        "network 10.0.250.15/32",
        "network 10.0.255.15/32",
        "maximum-paths 4 ecmp 64",
        "neighbor evpn peer group",
        "neighbor evpn remote-as 65000",
        "neighbor evpn update-source Loopback0",
        "neighbor evpn ebgp-multihop 3",
        "neighbor evpn send-community extended",
        "neighbor evpn maximum-routes 12000 warning-only",
        "neighbor 10.0.250.1 peer group evpn",
        "neighbor 10.0.250.2 peer group evpn",
        "neighbor 10.0.250.3 peer group evpn",
        "neighbor 10.0.250.4 peer group evpn",
        "address-family evpn",
        "neighbor evpn activate",
        "vlan 40",
        "rd 65003:100040",
        "route-target both 40:100040",
        "redistribute learned",
        "vlan 34",
        "rd 65003:100040",
        "route-target both 34:100034",
        "redistribute learned",
        "vlan 78",
        "rd 65003:100040",
        "route-target both 78:100078",
        "redistribute learned",
        "vrf gold",
        "rd 10.0.250.15:1",
        "route-target both 1:100001",
        "redistribute connected",
        "neighbor 10.90.90.1 remote-as 64999",
        "address-family ipv4",
        "neighbor 10.90.90.1 activate",
        "interface vxlan1",
        "vxlan source-int loopback1",
        "vxlan udp-port 4789",
        "vxlan learn-restrict any",
        "vxlan vlan 40 vni 100040",
        "vxlan vlan 34 vni 100034",
        "vxlan vlan 78 vni 100078",
        "vxlan vrf gold vni 100001",
        "no shutdown",
        "vlan 34",
        "vlan 78",
        "vlan 10",
        "interface vlan 10",
        "vrf gold",
        "ip address 10.90.90.2/29",
        "no shutdown",
        "interface Ethernet24",
        "switchport",
        "switchport access vlan 40",
        "no shutdown"
    ]

    # Execute configuration commands on the device
    for command in config_commands:
        conn.execute(command)
    print(f"Configuration applied successfully on {target_device}")

except Exception as e:
    print(f"Failed to configure {target_device}: {e}")
