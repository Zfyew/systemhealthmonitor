# System Health Monitor
# v2: added memory usage monitoring

import psutil
import time

def monitor_cpu():
    print("\n[*] CPU Usage (10 seconds)...\n")
    for i in range(10):
        cpu = psutil.cpu_percent(interval=1)
        bar = "█" * int(cpu / 5) + "░" * (20 - int(cpu / 5))
        print(f"    CPU: [{bar}] {cpu}%")

def monitor_memory():
    print("\n[*] Memory Usage...\n")
    mem = psutil.virtual_memory()
    used = mem.used / (1024 ** 3)
    total = mem.total / (1024 ** 3)
    percent = mem.percent
    bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
    print(f"    RAM: [{bar}] {percent}%")
    print(f"    Used: {used:.2f} GB / {total:.2f} GB")

print("\n==============================")
print("   SYSTEM HEALTH MONITOR     ")
print("==============================")

monitor_cpu()
monitor_memory()

print("\n[+] Done.")