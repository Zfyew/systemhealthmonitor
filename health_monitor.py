# System Health Monitor
# v1: CPU usage monitoring

import psutil
import time

def monitor_cpu():
    print("\n==============================")
    print("   SYSTEM HEALTH MONITOR     ")
    print("==============================")
    print("\n[*] Monitoring CPU usage (10 seconds)...\n")
    
    for i in range(10):
        cpu = psutil.cpu_percent(interval=1)
        bar = "█" * int(cpu / 5) + "░" * (20 - int(cpu / 5))
        print(f"    CPU: [{bar}] {cpu}%")
    
    print("\n[+] Done.")

monitor_cpu()