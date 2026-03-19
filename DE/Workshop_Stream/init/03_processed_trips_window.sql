-- Question 6: 1-hour tumbling window, SUM(tip_amount) per hour
CREATE TABLE IF NOT EXISTS processed_trips_window (
    window_start TIMESTAMP(3),
    sum_tip DOUBLE PRECISION
);
