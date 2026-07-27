"""Deployment manifest — import the pipelines and notebooks you want to deploy and list them in __all__."""

# Import the dashboard MODULE (not `app`). Putting marimo.App into this
# module makes detect_module_job treat __deployment__ itself as the only job
# and skips batch jobs listed in __all__.
import agent_traces_dashboard
from pipelines.rest_api_pipeline import ingest_agent_traces

__all__ = [
    "ingest_agent_traces",
    "agent_traces_dashboard",
]
