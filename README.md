 # AtmoSync – Micro-Climate Arbitrage Analytics

## 1. Project Overview

AtmoSync is a data engineering and analytics project designed to monitor environmental conditions inside transportation containers carrying perishable goods.

The system collects sensor readings such as temperature, humidity, and vibration. It aims to combine this information with historical market prices to estimate spoilage risk and identify potential market opportunities.

## 2. Project Objectives

- Monitor environmental conditions inside transportation containers.
- Generate simulated IoT sensor readings.
- Stream sensor data using Apache Kafka.
- Store and manage sensor readings in databases.
- Analyze historical avocado market prices.
- Develop spoilage-risk and market-opportunity analytics.
- Build dashboards for monitoring and visualization.

## 3. Technologies Used

- **Python:** Sensor simulation and data processing.
- **Apache Kafka:** Real-time data streaming.
- **PostgreSQL:** Local storage of sensor readings.
- **Snowflake:** Cloud data warehouse.
- **dbt Core:** Planned data transformation.
- **Apache Superset:** Planned dashboard development.
- **Git and GitHub:** Version control and project collaboration.
- **VS Code:** Development environment.

## 4. Work Completed So Far

### 4.1 GitHub Setup
- Created the AtmoSync GitHub repository.
- Configured the local project environment.
- Added project folders and documentation.
- Committed and pushed project changes.

### 4.2 IoT Sensor Simulation
- Created a Python sensor simulator.
- Generated simulated container sensor readings.
- Included temperature, humidity, vibration, container ID, and timestamp fields.

### 4.3 Apache Kafka Setup
- Installed and configured Apache Kafka.
- Started the Kafka broker.
- Created the `container-sensor-data` topic.
- Installed the Python Kafka client.
- Developed and tested a Kafka producer that sends simulated sensor readings.

### 4.4 PostgreSQL Integration
- Installed the PostgreSQL Python connector.
- Created the `atmosync_db` database.
- Created the `sensor_readings` table.
- Developed a Kafka consumer to receive sensor messages and insert them into PostgreSQL.
- Verified that sensor records were being stored successfully.

### 4.5 Snowflake Setup
- Created a Snowflake account.
- Created the `ATMOSYNC_DB` database.
- Created the `RAW` schema.
- Created the `SENSOR_READINGS` table.
- Inserted and verified a sample sensor record.
- Installed the Snowflake Python connector.

**Current status:** Python-to-Snowflake authentication is still being configured. Google sign-in works through the browser, but the Python connector connection has encountered an authentication issue.

## 5. Database Structure

The sensor readings table contains:

| Column | Description |
|---|---|
| ID | Unique record identifier |
| CONTAINER_ID | Container identification |
| RECORDED_AT | Reading timestamp |
| TEMPERATURE_C | Temperature in Celsius |
| HUMIDITY_PERCENT | Humidity percentage |
| VIBRATION_G | Vibration measurement |

## 6. Project Architecture

Current implemented flow:

Python Sensor Producer → Apache Kafka → Kafka Consumer → PostgreSQL

Planned cloud integration:

Apache Kafka → Snowflake → dbt Core → Apache Superset

## 7. Pending Work

- Complete secure Snowflake authentication.
- Establish Python connectivity with Snowflake.
- Integrate Kafka sensor data with Snowflake.
- Configure dbt models and transformations.
- Develop the Apache Superset dashboard.
- Implement spoilage-risk analysis.
- Integrate market-price analysis.
- Develop time-to-spoilage versus distance-to-market analysis.
- Perform end-to-end testing and documentation.

## 8. Expected Project Outcome

AtmoSync aims to provide an analytics platform that connects transportation conditions with market intelligence. It will help identify potential spoilage risks and evaluate whether goods can reach suitable markets before their quality deteriorates.

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Development Status:** In Progress