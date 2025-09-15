import socket
import time
import csv
from scapy.all import rdpcap, DNS

# Custom header in format HHMMSSID
def build_custom_header(seq_id: int) -> str:
    now = time.localtime()
    return f"{now.tm_hour:02d}{now.tm_min:02d}{now.tm_sec:02d}{seq_id:02d}"

def main():
    server_host = "127.0.0.1"
    server_port = 53535

    packets = rdpcap("0.pcap")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    seq_id = 0
    results = []

    for pkt in packets:
        if pkt.haslayer(DNS) and pkt[DNS].qr == 0:  # DNS Query
            custom_header = build_custom_header(seq_id)

            payload = custom_header.encode("utf-8") + bytes(pkt[DNS])
            sock.sendto(payload, (server_host, server_port))
            response, _ = sock.recvfrom(4096)

            # Parse response
            parts = response.decode("utf-8").split(" ")
            recv_header, domain, resolved_ip = parts[0], " ".join(parts[1:-1]), parts[-1]

            print(f"[CLIENT] Header: {recv_header} | Domain: {domain} | Resolved: {resolved_ip}")

            results.append([recv_header, domain, resolved_ip])
            seq_id += 1

    sock.close()

    # Saving results to CSV
    with open("dns_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Custom Header", "Domain", "Resolved IP"])
        writer.writerows(results)

if __name__ == "__main__":
    main()
