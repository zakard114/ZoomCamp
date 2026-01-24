# Data Engineering Zoomcamp 2026 - Module 1 Homework

This repository contains the solutions for the **Data Engineering Zoomcamp 2026** Module 1 homework, covering Docker, SQL, and Terraform.

## 🚀 Key Highlights & Differentiation
* **Early Adoption of Orchestration**: I integrated **Kestra's Backfill feature** (originally a Module 2 topic) into this module. This enabled an automated and efficient data loading process for the October 2019 dataset, optimizing resource management compared to manual scripts.
* **Infrastructure as Code (IaC)**: Provisioned GCP resources using **Terraform**, focusing on professional best practices such as state management (`.tfstate`) and secure credential handling.

---

## 🐳 Docker & Networking (Questions 1 & 2)

### Q1. Understanding Docker First Run
Checked the `pip` version in the `python:3.12.8` image by running it in interactive mode with `bash` as the entrypoint.
### Q1. Understanding Docker First Run
To check the `pip` version in the `python:3.12.8` image, I executed the container in interactive mode with `bash` as the entrypoint.

**Command:**
```bash
docker run -it --entrypoint bash python:3.12.8

Inside the container:

Bash
pip --version
Result: pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)


> **Answer:** `24.3.1`

### Q2. Understanding Docker Networking
Hostname and port used by `pgadmin` to connect to the PostgreSQL database within the same Docker network.
> **Answer:** `db:5432`

---

## 📊 SQL Data Analysis (Questions 3 - 6)

All detailed analysis queries are documented in the [homework_1_solution.sql](./homework_1_solution.sql) file.

* **Q3. Trip Segmentation Count**: `104,802; 198,924; 109,603; 27,678; 35,189`
* **Q4. Longest Trip for Each Day**: `2019-10-31`
* **Q5. Three Biggest Pickup Zones**: `East Harlem North, East Harlem South, Morningside Heights`
* **Q6. Largest Tip (Pickup: East Harlem North)**: `JFK Airport`

---

## 🏗️ Terraform (Question 7)

### Q7. Terraform Workflow Sequence
1. Initialize & Download Plugins: `terraform init`
2. Generate plan & Auto-execute: `terraform apply -auto-approve`
3. Remove all managed resources: `terraform destroy`
> **Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

---

## 💡 Engineering Best Practices
* **Security**: Used `.gitignore` to prevent sensitive data like GCP Service Account keys (`.json`) and Terraform state files (`.tfstate`) from being pushed to the public repository.
* **Standardization**: Applied `terraform fmt` to maintain clean, industry-standard HCL code.
* **Automation**: Proactively implemented a Kestra-based orchestration pipeline to move beyond manual data ingestion.