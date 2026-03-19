-- Question 5: Session window per PULocationID - longest streak = max num_trips in a session at one zone
CREATE TABLE IF NOT EXISTS session_streaks (
    session_start TIMESTAMP(3),
    session_end TIMESTAMP(3),
    pulocationid INTEGER,
    num_trips BIGINT
);
