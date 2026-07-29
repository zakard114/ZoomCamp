"""dlt REST API pipeline: Claude Code Agent Logs API -> playground lake.

Source: https://test-agent-traces-api-xt2e7ottma-ew.a.run.app
Endpoint: GET /logs — offset/limit pagination, records under `logs`, the
response envelope carries `total` (1,000,000). No auth.

Destination is the dltHub playground lake (persistent across cloud runs).
Local sample runs still use add_limit(1) unless --full is passed.
"""

import dlt
from dlt.hub import run
from dlt.hub.run import trigger
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

BASE_URL = "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app"


@dlt.source(name="agent_logs_api")
def agent_logs_source(base_url: str = dlt.config.value, page_size: int = 1000):
    """Claude Code Agent Logs API.

    Args:
        base_url: API base URL. Auto-loaded from config.toml ([sources.agent_logs_api]).
        page_size: records per page for the offset paginator.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "paginator": {
                "type": "offset",
                "limit": page_size,
                "offset": 0,
                "limit_param": "limit",
                "offset_param": "offset",
                "total_path": "total",  # read total record count from the envelope
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "logs",
                "endpoint": {
                    "path": "/logs",
                    "data_selector": "logs",  # records live under the "logs" key
                },
                "primary_key": "index",
            },
        ],
    }
    yield from rest_api_resources(config)


def load(full: bool = False) -> None:
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces",
        destination="playground",
        dataset_name="traces",
    )
    source = agent_logs_source(base_url=BASE_URL)
    if not full:
        source.add_limit(1)  # one page = 1000 records; pass --full for all 1M
    info = pipeline.run(source)
    print(info)
    print(pipeline.last_trace.last_normalize_info)


@run.pipeline("agent_traces", trigger=trigger.schedule("0 12 * * *"))
def ingest_agent_traces() -> None:
    """Cloud batch job: sample page only (safe). Use local --full for large loads."""
    load(full=False)


if __name__ == "__main__":
    import sys

    load(full="--full" in sys.argv)
