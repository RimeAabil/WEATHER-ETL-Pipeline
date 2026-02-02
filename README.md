# 🌦️ End-to-End Weather ETL & Analytics Pipeline

## 📖 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Detailed Tech Stack](#detailed-tech-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Component Deep Dive](#component-deep-dive)
- [Usage Guide](#usage-guide)
- [Data Flow Explanation](#data-flow-explanation)
- [Airflow DAG Details](#airflow-dag-details)
- [dbt Models & Transformations](#dbt-models--transformations)
- [Dashboard Creation](#dashboard-creation)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 Overview

This project represents a production-ready, end-to-end Data Engineering solution that automates the complete lifecycle of weather data analytics. From ingestion through transformation to visualization, this pipeline demonstrates modern data engineering best practices using industry-standard tools.

### What This Project Does

The pipeline continuously collects weather data from multiple global cities using the WeatherStack API, stores it in a structured PostgreSQL data warehouse, transforms and models it using dbt (Data Build Tool), and presents it through interactive Apache Superset dashboards. All of this is orchestrated and monitored by Apache Airflow, ensuring reliable, scheduled execution with full observability.

### Business Value

Weather data analytics has wide-ranging applications including:
- **Retail & Supply Chain**: Inventory planning based on weather patterns
- **Agriculture**: Crop monitoring and yield prediction
- **Energy**: Demand forecasting for utilities
- **Insurance**: Risk assessment and claims prediction
- **Tourism & Hospitality**: Resource allocation and marketing timing
- **Transportation**: Route optimization and safety planning

### Technical Goals

This project demonstrates mastery of:
- **ETL/ELT Pipeline Design**: Building scalable data ingestion workflows
- **Data Warehousing**: Schema design, data modeling, and optimization
- **Data Transformation**: SQL-based transformation with version control and testing
- **Workflow Orchestration**: Scheduling, dependency management, and error handling
- **Business Intelligence**: Creating actionable insights through visualization
- **DevOps for Data**: Containerization, infrastructure as code, and automation

---

## 🎯 Key Features

### Automated Data Collection
- **Scheduled Ingestion**: Configurable intervals (hourly, daily, or custom) for data collection
- **Multi-City Support**: Collect data from unlimited geographic locations simultaneously
- **Error Handling**: Automatic retries with exponential backoff for API failures
- **Data Validation**: Schema validation before database insertion to ensure data quality

### Robust Data Storage
- **Dual-Schema Architecture**: Separation of raw and analytics data for flexibility
- **Data Lineage**: Complete audit trail from source to final dashboard
- **Persistence**: Docker volumes ensure data survives container restarts
- **Backup Ready**: Standard PostgreSQL backup procedures apply

### Intelligent Transformation
- **SQL-Based Models**: Version-controlled transformations using dbt
- **Data Quality Tests**: Automated checks for null values, duplicates, and data integrity
- **Incremental Processing**: Efficient processing of only new/changed data
- **Documentation**: Auto-generated data catalog with column-level lineage

### Production-Grade Orchestration
- **Visual DAG Management**: Web-based interface for monitoring pipeline health
- **SLA Monitoring**: Alerts for missed execution windows
- **Task Dependencies**: Ensures correct execution order with failure isolation
- **Logging**: Comprehensive logs for debugging and auditing

### Interactive Analytics
- **Real-Time Dashboards**: Live data exploration with drill-down capabilities
- **Custom Metrics**: Create calculated fields without touching the database
- **Multi-Format Export**: Share insights via PDF, CSV, or email
- **Role-Based Access**: Control who can view or edit specific dashboards

---

## 🏗️ Architecture

### High-Level Architecture Diagram

**Tools & Components Overview**
![Project Architecture and Data Pipeline](assets/weather-pipeline-architecture.jpg)

### Data Flow Architecture

```mermaid
graph TB
    %% Data Source
    API[("☁️ WeatherStack API<br/><small>External Data Source</small>")]
    
    %% Ingestion Layer
    Python["🐍 Python Ingestion Script<br/><small>Data Collection & Loading</small>"]
    
    %% Storage Layers
    Raw[("📦 PostgreSQL<br/>Raw Schema<br/><small>Staging Data</small>")]
    Analytics[("📊 PostgreSQL<br/>Analytics Schema<br/><small>Transformed Data</small>")]
    
    %% Transformation
    DBT["⚙️ dbt Transformation<br/><small>Data Modeling & Quality</small>"]
    
    %% Visualization
    Superset["📈 Apache Superset<br/><small>Dashboards & Analytics</small>"]
    
    %% Orchestration
    Airflow["🔄 Apache Airflow<br/><small>Workflow Orchestration</small>"]
    
    %% Process Explanations
    Step1["📥 STEP 1: EXTRACT<br/>Fetch current weather data<br/>via HTTP requests"]
    Step2["💾 STEP 2: LOAD<br/>Store raw JSON/data as-is<br/>with timestamps"]
    Step3["🔄 STEP 3: TRANSFORM<br/>Clean, aggregate & model<br/>Apply business logic"]
    Step4["📊 STEP 4: ANALYZE<br/>Create charts & dashboards<br/>Monitor weather trends"]
    Step5["⏰ ORCHESTRATION<br/>Schedule daily runs<br/>Handle failures & alerts"]
    
    %% Data Flow
    API -->|REST API Call| Python
    Python -->|Bulk Insert| Raw
    Raw -->|Source Tables| DBT
    DBT -->|Marts & Models| Analytics
    Analytics -->|SQL Queries| Superset
    
    %% Orchestration Flow
    Airflow -.->|Schedule & Monitor| Python
    Airflow -.->|Schedule & Monitor| DBT
    
    %% Explanations positioning
    Step1 -.-> Python
    Step2 -.-> Raw
    Step3 -.-> DBT
    Step4 -.-> Superset
    Step5 -.-> Airflow
    
    %% Styling
    classDef source fill:#e1f5ff,stroke:#0288d1,stroke-width:2px,color:#000
    classDef process fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
    classDef storage fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000
    classDef viz fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000
    classDef orchestration fill:#fff9c4,stroke:#f9a825,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    classDef explanation fill:#fafafa,stroke:#757575,stroke-width:1px,color:#000,stroke-dasharray: 3 3
    
    class API source
    class Python,DBT process
    class Raw,Analytics storage
    class Superset viz
    class Airflow orchestration
    class Step1,Step2,Step3,Step4,Step5 explanation
```

### Architecture Philosophy

The pipeline follows the **ELT (Extract, Load, Transform)** pattern rather than traditional ETL:

1. **Extract**: Pull raw data from the API without any transformation
2. **Load**: Store the data exactly as received in the raw schema
3. **Transform**: Apply business logic and transformations within the database using SQL

This approach offers several advantages:
- **Data Preservation**: Raw data is always available for reprocessing
- **Flexibility**: Change transformation logic without re-extracting data
- **Performance**: Leverage database optimization for transformations
- **Auditability**: Clear separation between source data and derived data

---

## 🛠️ Detailed Tech Stack

### Core Components

| Component | Technology | Version | Purpose | Why This Tool? |
|-----------|-----------|---------|---------|----------------|
| **Orchestrator** | Apache Airflow | 2.10.x | Workflow scheduling and monitoring | Industry standard for data pipeline orchestration, provides visual DAG management and robust error handling |
| **Data Warehouse** | PostgreSQL | 15.x | Relational data storage | Open-source, ACID-compliant, excellent performance for analytical workloads, wide ecosystem support |
| **Transformation** | dbt-core | 1.9.x | SQL-based data modeling | Version-controlled transformations, built-in testing framework, automatic documentation generation |
| **BI Platform** | Apache Superset | 3.0.x | Data visualization and dashboarding | Modern, feature-rich alternative to commercial BI tools, supports complex visualizations and SQL Lab |
| **Message Broker** | Redis | 7.x | Caching and task queue | Used by Superset for async queries and Airflow for distributed task execution |
| **Container Runtime** | Docker & Docker Compose | Latest | Containerization and orchestration | Ensures consistent environments across development and production, simplifies deployment |
| **Programming Language** | Python | 3.10+ | Pipeline scripting | Versatile, extensive libraries for data engineering, widely adopted in the industry |

### Python Dependencies Explained

**Core Libraries**:
- `requests==2.31.0`: HTTP library for making API calls to WeatherStack
- `psycopg2-binary==2.9.9`: PostgreSQL adapter for Python, enables database operations
- `python-dotenv==1.0.0`: Loads environment variables from .env files for secure configuration management
- `apache-airflow[postgres,redis]==2.10.2`: Core Airflow with PostgreSQL and Redis support
- `dbt-core==1.9.0`: Core dbt engine for transformations
- `dbt-postgres==1.9.0`: PostgreSQL adapter for dbt

**Development Tools**:
- `pytest==7.4.3`: Testing framework for Python code
- `black==23.12.1`: Code formatter for consistent styling
- `flake8==7.0.0`: Linting tool for code quality checks

**Airflow Providers**:
- `apache-airflow-providers-postgres`: Operators for PostgreSQL tasks in Airflow
- `apache-airflow-providers-http`: HTTP operators for API interactions

---

## 📋 Prerequisites

### System Requirements

**Minimum Hardware**:
- CPU: 2 cores
- RAM: 8 GB
- Storage: 20 GB free space
- Network: Stable internet connection for API calls

**Recommended Hardware**:
- CPU: 4+ cores
- RAM: 16 GB
- Storage: 50 GB SSD
- Network: High-speed broadband

### Required Software

1. **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
   - Version 20.10 or higher
   - Docker Compose V2 included
   - Download: https://docs.docker.com/get-docker/

2. **Git** (for version control)
   - Version 2.0 or higher
   - Download: https://git-scm.com/downloads

3. **Text Editor/IDE** (recommended)
   - VS Code with Python and Docker extensions
   - PyCharm
   - Or any editor of your choice

### API Requirements

**WeatherStack API Key**:
- Sign up at: https://weatherstack.com/signup/free
- Free tier includes:
  - 1,000 API calls per month
  - Current weather data
  - Multiple locations
- Paid tiers available for higher limits and historical data

### Knowledge Prerequisites

**Recommended Knowledge**:
- Basic understanding of SQL
- Familiarity with command line/terminal
- Basic Docker concepts (containers, volumes, networks)
- Understanding of REST APIs
- Basic Python (helpful but not required)

**Learning Resources**:
- Docker: https://docs.docker.com/get-started/
- SQL: https://www.w3schools.com/sql/
- Airflow: https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html
- dbt: https://docs.getdbt.com/docs/introduction

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
# Clone the project
git clone https://github.com/RimeAabil/WEATHER-ETL-Pipeline.git

# Navigate to project directory
cd WEATHER-ETL-Pipeline

# Verify files
ls -la
```

**What you should see**:
- `docker-compose.yml`: Defines all services and their configurations
- `.env.example`: Template for environment variables
- `airflow/`: Contains DAGs and Airflow configurations
- `dbt/`: Contains dbt project and models
- `api-request/`: Python scripts for data ingestion
- `postgres/`: Database initialization scripts

### Step 2: Configure Environment Variables

Environment variables store sensitive configuration data outside of your code.

```bash
# Copy the example file
cp .env.example .env

# Edit the file with your favorite editor
nano .env
# or
vim .env
# or open in VS Code
code .env
```

**Required Variables**:

```env
# ==========================================
# API Configuration
# ==========================================
# Your WeatherStack API key (get from weatherstack.com)
WEATHER_STACK_API=your_api_key_here

# WeatherStack API endpoint (do not change unless using enterprise)
API_URL=http://api.weatherstack.com/current

# Locations to fetch weather data for (comma-separated)
CITIES=New York,London,Tokyo,Sydney,Paris,Dubai,Singapore

# ==========================================
# PostgreSQL Database Configuration
# ==========================================
# Database credentials
POSTGRES_USER=weather_admin
POSTGRES_PASSWORD=StrongPassword123!
POSTGRES_DB=weather_db

# Connection details (these match docker-compose.yml)
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ==========================================
# Airflow Configuration
# ==========================================
# Airflow web UI credentials
AIRFLOW_ADMIN_USERNAME=admin
AIRFLOW_ADMIN_PASSWORD=admin

# Airflow executor (LocalExecutor for single machine)
AIRFLOW_EXECUTOR=LocalExecutor

# Airflow database connection
AIRFLOW_DATABASE_URL=postgresql+psycopg2://weather_admin:StrongPassword123!@postgres:5432/weather_db

# ==========================================
# Superset Configuration
# ==========================================
# Superset admin credentials
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=admin
SUPERSET_ADMIN_EMAIL=admin@superset.com

# Redis configuration for Superset
REDIS_HOST=redis
REDIS_PORT=6379

# ==========================================
# dbt Configuration
# ==========================================
# These should match your PostgreSQL settings
DBT_POSTGRES_HOST=postgres
DBT_POSTGRES_PORT=5432
DBT_POSTGRES_USER=weather_admin
DBT_POSTGRES_PASSWORD=StrongPassword123!
DBT_POSTGRES_DB=weather_db
DBT_POSTGRES_SCHEMA=analytics
```

**Security Best Practices**:
- Never commit `.env` to Git (already in `.gitignore`)
- Use strong passwords in production
- Rotate credentials regularly
- Use different passwords for each service

### Step 3: Initialize Docker Environment

Docker Compose will build and start all services defined in `docker-compose.yml`.

```bash
# Build and start all containers in detached mode
docker-compose up -d --build

# What this does:
# --build: Rebuilds images if Dockerfiles have changed
# -d: Runs containers in background (detached mode)
# This process may take 5-10 minutes on first run
```

**Expected Output**:
```
[+] Building 45.2s (23/23) FINISHED
[+] Running 7/7
 ✔ Network weather-etl_default      Created
 ✔ Container postgres               Started
 ✔ Container redis                  Started
 ✔ Container airflow-init           Started
 ✔ Container airflow-webserver      Started
 ✔ Container airflow-scheduler      Started
 ✔ Container dbt                    Started
 ✔ Container superset               Started
```

**Verify Container Status**:
```bash
# Check all containers are running
docker-compose ps

# Expected output: All containers should show "Up" status
# If any show "Exit" or "Restarting", check logs
```

**Common Issues During Startup**:

1. **Port Already in Use**:
   ```
   Error: Bind for 0.0.0.0:8080 failed: port is already allocated
   ```
   Solution: Stop the conflicting service or change port in `docker-compose.yml`

2. **Insufficient Memory**:
   ```
   Container killed due to OOM
   ```
   Solution: Increase Docker memory allocation in Docker Desktop settings

3. **Permission Denied**:
   ```
   Permission denied while trying to connect to Docker daemon
   ```
   Solution: Add user to docker group or run with sudo (Linux)

### Step 4: Initialize Airflow Database

Airflow requires database initialization before first use.

```bash
# Initialize Airflow metadata database
docker exec -it airflow-webserver airflow db init

# Create admin user (if not created via docker-compose)
docker exec -it airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### Step 5: Verify Installation

**Check Docker Logs**:
```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs airflow-webserver
docker-compose logs postgres
docker-compose logs dbt
docker-compose logs superset

# Follow logs in real-time (Ctrl+C to exit)
docker-compose logs -f airflow-scheduler
```

**Access Web Interfaces**:

1. **Airflow**: http://localhost:8080
   - Username: admin
   - Password: admin
   - You should see the DAGs page with your weather pipeline

2. **Superset**: http://localhost:8088
   - Username: admin
   - Password: admin
   - You should see the Superset home page

**Test Database Connection**:
```bash
# Access PostgreSQL container
docker exec -it postgres psql -U weather_admin -d weather_db

# List all schemas
\dn

# You should see:
# dev (for raw data)
# analytics (for transformed data)

# Exit psql
\q
```

---

## 📁 Project Structure

Understanding the project structure helps with navigation and customization.

```
WEATHER-ETL-Pipeline/
│
├── 📄 docker-compose.yml          # Orchestrates all Docker containers
├── 📄 .env                        # Environment variables (not in Git)
├── 📄 .env.example                # Template for .env
├── 📄 .gitignore                  # Files to exclude from Git
├── 📄 README.md                   # This file
├── 📄 LICENSE                     # Project license
│
├── 📂 airflow/                    # Apache Airflow configuration
│   ├── 📂 dags/                   # DAG definitions
│   │   ├── 📄 orchestrator.py     # Main pipeline DAG
│   │   └── 📄 __init__.py
│   ├── 📂 logs/                   # Airflow execution logs
│   ├── 📂 plugins/                # Custom Airflow plugins
│   └── 📄 airflow.cfg             # Airflow configuration
│
├── 📂 api-request/                # Data ingestion scripts
│   ├── 📄 api.py                  # API client for WeatherStack
│   ├── 📄 insert_record.py        # Database insertion logic
│   ├── 📄 config.py               # Configuration management
│   └── 📄 requirements.txt        # Python dependencies
│
├── 📂 dbt/                        # dbt transformation project
│   ├── 📂 weather_project/        # Main dbt project
│   │   ├── 📂 models/             # SQL transformation models
│   │   │   ├── 📂 staging/        # Staging models (clean raw data)
│   │   │   │   └── 📄 stg_weather.sql
│   │   │   ├── 📂 marts/          # Business logic models
│   │   │   │   ├── 📄 daily_weather_summary.sql
│   │   │   │   └── 📄 weather_report.sql
│   │   │   └── 📄 schema.yml     # Model documentation & tests
│   │   ├── 📂 tests/              # Custom dbt tests
│   │   ├── 📂 macros/             # Reusable SQL functions
│   │   ├── 📄 dbt_project.yml     # dbt project configuration
│   │   └── 📄 profiles.yml        # Database connection profiles
│   └── 📄 requirements.txt        # dbt dependencies
│
├── 📂 postgres/                   # PostgreSQL initialization
│   ├── 📄 init.sql                # Schema and table creation
│   └── 📂 data/                   # Database volume (not in Git)
│
├── 📂 docker/                     # Docker-related configurations
│   ├── 📂 airflow/                # Airflow Dockerfile
│   ├── 📂 dbt/                    # dbt Dockerfile
│   ├── 📂 superset/               # Superset configuration
│   │   ├── 📄 superset_config.py  # Superset settings
│   │   └── 📄 docker-bootstrap.sh # Initialization script
│   └── 📂 postgres/               # PostgreSQL Dockerfile
│
├── 📂 assets/                     # Documentation assets
│   └── 📄 weather-pipeline-architecture.jpg
│
└── 📂 tests/                      # Integration tests
    └── 📄 test_pipeline.py        # End-to-end tests
```

### Key Files Explained

**docker-compose.yml**:
- Defines 6 services: postgres, redis, airflow-webserver, airflow-scheduler, dbt, superset
- Configures networks, volumes, and environment variables
- Sets up service dependencies (e.g., Airflow waits for Postgres)

**airflow/dags/orchestrator.py**:
- Defines the DAG (Directed Acyclic Graph)
- Sets schedule interval (e.g., daily at midnight)
- Chains tasks: ingestion → dbt transformation → data quality checks

**api-request/insert_record.py**:
- Main ingestion script
- Fetches data from WeatherStack API
- Validates and inserts into PostgreSQL raw schema
- Handles errors and retries

**dbt/weather_project/models/**:
- Contains SQL files that transform raw data
- Staging models clean and standardize raw data
- Marts models apply business logic and create reporting tables

**postgres/init.sql**:
- Runs on first database startup
- Creates schemas (dev, analytics)
- Creates initial tables
- Sets up indexes for performance

---

## 🔧 Component Deep Dive

### 1. Data Ingestion Layer (Python + WeatherStack API)

**Purpose**: Extract weather data from external API and load into database.

**How It Works**:

The ingestion process follows these steps:

1. **Configuration Loading**:
   ```python
   # config.py
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   API_KEY = os.getenv('WEATHER_STACK_API')
   API_URL = os.getenv('API_URL')
   CITIES = os.getenv('CITIES', '').split(',')
   ```

2. **API Request**:
   ```python
   # api.py
   import requests
   
   def fetch_weather(city):
       """Fetch current weather for a city"""
       params = {
           'access_key': API_KEY,
           'query': city,
           'units': 'm'  # metric units
       }
       
       response = requests.get(API_URL, params=params)
       response.raise_for_status()
       
       return response.json()
   ```

3. **Data Validation**:
   ```python
   def validate_weather_data(data):
       """Ensure required fields exist"""
       required_fields = ['location', 'current', 'request']
       
       for field in required_fields:
           if field not in data:
               raise ValueError(f"Missing required field: {field}")
       
       return True
   ```

4. **Database Insertion**:
   ```python
   # insert_record.py
   import psycopg2
   
   def insert_weather_record(data):
       """Insert weather data into PostgreSQL"""
       conn = psycopg2.connect(
           host=os.getenv('POSTGRES_HOST'),
           database=os.getenv('POSTGRES_DB'),
           user=os.getenv('POSTGRES_USER'),
           password=os.getenv('POSTGRES_PASSWORD')
       )
       
       with conn.cursor() as cur:
           cur.execute("""
               INSERT INTO dev.weather_raw 
               (city, temperature, humidity, wind_speed, 
                weather_description, observation_time, fetched_at)
               VALUES (%s, %s, %s, %s, %s, %s, NOW())
           """, (
               data['location']['name'],
               data['current']['temperature'],
               data['current']['humidity'],
               data['current']['wind_speed'],
               data['current']['weather_descriptions'][0],
               data['current']['observation_time']
           ))
       
       conn.commit()
       conn.close()
   ```

**Error Handling**:

The script implements robust error handling:

```python
def fetch_and_store_weather():
    """Main function with error handling"""
    cities = CITIES
    
    for city in cities:
        try:
            # Fetch data
            data = fetch_weather(city)
            
            # Validate
            validate_weather_data(data)
            
            # Store
            insert_weather_record(data)
            
            logging.info(f"Successfully stored weather for {city}")
            
        except requests.RequestException as e:
            logging.error(f"API error for {city}: {e}")
            # Don't raise - continue with other cities
            
        except psycopg2.Error as e:
            logging.error(f"Database error for {city}: {e}")
            # This is more serious - may want to raise
            
        except Exception as e:
            logging.error(f"Unexpected error for {city}: {e}")
```

**Why This Approach?**:
- **Separation of Concerns**: API logic, validation, and database operations are separate
- **Resilience**: Failures for one city don't affect others
- **Observability**: Comprehensive logging for debugging
- **Testability**: Each function can be unit tested independently

### 2. Storage Layer (PostgreSQL)

**Purpose**: Provide reliable, structured storage for both raw and transformed data.

**Schema Design**:

The database uses a two-schema approach:

**Dev Schema (Raw Data)**:
```sql
CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE dev.weather_raw (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2),
    humidity INTEGER,
    wind_speed DECIMAL(5,2),
    weather_description VARCHAR(255),
    observation_time TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT temperature_range CHECK (temperature BETWEEN -100 AND 100),
    CONSTRAINT humidity_range CHECK (humidity BETWEEN 0 AND 100)
);

-- Indexes for performance
CREATE INDEX idx_weather_raw_city ON dev.weather_raw(city);
CREATE INDEX idx_weather_raw_fetched ON dev.weather_raw(fetched_at);
CREATE INDEX idx_weather_raw_observation ON dev.weather_raw(observation_time);
```

**Why These Indexes?**:
- `idx_weather_raw_city`: Fast filtering by city
- `idx_weather_raw_fetched`: Efficient time-based queries
- `idx_weather_raw_observation`: Sorting by observation time

**Analytics Schema (Transformed Data)**:
```sql
CREATE SCHEMA IF NOT EXISTS analytics;

-- This table is created by dbt
CREATE TABLE analytics.weather_report (
    report_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    avg_temperature DECIMAL(5,2),
    avg_humidity DECIMAL(5,2),
    avg_wind_speed DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    observation_date DATE,
    record_count INTEGER,
    last_updated TIMESTAMP DEFAULT NOW()
);
```

**Data Types Explained**:
- `SERIAL`: Auto-incrementing integer for primary keys
- `VARCHAR(n)`: Variable-length string with max length
- `DECIMAL(p,s)`: Fixed-precision decimal (p=precision, s=scale)
- `INTEGER`: Whole numbers
- `TIMESTAMP`: Date and time with microsecond precision
- `DATE`: Date only (no time component)

**Performance Considerations**:

1. **Partitioning** (for large datasets):
   ```sql
   -- Partition by month for better query performance
   CREATE TABLE dev.weather_raw_2024_01 
   PARTITION OF dev.weather_raw
   FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
   ```

2. **Vacuum & Analyze** (maintenance):
   ```sql
   -- Reclaim space and update statistics
   VACUUM ANALYZE dev.weather_raw;
   ```

3. **Connection Pooling** (in Python):
   ```python
   from psycopg2 import pool
   
   connection_pool = pool.SimpleConnectionPool(
       minconn=1,
       maxconn=10,
       host=POSTGRES_HOST,
       database=POSTGRES_DB,
       user=POSTGRES_USER,
       password=POSTGRES_PASSWORD
   )
   ```

### 3. Transformation Layer (dbt)

**Purpose**: Transform raw data into analytics-ready tables using SQL.

**dbt Project Structure**:

```yaml
# dbt_project.yml
name: 'weather_project'
version: '1.0.0'
config-version: 2

profile: 'weather_profile'

model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]

models:
  weather_project:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: analytics
```

**Configuration Explained**:
- `materialized: view`: Creates database views (lightweight, always fresh)
- `materialized: table`: Creates physical tables (faster queries, stale until rebuilt)
- `+schema`: Controls which schema models are created in

**Staging Models** (Clean Raw Data):

```sql
-- models/staging/stg_weather.sql
{{ config(
    materialized='view',
    schema='staging'
) }}

WITH source_data AS (
    SELECT
        id,
        city,
        temperature,
        humidity,
        wind_speed,
        weather_description,
        observation_time,
        fetched_at
    FROM {{ source('dev', 'weather_raw') }}
    WHERE fetched_at >= CURRENT_DATE - INTERVAL '7 days'
),

cleaned_data AS (
    SELECT
        id,
        TRIM(UPPER(city)) AS city,  -- Standardize city names
        ROUND(temperature::NUMERIC, 1) AS temperature,
        humidity,
        ROUND(wind_speed::NUMERIC, 1) AS wind_speed,
        weather_description,
        observation_time,
        fetched_at,
        -- Add derived fields
        CASE
            WHEN temperature < 0 THEN 'Freezing'
            WHEN temperature < 10 THEN 'Cold'
            WHEN temperature < 20 THEN 'Moderate'
            WHEN temperature < 30 THEN 'Warm'
            ELSE 'Hot'
        END AS temperature_category
    FROM source_data
    WHERE temperature IS NOT NULL
      AND humidity IS NOT NULL
)

SELECT * FROM cleaned_data
```

**Marts Models** (Business Logic):

```sql
-- models/marts/daily_weather_summary.sql
{{ config(
    materialized='table',
    schema='analytics'
) }}

SELECT
    city,
    DATE(observation_time) AS observation_date,
    COUNT(*) AS reading_count,
    ROUND(AVG(temperature)::NUMERIC, 1) AS avg_temperature,
    ROUND(AVG(humidity)::NUMERIC, 1) AS avg_humidity,
    ROUND(AVG(wind_speed)::NUMERIC, 1) AS avg_wind_speed,
    MAX(temperature) AS max_temperature,
    MIN(temperature) AS min_temperature,
    MODE() WITHIN GROUP (ORDER BY weather_description) AS most_common_weather
FROM {{ ref('stg_weather') }}
GROUP BY city, DATE(observation_time)
ORDER BY city, observation_date DESC
```

**Data Quality Tests**:

```yaml
# models/schema.yml
version: 2

sources:
  - name: dev
    database: weather_db
    schema: dev
    tables:
      - name: weather_raw
        description: "Raw weather data from WeatherStack API"
        columns:
          - name: id
            description: "Primary key"
            tests:
              - unique
              - not_null

models:
  - name: stg_weather
    description: "Cleaned and standardized weather data"
    columns:
      - name: id
        tests:
          - unique
          - not_null
      - name: city
        tests:
          - not_null
      - name: temperature
        tests:
          - not_null
          - accepted_range:
              min_value: -50
              max_value: 60

  - name: daily_weather_summary
    description: "Daily aggregated weather metrics by city"
    columns:
      - name: city
        tests:
          - not_null
      - name: observation_date
        tests:
          - not_null
      - name: avg_temperature
        tests:
          - not_null
```

**Running dbt**:

```bash
# Run all models
docker exec -it dbt_container dbt run \
    --project-dir /usr/app/dbt/weather_project \
    --profiles-dir /usr/app/dbt

# Run specific model
docker exec -it dbt_container dbt run \
    --select daily_weather_summary \
    --project-dir /usr/app/dbt/weather_project \
    --profiles-dir /usr/app/dbt

# Run tests
docker exec -it dbt_container dbt test \
    --project-dir /usr/app/dbt/weather_project \
    --profiles-dir /usr/app/dbt

# Generate documentation
docker exec -it dbt_container dbt docs generate \
    --project-dir /usr/app/dbt/weather_project \
    --profiles-dir /usr/app/dbt

# Serve documentation (accessible at http://localhost:8081)
docker exec -it dbt_container dbt docs serve \
    --project-dir /usr/app/dbt/weather_project \
    --profiles-dir /usr/app/dbt \
    --port 8081
```

**dbt Advantages**:
- **Version Control**: SQL transformations in Git
- **Testing**: Built-in data quality checks
- **Documentation**: Auto-generated data catalog
- **Lineage**: Visual representation of data flow
- **Modularity**: Reusable models via `ref()`

---

*Developed with ❤️ for the Data Engineering community*

*Last Updated: February 2, 2026*
