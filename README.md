# ВКР: оптимизация распределения нагрузки на серверы

Проект посвящён оптимизации распределения нагрузки/задач на серверы с помощью ML: прогнозирование временных рядов (LSTM) и сравнение методов кластеризации. Цель — унифицировать данные из разных трасс, построить надёжный пайплайн предобработки и подготовить основу для дальнейшего моделирования.

## Датасеты

Используются три источника:

- **Google Cluster Trace** — данные о нагрузке и ресурсах машин в кластере.
- **Alibaba Cluster Trace** — трассы использования ресурсов контейнеров/машин.
- **Bitbrains** — метрики виртуальных машин.

Подробности: [docs/datasets.md](docs/datasets.md).

## Структура репозитория

- `data/raw` — сырые данные (не коммитим).
- `data/interim` — промежуточные результаты (валидация).
- `data/processed` — унифицированные parquet-файлы.
- `src/wkr` — код пайплайна, фичей и моделей.
- `scripts` — CLI-скрипты.
- `docs` — документация.

## Быстрый старт

### Установка

```bash
poetry install
```

### Подготовка данных

Положите исходные файлы:

```
data/raw/google/trace.csv
data/raw/alibaba/trace.csv
data/raw/bitbrains/trace.csv
```

### Запуск пайплайна

```bash
poetry run python scripts/run_preprocessing.py --dataset google --config src/wkr/config/default.yaml --validate
poetry run python scripts/run_preprocessing.py --dataset alibaba --config src/wkr/config/default.yaml --validate
poetry run python scripts/run_preprocessing.py --dataset bitbrains --config src/wkr/config/default.yaml --validate
```

## Выходные данные

Каждый датасет приводится к единому формату и сохраняется в `data/processed/<dataset>.parquet` со схемой:

- `dataset` — источник (`google|alibaba|bitbrains`).
- `entity_id` — идентификатор объекта (машина/контейнер/VM).
- `timestamp` — временная метка (datetime, UTC).
- `cpu_usage` — использование CPU.
- `mem_usage` — использование памяти.
- `disk_io` — дисковый ввод-вывод.
- `net_io` — сетевой ввод-вывод.
- `label` — тип события/уровень агрегации.
- `source_fields` — JSON-описание источников колонок.

## Команды качества

```bash
make format
make lint
make test
```
