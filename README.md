# System Health Monitor

Python script that keeps an eye on system resources in real time. Runs as a live 
dashboard that refreshes every 2 seconds showing CPU, memory and disk usage alongside 
the top 5 processes by memory. Alerts you if CPU or memory goes above set thresholds 
and prints a session summary when you exit.

## How to run

    python health_monitor.py

Hit Ctrl+C to stop. Summary prints on exit.

## What it monitors

- CPU usage with live progress bar
- RAM usage and how much is used out of total
- Disk usage across all drives
- Top 5 processes by memory

## Alerts

Warns if CPU goes above 80% or memory above 85% during the session.
Default thresholds can be changed at the top of the script.
