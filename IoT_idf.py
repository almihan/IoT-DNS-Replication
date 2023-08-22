from scapy.all import *
from collections import defaultdict
import numpy as np
import pandas as pd
from scapy.layers.dns import DNSQR, DNSRR
from scapy.layers.inet import IP

# Define your pcap file
pcap_file = "data8_1.pcap"

# Read the .pcap file
packets = rdpcap(pcap_file)

# Create a dictionary to store the number of clients that query each domain
domain_client_counts = defaultdict(set)

# Iterate over the packets and extract the DNS queries, answers, and the clients that made them
for packet in packets:
    if packet.haslayer(DNSQR):
        domain = packet[DNSQR].qname.decode("utf-8")
        client_ip = packet[IP].dst
        domain_client_counts[domain].add(client_ip)
    if packet.haslayer(DNSRR):
        domain = packet[DNSRR].rrname.decode("utf-8")
        client_ip = packet[IP].dst
        domain_client_counts[domain].add(client_ip)

# Compute the total number of clients that queried at least one IoT domain
all_clients = set()
for clients in domain_client_counts.values():
    all_clients.update(clients)

total_unique_clients = len(all_clients)
# Compute the IDF for each domain
idf = {}
for domain, clients in domain_client_counts.items():
    idf[domain] = np.log(1 + all_clients / (1 + len(clients)))

# Convert the IDF scores to a DataFrame and save it to a CSV file
df_idf = pd.DataFrame(list(idf.items()), columns=['Domain', 'IDF'])
df_idf.to_csv("domain_idf.csv", index=False)
