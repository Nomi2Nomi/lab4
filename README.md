# Лабораторная работа №4. Автоматизированная инвентаризация и мониторинг рабочей станции на Python

**ФИО:** Таипова Лейли Алчиновна
**Группа:** ПТ 16:30
**Вариант:** 11

## Что делает каждый скрипт

| Файл | Назначение |
| --- | --- |
| `inventory.py` | Агент инвентаризации. Собирает данные о системе, процессоре, памяти, дисках и сети, делает рекомендации (`analyze`) и сохраняет всё в `passport_<имя_компьютера>.json`. |
| `monitor.py` | Мониторинг нагрузки. Делает 15 замеров CPU / RAM / DISK каждые 2 секунды, сравнивает с порогами, пишет журнал в `monitor_log.csv` и в конце выводит среднее, максимум и минимум. |

## Параметры варианта 11

- INTERVAL = 2 с
- SAMPLES = 15
- Пороги CPU / RAM / DISK = 70 / 90 / 85 %
- Дополнительная метрика: время работы без перезагрузки, часы (`uptime_h`)

## Подготовка

```bash
mkdir lab1 && cd lab1
python3 -m venv venv
source venv/bin/activate        
pip install psutil
```

## Запуск

```bash
python inventory.py     # создаёт passport_<имя>.json
python monitor.py       # создаёт monitor_log.csv 
```

## Пример вывода

### inventory.py

```
{
  "collected_at": "2026-11-06 14:54:52",
  "system": {
    "hostname": "Nomis-MacBook-Air.local",
    "os": "Darwin",
    "os_version": "Darwin Kernel Version 24.6.0: Wed Nov  5 21:34:00 PST 2025; root:xnu-11417.140.69.705.2~1/RELEASE_ARM64_T8132",
    "architecture": "arm64",
    "boot_time": "2026-10-17 21:43"
  },
  "cpu": {
    "model": "arm",
    "physical_cores": 10,
    "logical_cores": 10,
    "max_freq_mhz": 4,
    "load_percent": 4.0
  },
  "memory": {
    "total_gb": 16.0,
    "used_percent": 69.1,
    "available_gb": 4.9
  },
  "disks": [
    {
      "device": "/dev/disk3s1s1",
      "mountpoint": "/",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 35.4
    },
    {
      "device": "/dev/disk3s6",
      "mountpoint": "/System/Volumes/VM",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 13.8
    },
    {
      "device": "/dev/disk3s2",
      "mountpoint": "/System/Volumes/Preboot",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 32.3
    },
    {
      "device": "/dev/disk3s4",
      "mountpoint": "/System/Volumes/Update",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 2.3
    },
    {
      "device": "/dev/disk1s2",
      "mountpoint": "/System/Volumes/xarts",
      "fs": "apfs",
      "total_gb": 0.5,
      "used_percent": 1.2
    },
    {
      "device": "/dev/disk1s1",
      "mountpoint": "/System/Volumes/iSCPreboot",
      "fs": "apfs",
      "total_gb": 0.5,
      "used_percent": 1.2
    },
    {
      "device": "/dev/disk1s3",
      "mountpoint": "/System/Volumes/Hardware",
      "fs": "apfs",
      "total_gb": 0.5,
      "used_percent": 0.4
    },
    {
      "device": "/dev/disk3s5",
      "mountpoint": "/System/Volumes/Data",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 83.3
    },
    {
      "device": "/dev/disk2s1",
      "mountpoint": "/System/Volumes/Update/SFR/mnt1",
      "fs": "apfs",
      "total_gb": 5.0,
      "used_percent": 43.2
    },
    {
      "device": "/dev/disk3s1",
      "mountpoint": "/System/Volumes/Update/mnt1",
      "fs": "apfs",
      "total_gb": 228.3,
      "used_percent": 35.4
    }
  ],
  "network": [
    {
      "name": "lo0",
      "ipv4": "127.0.0.1",
      "netmask": "255.0.0.0",
      "mac": null
    },
    {
      "name": "en0",
      "ipv4": "10.140.224.160",
      "netmask": "255.255.255.0",
      "mac": "36:2e:07:05:57:d9"
    },
    {
      "name": "utun4",
      "ipv4": "100.96.11.26",
      "netmask": "255.255.255.240",
      "mac": null
    }
  ],
  "recommendations": [
    "Подходит для одновременной работы нескольких VM"
  ]
}
```

### monitor.py

```
14:56:45  CPU   5.7%  RAM  69.1%  DISK  35.4%  UPTIME 473.2 ч
14:56:47  CPU   5.0%  RAM  69.0%  DISK  35.4%  UPTIME 473.2 ч
14:56:49  CPU   4.3%  RAM  68.9%  DISK  35.4%  UPTIME 473.2 ч
14:56:51  CPU   6.4%  RAM  68.9%  DISK  35.4%  UPTIME 473.2 ч
14:56:53  CPU   4.8%  RAM  68.9%  DISK  35.4%  UPTIME 473.2 ч
14:56:55  CPU   5.5%  RAM  69.1%  DISK  35.4%  UPTIME 473.2 ч
14:56:57  CPU   4.6%  RAM  69.0%  DISK  35.4%  UPTIME 473.2 ч
14:56:59  CPU  13.3%  RAM  69.9%  DISK  35.4%  UPTIME 473.2 ч
14:57:01  CPU  10.5%  RAM  68.6%  DISK  35.4%  UPTIME 473.2 ч
14:57:03  CPU  10.5%  RAM  69.2%  DISK  35.4%  UPTIME 473.2 ч
14:57:05  CPU   6.1%  RAM  68.6%  DISK  35.4%  UPTIME 473.2 ч
14:57:07  CPU   4.0%  RAM  68.6%  DISK  35.4%  UPTIME 473.2 ч
14:57:09  CPU  11.7%  RAM  69.1%  DISK  35.4%  UPTIME 473.2 ч
14:57:11  CPU   4.3%  RAM  69.2%  DISK  35.4%  UPTIME 473.2 ч
14:57:13  CPU   6.6%  RAM  69.2%  DISK  35.4%  UPTIME 473.2 ч

Журнал сохранён в monitor_log.csv

Итоги:
CPU   среднее   6.9%  макс  13.3%  мин   4.0%
RAM   среднее  69.0%  макс  69.9%  мин  68.6%
DISK  среднее  35.4%  макс  35.4%  мин  35.4%
```
