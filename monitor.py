"""ЛР4. Мониторинг нагрузки с порогами и журналом в CSV. Вариант 11."""

import csv
import time
from datetime import datetime

import psutil

INTERVAL = 2          # секунд между замерами
SAMPLES = 15          # количество замеров
THRESHOLDS = {"cpu": 70, "ram": 90, "disk": 85}
LOG_FILE = "monitor_log.csv"


def take_sample():
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        # дополнительная метрика варианта 11: время работы без перезагрузки, часы
        "uptime_h": round((time.time() - psutil.boot_time()) / 3600, 1),
    }


def check_alerts(sample):
    alerts = []
    for metric, limit in THRESHOLDS.items():
        if sample[metric] >= limit:
            alerts.append(f"{metric.upper()} = {sample[metric]}% (порог {limit}%)")
    return alerts


def main():
    psutil.cpu_percent(interval=None)  # первый вызов всегда 0, «прогреваем»
    samples = []                       # сюда складываем все замеры для статистики

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["time", "cpu", "ram", "disk", "uptime_h", "alert"])
        writer.writeheader()

        for _ in range(SAMPLES):
            time.sleep(INTERVAL)
            s = take_sample()
            alerts = check_alerts(s)
            s["alert"] = "; ".join(alerts)
            writer.writerow(s)
            samples.append(s)
            mark = "  <-- ВНИМАНИЕ: " + s["alert"] if alerts else ""
            print(f"{s['time']}  CPU {s['cpu']:5.1f}%  RAM {s['ram']:5.1f}%  "
                  f"DISK {s['disk']:5.1f}%  UPTIME {s['uptime_h']} ч{mark}")

    print(f"\nЖурнал сохранён в {LOG_FILE}")

    # Итоги: среднее, максимум и минимум по каждой метрике
    print("\nИтоги:")
    for metric in ["cpu", "ram", "disk"]:
        values = [s[metric] for s in samples]
        print(f"{metric.upper():5} среднее {sum(values) / len(values):5.1f}%  "
              f"макс {max(values):5.1f}%  мин {min(values):5.1f}%")


if __name__ == "__main__":
    main()
