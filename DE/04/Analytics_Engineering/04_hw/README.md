dbt Homework 4: Analytics Engineering (NYC Taxi Data)

This folder contains the SQL solutions and execution summaries for the Module 4 homework, focusing on dbt (data build tool) modeling, data testing, and resource-efficient pipeline execution in a local environment.

📂 Project Structure
Plaintext
ZoomCamp/DE/04/Analytics_Engineering/04_hw/
├── homework_4_solution.sql   # Comprehensive SQL results and validation queries
└── README.md                 # Project overview and technical optimization notes

Key Takeaways
1. Selective Model Execution
dbt selectors: Used --select flag to build specific models (int_trips_unioned, fct_monthly_zone_revenue) rather than the entire project.

Result: Successfully isolated dependencies and validated logic without exhausting system resources.

2. Testing and Validation (Question 2)
Data Integrity: Understood the mechanism of accepted_values tests.

Fail-fast Principle: Confirmed that dbt returns a non-zero exit code upon test failure, ensuring that upstream data quality issues block downstream deployment in production environments.

3. Resource Optimization (Question 3 & 6)
Hardware Constraints: Managed a 12GB RAM environment by tuning profiles.yml with threads: 1 and memory_limit: 3GB.

DuckDB Efficiency: For large-scale data (43M+ rows in FHV 2019), utilized DuckDB's native read_csv_auto to achieve efficient scanning and filtering, bypassing dbt model overhead where appropriate for quick validation.

4. Dimensionality in Modeling
Validated the expected granularity of the monthly revenue model: 24 months × 265 zones × 2 service types, resulting in exactly 12,998 records.

SQL Scripts
homework_4_solution.sql: Contains the full record of terminal commands, DuckDB queries, and logic used to derive the homework answers.