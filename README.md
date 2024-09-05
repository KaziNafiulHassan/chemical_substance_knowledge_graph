# Chemical Substance Graph Analysis

## Overview

This project uses a graph database (Neo4j) to analyze the relationships between chemical substances, their exposure concentrations in various water bodies, and their associated hazards to different species. The graph database allows for intuitive exploration of these relationships and offers a foundation for more complex queries and analysis.

## Features

- **Data Relationships**: Explore connections between chemical substances, exposure concentrations, and species-specific hazards.
- **Simple Queries**: Retrieve and visualize basic relationships in the data.
- **Advanced Queries**: Perform complex analyses to gain deeper insights into the chemical hazards.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Neo4j Desktop](https://neo4j.com/download/)
- [Python 3.x](https://www.python.org/downloads/)
- Python libraries (install via `requirements.txt`):
  ```bash
  pip install -r requirements.txt

## Setup Instructions

Step 1: Start Neo4j
- Install Neo4j Desktop and create a new project.
- Add a Local DBMS to the project and start it.
- Set Up Credentials: Default credentials are usually username: neo4j and password: neo4j.
- Make sure you remember these credentials for the scripts.

Step 2: Load Data into Neo4j
- Preprocess Data: Run the data_preprocessing.py script to clean and preprocess the datasets.
- Example command: python scripts/data_preprocessing.py
- Import Data to Neo4j: Use the neo4j_import.py script to create nodes and relationships in your Neo4j instance.
- Example command: python scripts/neo4j_import.py

Step 3: Explore the Graph
- Example Queries: Example cypher queries are given in the repository

## Advanced Queries and Enhancements
- Some advanced cypher queries are given in the repository.
- A Flask app has been created and added to the repository for a web interface. This web interface will be updated in future.
