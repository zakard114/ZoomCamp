"""NYC taxi data REST API pipeline. Paginated JSON, 1000 records per page, stop on empty page."""

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source
def nyc_taxi_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "trips",
                "endpoint": {
                    "path": "",
                    "params": {
                        "limit": 1000,
                    },
                    "data_selector": "$",
                    "paginator": {
                        "type": "offset",
                        "limit": 1000,
                        "offset": 0,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": None,
                        "stop_after_empty_page": True,
                    },
                },
            },
        ],
    }
    yield from rest_api_resources(config)


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="ny_taxi_data",
        progress="log",
    )
    load_info = pipeline.run(nyc_taxi_source())
    print(load_info)


if __name__ == "__main__":
    main()
