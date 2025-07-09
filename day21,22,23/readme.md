Data warehousing concepts revolve around creating a centralized, subject-oriented, integrated, time-variant, and non-volatile repository for data to support decision-making. Data modeling, in this context, is the process of designing this repository's structure, ensuring data is organized, stored, and accessed efficiently for analysis and reporting. 
Key concepts: 
Data Warehousing: 

• Definition: A data warehouse is a large, centralized repository of integrated data from various sources, designed for analytical and reporting purposes. 
• Key Characteristics: 
	• Subject-oriented: Focuses on a specific subject area (e.g., sales, marketing) rather than ongoing operations.  
	• Integrated: Combines data from multiple sources into a consistent format.  
	• Time-variant: Data includes historical information, allowing for time-based analysis.  
	• Non-volatile: Data is not updated in real-time; it's loaded periodically and remains static for analysis.  

• Components: 
	• Data Storage: Where the data is physically stored (e.g., database).   
	• ETL (Extract, Transform, Load): Processes to extract data from source systems, transform it into a usable format, and load it into the warehouse. 
	• Metadata: Data about the data, providing information about the structure, content, and usage of the warehouse.
	• Access Tools: Tools for querying, reporting, and analyzing data.  

• Types of Data Warehouses: 
	• Enterprise Data Warehouse (EDW): A large-scale warehouse serving the entire organization. 
	• Data Mart: A smaller, focused warehouse designed for a specific department or business unit.
	• Operational Data Store (ODS): Stores near real-time data for operational reporting and quick access.  

• Cloud Data Warehouses: Warehouses hosted on cloud platforms (e.g., AWS, Azure, Google Cloud).

Data Modeling: 

• Definition: The process of creating a visual representation of how data will be structured, stored, and accessed within the data warehouse.  
• Purpose: 
	• Data Integration: Ensures data from different sources is compatible and can be combined.  
	• Query Optimization: Organizes data in a way that allows for efficient querying and retrieval.  
	• Scalability: Models are designed to handle increasing amounts of data and users. 
	• Enhanced Data Quality: Reduces redundancy and inconsistencies, leading to more reliable data.

• Techniques: 
	• Dimensional Modeling: A common technique in data warehousing that uses fact and dimension tables to represent business processes and their associated attributes. 
	• Entity-Relationship Modeling (ERM): A conceptual model that represents entities, their attributes, and relationships.
	• Relational Modeling: A logical model that organizes data into tables with rows and columns and defines relationships between them.  

• Layers: 
	• Conceptual Model: A high-level, abstract view of the data.  
	• Logical Model: Refines the conceptual model into a more detailed representation, including data types and relationships. 
	• Physical Model: Specifies how the data will be physically stored in the database. 

| Feature                  | Star Schema                                     | Snowflake Schema                              |
| ------------------------ | ----------------------------------------------- | --------------------------------------------- |
| **Structure**            | Central fact table with denormalized dimensions | Central fact table with normalized dimensions |
| **Complexity**           | Simple                                          | Complex                                       |
| **Normalization**        | Denormalized                                    | Normalized (up to 3NF or more)                |
| **Query Performance**    | Faster (fewer joins)                            | Slower (more joins required)                  |
| **Storage Requirements** | More (due to data redundancy)                   | Less (due to normalization)                   |
| **Ease of Maintenance**  | Easier to maintain and query                    | More complex to manage                        |
| **Data Redundancy**      | Higher                                          | Lower                                         |
| **Use Case**             | Simple reporting and dashboards                 | Complex data analysis with integrity          |
| **Join Complexity**      | Low                                             | High                                          |
| **Example Tool Usage**   | Best with tools like Power BI, Tableau          | Also good with OLAP systems like SSAS         |
