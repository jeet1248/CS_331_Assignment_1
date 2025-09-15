import socket
from scapy.all import DNS

# Predefined IP pool
IP_POOL = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
]

# Rules JSON
RULES = {
    "morning": {
        "time_range": "04:00-11:59",
        "hash_mod": 5,
        "ip_pool_start": 0,
        "description": "Morning traffic routed to first 5 IPs"
    },
    "afternoon": {
        "time_range": "12:00-19:59",
        "hash_mod": 5,
        "ip_pool_start": 5,
        "description": "Afternoon traffic routed to middle 5 IPs"
    },
    "night": {
        "time_range": "20:00-03:59",
        "hash_mod": 5,
        "ip_pool_start": 10,
        "description": "Night traffic routed to last 5 IPs"
    }
}

# Return rule dict based on hour
def get_time_period(hour: int) -> dict:
    if 4 <= hour <= 11:
        return RULES["morning"]
    elif 12 <= hour <= 19:
        return RULES["afternoon"]
    else:  # 20:00–03:59
        return RULES["night"]

# Selecting an IP based on custom header format HHMMSSID
def select_ip(custom_header: str) -> str:
    hour = int(custom_header[0:2])
    seq_id = int(custom_header[6:8])

    rule = get_time_period(hour)
    base_index = rule["ip_pool_start"]
    offset = seq_id % rule["hash_mod"]

    ip_index = base_index + offset
    return IP_POOL[ip_index]

def main():
    host = "127.0.0.1"
    port = 53535

    # Initialize a socket on localhost at port 53535
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[SERVER] Listening on {host}:{port}...")

    while True:
        data, addr = sock.recvfrom(4096)

        # Extracting custom header
        custom_header = data[:8].decode("utf-8")
        dns_payload = data[8:]

        # Parsing DNS query
        dns_packet = DNS(dns_payload)
        query_name = dns_packet.qd.qname.decode() if dns_packet.qd else "UNKNOWN"

        # Select IP based on header
        resolved_ip = select_ip(custom_header)

        print(f"[DEBUG] Query-Address: {addr} | Query: {query_name} | Header: {custom_header} | Resolved: {resolved_ip}")

        response = f"{custom_header} {query_name} {resolved_ip}"
        # print(f"[SERVER] Response: {response}")
        sock.sendto(response.encode("utf-8"), addr)

if __name__ == "__main__":
    main()