# Data Types & Sources Overview

Data comes in different formats, structures, and storage methods, each serving unique use cases. Below is a breakdown of key concepts related to data types and storage solutions.

## 1. Data Types

### **Structured Data**
- Well-organized, formatted data stored in a tabular form (rows & columns).
- Managed using **Relational Database Management Systems (RDBMS)** such as MySQL, PostgreSQL, and SQL Server.
- Supports **SQL queries** for efficient data retrieval and manipulation.

**Examples:**
- Customer records in an SQL database
- Financial transactions stored in tables

### **Semi-Structured Data**
- Contains both structured and unstructured elements.
- Lacks a fixed schema but follows some organization for easier processing.
- Commonly used in **Big Data** and **NoSQL** databases.

**Examples & Formats:**
- JSON (JavaScript Object Notation)
- XML (Extensible Markup Language)
- Avro (Apache data serialization system)
- Parquet (Optimized columnar storage format for analytics)

### **Unstructured Data**
- Does not follow a predefined format or schema.
- Typically large-scale, raw data requiring specialized processing techniques.
- Stored in **data lakes**, distributed storage systems, or object repositories.

**Examples:**
- Text files, emails, and documents
- Multimedia (images, videos, audio)
- Log files from applications and servers

## 2. Data Storage Solutions

### **Data Lake**
- **Centralized repository** for storing raw, structured, semi-structured, and unstructured data.
- Allows flexible data ingestion for later analysis or processing.
- Often built on **cloud platforms** (e.g., AWS S3, Azure Data Lake, Google Cloud Storage).

**Key Benefits:**
- Stores massive volumes of raw data
- Supports real-time and batch processing
- Ideal for AI/ML workloads and analytics

### **Data Warehouse**
- Optimized **structured storage** for fast querying and reporting.
- Stores **processed & refined** data for business intelligence (BI) and analytics.
- Typically uses **columnar storage** for efficient querying.

**Examples:**
- Amazon Redshift
- Google BigQuery
- Snowflake
- Teradata

### **OLTP (Online Transaction Processing)**
- Designed to handle **frequent, real-time transactions** efficiently.
- Used in **banking, retail, and order processing systems**.
- Requires **high availability** and **strong consistency**.

**Examples:**
- ATM transactions
- E-commerce purchases
- Inventory management systems

### **OLAP (Online Analytical Processing)**
- Used for **complex queries, reporting, and business analytics**.
- Stores historical and aggregated data for **decision-making**.
- Supports **multi-dimensional analysis (data cubes)**.

**Examples:**
- Financial forecasting
- Customer behavior analytics
- Business intelligence dashboards

# Data Processing Overview

Data processing involves transforming raw data into meaningful insights using different methodologies. Below are the key concepts related to data processing techniques.

## 1. ETL (Extract, Transform, Load)
- **Extract**: Data is pulled from various sources (databases, APIs, logs, etc.).
- **Transform**: Data is cleaned, enriched, and structured for analysis.
- **Load**: The processed data is stored in a **data warehouse** or **database**.

### **Example Workflow:**
1. Extract customer records from an SQL database.
2. Transform records by normalizing data and handling missing values.
3. Load the transformed data into an analytics database.

**Common ETL Tools:**
- Apache NiFi
- Talend
- Informatica
- Microsoft SQL Server Integration Services (SSIS)

## 2. ELT (Extract, Load, Transform)
- A modern variation of ETL optimized for **cloud-based data pipelines**.
- The raw data is **loaded first** into a **data lake**, then transformed as needed.
- Supports large-scale analytics with **distributed processing**.

**Advantages Over ETL:**
- Faster ingestion since no transformation occurs before storage.
- Leverages cloud-native processing (e.g., BigQuery, Snowflake).

## 3. Batch Processing
- **Processes data in large chunks** instead of real-time streaming.
- Suitable for **scheduled workloads**, such as daily financial reports.

### **Example Technologies:**
- **Apache Spark** – Distributed batch data processing.
- **Hadoop MapReduce** – Parallelized data computation.

**Use Cases:**
- Large-scale database backups.
- Generating monthly sales reports.
- Data aggregation for machine learning.

## 4. Stream Processing
- Processes **continuous real-time data streams** instead of waiting for batches.
- Used for **event-driven applications** where latency is critical.

