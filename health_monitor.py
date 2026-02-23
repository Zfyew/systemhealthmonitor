# System Health Monitor
# v7: clean summary report on exit

import psutil
import os
import time

CPU_THRESHOLD = 80
MEM_THRESHOLD = 85

# tracks peak values during the session
peak_cpu = 0
peak_mem = 0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_bar(percent, width=20):
    filled = int(percent / 100 * width)
    return "█" * filled + "░" * (width - filled)

def monitor_cpu():
    global peak_cpu
    cpu = psutil.cpu_percent(interval=1)
    if cpu > peak_cpu:
        peak_cpu = cpu
    alert = " ⚠ HIGH" if cpu >= CPU_THRESHOLD else ""
    print(f"  CPU      [{get_bar(cpu)}] {cpu}%{alert}")
    return cpu

def monitor_memory():
    global peak_mem
    mem = psutil.virtual_memory()
    used = mem.used / (1024 ** 3)
    total = mem.total / (1024 ** 3)
    if mem.percent > peak_mem:
        peak_mem = mem.percent
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

def print_summary():
    print("\n" + "=" * 56)
    print("          SESSION SUMMARY")
    print("=" * 56)
    print(f"  Peak CPU usage:    {peak_cpu}%")
    print(f"  Peak memory usage: {peak_mem}%")
    if peak_cpu >= CPU_THRESHOLD:
        print(f"  ⚠ CPU hit the {CPU_THRESHOLD}% threshold during this session")
    if peak_mem >= MEM_THRESHOLD:
        print(f"  ⚠ Memory hit the {MEM_THRESHOLD}% threshold during this session")
    print("=" * 56)
    print()

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
    print_summary()