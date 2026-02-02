# Датасеты

## Google Cluster Trace

- **Источник:** публичные трассы Google Cluster Data.
- **Формат:** CSV/табличные файлы с метриками машин.
- **Ключевые поля:** `machine_id`, `timestamp`, `cpu_usage`, `mem_usage`.
- **Проблемы:** большие объёмы, требуется чтение чанками и агрегация во временные окна.

## Alibaba Cluster Trace

- **Источник:** Alibaba Cluster Trace (machine_usage/container_usage).
- **Формат:** CSV, несколько таблиц.
- **Ключевые поля:** `machine_id` или `container_id`, `time`, `cpu_usage`, `mem_usage`.
- **Проблемы:** выбор уровня агрегации (machine vs container), неоднородные схемы.

## Bitbrains

- **Источник:** Bitbrains VM dataset.
- **Формат:** CSV с метриками по VM.
- **Ключевые поля:** `vm_id`, `timestamp`, `cpu_usage`, `mem_usage`.
- **Проблемы:** разные единицы измерения, пропуски в метриках.
