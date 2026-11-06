"""ЛР4. Автоматическая инвентаризация компьютера."""

import json
import platform
import socket
from datetime import datetime

import psutil


def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M"),
    }


def get_cpu_info():
    freq = psutil.cpu_freq()
    return {
        "model": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_freq_mhz": round(freq.max) if freq else None,
        "load_percent": psutil.cpu_percent(interval=1),
    }


def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / 1024**3, 1),
        "used_percent": mem.percent,
        "available_gb": round(mem.available / 1024**3, 1),
    }


def get_disk_info():
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        disks.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fs": part.fstype,
            "total_gb": round(usage.total / 1024**3, 1),
            "used_percent": usage.percent,
        })
    return disks


# ---------- Задание 2 ----------
def get_network_info():
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        ip = mask = mac = None
        for a in addrs:
            if a.family == socket.AF_INET:      # IPv4
                ip, mask = a.address, a.netmask
            elif a.family == psutil.AF_LINK:    # MAC-адрес
                mac = a.address
        if ip:                                  # без IPv4 - пропускаем
            interfaces.append({"name": name, "ipv4": ip, "netmask": mask, "mac": mac})
    return interfaces


# ---------- Задание 3 ----------
def analyze(passport):
    ram = passport["memory"]["total_gb"]
    cores = passport["cpu"]["physical_cores"]
    result = []

    if ram < 8:
        result.append("Недостаточно памяти для виртуальных машин и Docker")
    if ram >= 16 and cores >= 6:
        result.append("Подходит для одновременной работы нескольких VM")
    for disk in passport["disks"]:
        if disk["used_percent"] > 85:
            result.append(f"Освободить место на диске {disk['device']}")
    if cores < 4:
        result.append("Процессор может стать узким местом (bottleneck)")

    # Своё правило: память почти заполнена прямо сейчас
    if passport["memory"]["used_percent"] > 80:
        result.append("Оперативная память почти заполнена - закройте лишние программы")

    return result


def main():
    passport = {
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "network": get_network_info(),
    }
    passport["recommendations"] = analyze(passport)

    filename = f"passport_{passport['system']['hostname']}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(passport, f, indent=2, ensure_ascii=False)

    print(json.dumps(passport, indent=2, ensure_ascii=False))
    print(f"\nПаспорт сохранён в файл {filename}")


if __name__ == "__main__":
    main()
