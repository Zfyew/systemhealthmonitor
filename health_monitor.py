# System Health Monitor
# v3: added disk usage monitoring

import psutil

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

def monitor_disk():
    print("\n[*] Disk Usage...\n")
    # check all mounted drives
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            used = usage.used / (1024 ** 3)
            total = usage.total / (1024 ** 3)
            percent = usage.percent
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            print(f"    {partition.device}")
            print(f"    [{bar}] {percent}%  {used:.2f} GB / {total:.2f} GB\n")
        except PermissionError:
            # some drives like card readers show up but can't be read
            pass

print("\n==============================")
print("   SYSTEM HEALTH MONITOR     ")
print("==============================")

monitor_cpu()
monitor_memory()
monitor_disk()

print("\n[+] Done.")