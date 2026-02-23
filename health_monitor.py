# System Health Monitor
# v6: alerts when CPU or memory goes above set thresholds

import psutil
import os
import time

# anything above these levels triggers a warning
CPU_THRESHOLD = 80
MEM_THRESHOLD = 85

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_bar(percent, width=20):
    filled = int(percent / 100 * width)
    return "█" * filled + "░" * (width - filled)

def monitor_cpu():
    cpu = psutil.cpu_percent(interval=1)
    alert = " ⚠ HIGH" if cpu >= CPU_THRESHOLD else ""
    print(f"  CPU      [{get_bar(cpu)}] {cpu}%{alert}")
    return cpu

def monitor_memory():
    mem = psutil.virtual_memory()
    used = mem.used / (1024 ** 3)
    total = mem.total / (1024 ** 3)
    alert = " ⚠ HIGH" if mem.percent >= MEM_THRESHOLD else ""
    print(f"  RAM      [{get_bar(mem.percent)}] {mem.percent}%  {used:.1f} GB / {total:.1f} GB{alert}")
    return mem.percent

def monitor_disk():
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            used = usage.used / (1024 ** 3)
            total = usage.total / (1024 ** 3)
            print(f"  {partition.device[:6]:<6}   [{get_bar(usage.percent)}] {usage.percent}%  {used:.1f} GB / {total:.1f} GB")
        except PermissionError:
            pass

def list_processes():
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            procs.append(proc.info)
        except psutil.NoSuchProcess:
            pass

    procs = sorted(procs, key=lambda x: x['memory_percent'], reverse=True)[:5]
    print(f"\n  {'PID':<8} {'Name':<28} {'Mem':>6} {'CPU':>6}")
    print(f"  {'-'*52}")
    for p in procs:
        print(f"  {p['pid']:<8} {p['name'][:26]:<28} {p['memory_percent']:>5.1f}% {p['cpu_percent']:>5.1f}%")

def show_alerts(cpu, mem):
    alerts = []
    if cpu >= CPU_THRESHOLD:
        alerts.append(f"  ⚠ CPU above {CPU_THRESHOLD}% — currently at {cpu}%")
    if mem >= MEM_THRESHOLD:
        alerts.append(f"  ⚠ Memory above {MEM_THRESHOLD}% — currently at {mem}%")
    if alerts:
        print("\n" + "\n".join(alerts))

print("Press Ctrl+C to exit\n")
time.sleep(1)

try:
    while True:
        clear()
        print("=" * 56)
        print("          SYSTEM HEALTH MONITOR")
        print("=" * 56)
        cpu = monitor_cpu()
        mem = monitor_memory()
        monitor_disk()
        list_processes()
        show_alerts(cpu, mem)
        print(f"\n  Refreshing every 2 seconds. Ctrl+C to exit.")
        print("=" * 56)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\nMonitor stopped.\n")