### **Example Technologies:**
- **Apache Kafka** – Event-streaming platform for real-time messaging.
- **Apache Flink** – Distributed stream processing engine.
- **Apache Storm** – Real-time processing framework.

**Use Cases:**
- Fraud detection in banking transactions.
- Monitoring social media trends.
- IoT sensor data processing.

## 5. Data Ingestion
- The process of **collecting data** from multiple sources into a central repository.
- Sources may include databases, APIs, logs, files, and external services.

### **Types of Data Ingestion:**
- **Batch ingestion** – Periodic extraction of data (e.g., nightly syncs).
- **Stream ingestion** – Continuous data feed (e.g., real-time stock prices).

**Common Data Ingestion Tools:**
- Apache Kafka
- AWS Kinesis
- Google Pub/Sub

## 6. Data Orchestration
- Automates **workflow execution** and data dependencies.
- Ensures that data processing tasks **run efficiently** in the correct order.

### **Example Technology:**
- **Apache Airflow** – Workflow automation and scheduling.
- **Luigi** – Job pipeline management.
- **Prefect** – Cloud-native workflow orchestration.

**Use Cases:**
- Running ETL jobs at scheduled intervals.
- Coordinating multiple machine learning pipelines.
- Managing dependencies in analytics workflows.

# Storage & Formats Overview

Data storage involves different architectures and formats optimized for specific use cases. Below is a breakdown of key storage methods and data formats.

## 1. Columnar Storage
- Stores data **column by column** instead of row by row.
- Optimized for **analytical queries** where operations (aggregations, filtering) focus on specific columns.
- Provides **higher compression** and **faster retrieval** compared to row-based storage.

### **Common Columnar Formats:**
- **Parquet** – Highly efficient for big data & analytics (Apache Hadoop, Spark).
- **ORC (Optimized Row Columnar)** – Best suited for Hive-based data warehouses.

**Use Cases:**
- Business intelligence (BI) and analytics workloads.
- Data warehousing for large-scale reporting.

## 2. Row-based Storage
- Stores data **record by record (row-wise)**, making it efficient for transactional operations.
- Best suited for **frequent inserts, updates, and deletions**.

### **Common Row-based Formats:**
- **CSV (Comma-Separated Values)** – Simple, human-readable but not optimized for large-scale querying.
- **JSON (JavaScript Object Notation)** – Widely used for APIs and NoSQL databases.
- **Traditional databases** (MySQL, PostgreSQL, SQL Server) store data row-wise.

**Use Cases:**
- Online transaction processing (OLTP) applications.
- Real-time user interactions (e.g., banking systems, e-commerce platforms).

## 3. Distributed File System
- Designed to store **large-scale distributed data** across multiple nodes.
- Enables parallel processing for **big data analytics**.

### **Common Distributed File Systems:**
- **HDFS (Hadoop Distributed File System)** – Core storage system for Hadoop ecosystem.
- **Amazon S3** – Cloud-based object storage for scalable data management.
- **Azure Blob Storage** – Microsoft's solution for unstructured data storage.

**Use Cases:**
- Big data processing and machine learning workloads.
- Storing backups and large datasets in a cloud or cluster environment.

## 4. Data Partitioning
- **Divides large datasets** into smaller subsets for efficient querying and processing.
- Each partition is stored separately, improving performance in **distributed systems**.

### **Types of Partitioning:**
- **Range Partitioning** – Splits data based on a range of values (e.g., date-based partitions).
- **List Partitioning** – Divides data based on predefined categories (e.g., country codes).
- **Hash Partitioning** – Distributes data using hash functions for even load balancing.

**Use Cases:**
- Data lakes and large databases with high read/query performance needs.
- Cloud-based storage systems to speed up query execution.

## 5. Data Sharding
- **Splits large databases** into smaller, more manageable parts called **shards**.
- Improves **scalability and performance** in distributed applications.

### **Sharding Techniques:**
- **Horizontal Sharding** – Splits rows across multiple databases.
- **Vertical Sharding** – Segments tables by column-based distribution.
- **Geographical Sharding** – Stores data based on **regional proximity** (e.g., nearest servers).

**Use Cases:**
- High-traffic applications like social media platforms.
- Large-scale multi-tenant databases requiring independent partitions.



