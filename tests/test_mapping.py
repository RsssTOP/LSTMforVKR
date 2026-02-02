import pandas as pd

from wkr.data.common import MappingConfig, apply_column_mapping


def test_apply_column_mapping():
    df = pd.DataFrame(
        {
            "time": [1, 2],
            "machine_id": ["m1", "m1"],
            "cpu": [0.5, 0.7],
            "mem": [0.2, 0.3],
        }
    )
    mapping = MappingConfig(
        timestamp="time",
        entity_id="machine_id",
        cpu_usage="cpu",
        mem_usage="mem",
    )

    mapped = apply_column_mapping(df, mapping, dataset="google")

    assert list(mapped["timestamp"]) == [1, 2]
    assert list(mapped["entity_id"]) == ["m1", "m1"]
    assert list(mapped["cpu_usage"]) == [0.5, 0.7]
    assert list(mapped["mem_usage"]) == [0.2, 0.3]
    assert mapped["dataset"].unique().tolist() == ["google"]
