# System Health Monitor
# v4: added running process list

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

def list_processes():
    print("\n[*] Top 10 processes by memory usage...\n")
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            procs.append(proc.info)
        except psutil.NoSuchProcess:
            # process closed while we were reading it
            pass

    # sort by memory and grab top 10
    procs = sorted(procs, key=lambda x: x['memory_percent'], reverse=True)[:10]

    print(f"    {'PID':<8} {'Name':<30} {'Memory':>8} {'CPU':>8}")
    print(f"    {'-'*56}")
    for p in procs:
        print(f"    {p['pid']:<8} {p['name'][:28]:<30} {p['memory_percent']:>7.1f}% {p['cpu_percent']:>7.1f}%")

print("\n==============================")
print("   SYSTEM HEALTH MONITOR     ")
print("==============================")

monitor_cpu()
monitor_memory()
monitor_disk()
list_processes()

print("\n[+] Done.")