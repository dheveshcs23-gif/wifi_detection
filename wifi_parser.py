import re
import csv
from datetime import datetime

input_file = "wifi_raw.txt"
output_file = "wifi_dataset.csv"

with open(input_file, "r", encoding="utf-16") as file:
    data = file.read()

ssid_blocks = re.split(r"SSID \d+ :", data)[1:]

rows = []

for block in ssid_blocks:
    lines = block.strip().split("\n")
    ssid = lines[0].strip()

    auth = re.search(r"Authentication\s+:\s+(.*)", block)
    encryption = re.search(r"Encryption\s+:\s+(.*)", block)

    bssids = re.findall(r"BSSID \d+\s+:\s+([0-9a-f:]+)", block)
    signals = re.findall(r"Signal\s+:\s+(\d+)%", block)
    channels = re.findall(r"Channel\s+:\s+(\d+)", block)

    for i in range(len(bssids)):
        rows.append([
            datetime.now(),
            ssid,
            bssids[i],
            signals[i] if i < len(signals) else "",
            channels[i] if i < len(channels) else "",
            auth.group(1) if auth else "",
            encryption.group(1) if encryption else ""
        ])

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp","SSID","BSSID","Signal","Channel","Authentication","Encryption"])
    writer.writerows(rows)

print("Dataset created successfully.")