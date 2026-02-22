import pandas as pd
import subprocess
import re

print("\n========== CONNECTED WIFI ANALYSIS ==========\n")

# Get connected Wi-Fi details from Windows
interface_info = subprocess.getoutput("netsh wlan show interfaces")

# Extract SSID
ssid_match = re.search(r"^\s*SSID\s+:\s(.+)", interface_info, re.MULTILINE)

if not ssid_match:
    print("No Wi-Fi connected.")
    exit()

connected_ssid = ssid_match.group(1).strip()
print("Connected Network:", connected_ssid)

# Extract current signal strength
signal_match = re.search(r"^\s*Signal\s+:\s(\d+)%", interface_info, re.MULTILINE)

if signal_match:
    current_signal = int(signal_match.group(1))
else:
    current_signal = None

# Load dataset
df = pd.read_csv("wifi_dataset.csv")

# Filter dataset for connected SSID
df_filtered = df[df["SSID"] == connected_ssid]


if df_filtered.empty:
    print("No dataset information found for this network.")
    exit()

# Calculate dataset statistics
bssid_count = df_filtered["BSSID"].nunique()
encryption_types = df_filtered["Encryption"].nunique()
avg_signal = df_filtered["Signal"].astype(int).mean()

risk_score = 0
reasons = []

# Rule 1: Multiple BSSID (more than expected)
if bssid_count > 2:
    risk_score += 30
    reasons.append("Multiple BSSID detected")

# Rule 2: Encryption mismatch
auth_types = df_filtered["Authentication"].nunique()

if auth_types > 1:
    risk_score += 50
    reasons.append("Authentication mismatch detected")

# Rule 3: Adaptive Signal Anomaly Detection
if current_signal is not None:
    signal_difference = current_signal - avg_signal

    if signal_difference > 40:
        risk_score += 20
        reasons.append("Signal significantly stronger than historical average")

# Classification
if risk_score >= 60:
    status = "⚠ HIGH RISK (Possible Evil Twin)"
elif risk_score >= 30:
    status = "⚠ Suspicious"
else:
    status = "Legitimate"

print("Risk Score:", str(risk_score) + "%")
print("Status:", status)

if reasons:
    print("Reason:")
    for r in reasons:
        print("-", r)

print("----------------------------------")