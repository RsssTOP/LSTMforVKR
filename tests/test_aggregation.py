import pandas as pd
import pytest

from wkr.data.common import aggregate_time_series


def test_aggregate_time_series():
    df = pd.DataFrame(
        {
            "dataset": ["google", "google", "google"],
            "entity_id": ["m1", "m1", "m2"],
            "timestamp": [0, 60, 0],
            "cpu_usage": [0.5, 0.7, 0.2],
            "mem_usage": [0.2, 0.4, 0.1],
            "disk_io": [1.0, 1.5, 0.5],
            "net_io": [2.0, 2.5, 1.0],
            "label": [None, None, None],
            "source_fields": ["{}", "{}", "{}"],
        }
    )

    aggregated = aggregate_time_series(df, window="2min", timestamp_unit="s")

    m1_rows = aggregated[aggregated["entity_id"] == "m1"]
    assert len(m1_rows) == 1
    assert m1_rows["cpu_usage"].iloc[0] == pytest.approx(0.6)
    assert m1_rows["mem_usage"].iloc[0] == pytest.approx(0.3)
