"""Open Library REST API pipeline. Books and authors endpoints; books use incremental loading by publish_date."""

import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)


@dlt.source
def open_library_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://openlibrary.org/",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "api/books",
                    "params": {
                        "bibkeys": "ISBN:0385472579,ISBN:0451526538",
                        "format": "json",
                        "jscmd": "data",
                    },
                    "data_selector": "$.*",
                    "paginator": {"type": "single_page"},
                    "incremental": {
                        "cursor_path": "publish_date",
                        "initial_value": "1970-01-01",
                    },
                },
            },
            {
                "name": "authors",
                "endpoint": {
                    "path": "search/authors.json",
                    "params": {
                        "q": "Stephen King",
                    },
                    "data_selector": "docs",
                    "paginator": {"type": "single_page"},
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def get_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name='open_library_pipeline',
        destination='duckdb',
        dataset_name='open_library_data',
        progress='log',
    )
    load_info = pipeline.run(open_library_source())
    print(load_info)


if __name__ == "__main__":
    get_data()
