-- schema.sql
-- Agent tool-call monitoring table (HW_05).

CREATE TABLE IF NOT EXISTS agent_tool_calls (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    tool_input TEXT,
    tool_output TEXT,
    duration_ms FLOAT,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_tool_calls_session_id
    ON agent_tool_calls (session_id);

CREATE INDEX IF NOT EXISTS idx_agent_tool_calls_timestamp
    ON agent_tool_calls (timestamp);
