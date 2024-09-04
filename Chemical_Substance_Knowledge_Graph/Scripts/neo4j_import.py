from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"  # Adjust to your Neo4j instance
user = "neo4j"
password = "password"  # Replace with your Neo4j password

# Create a Neo4j driver instance
driver = GraphDatabase.driver(uri, auth=(user, password))

# Define a function to create ChemicalSubstance and ExposureEvent nodes and relationships
def create_chemical_and_exposure(tx, chemical_data, exposure_data):
    # Create Chemical Substance nodes
    for _, row in chemical_data.iterrows():
        tx.run(
            """
            MERGE (c:ChemicalSubstance {
                Norman_SusDat_ID: $Norman_SusDat_ID, 
                DTXSID: $DTXSID, 
                dtxcid: $dtxcid, 
                cas_number: $cas_number, 
                Substance_Name: $Name
            })
            """, 
            **row
        )
    
    # Create Exposure Event nodes and EXPOSED_AT relationships
    for _, row in exposure_data.iterrows():
        tx.run(
            """
            MATCH (c:ChemicalSubstance {Norman_SusDat_ID: $Norman_SusDat_ID, DTXSID: $DTXSID})
            MERGE (e:ExposureEvent {
                IDX: $IDX,
                concentration_value: $concentration_value, 
                concentration_unit: $concentration_unit, 
                time_point: $time_point,
                station_water_combined: $station_water_combined,
                lat: $lat,
                lon: $lon,
                station_name_n: $station_name_n,
                country: $country,
                water_body_name_n: $water_body_name_n,
                river_basin_name_n: $river_basin_name_n
            })
            MERGE (c)-[:EXPOSED_AT {
                concentration_value: $concentration_value,
                concentration_unit: $concentration_unit,
                time_point: $time_point
            }]->(e)
            """, 
            **row
        )

# Define a function to create HazardInfo nodes
def create_hazard_info(tx, hazard_data):
    # Create Hazard Information nodes
    for _, row in hazard_data.iterrows():
        tx.run(
            """
            MERGE (h:HazardInfo {
                tox_value_mg_L: $tox_value_mg_L,
                tox_stat: $tox_stat,
                tox_source: $tox_source,
                species: $species,
                tox_reliability: $tox_reliability,
                neutral_fraction_jchem: $neutral_fraction_jchem,
                tox_source_origin: $tox_source_origin
            })
            """, 
            **row
        )

# Define a function to create HAS_HAZARD relationships
def create_has_hazard_relationship(tx, hazard_data):
    for _, row in hazard_data.iterrows():
        tx.run(
            """
            MATCH (c:ChemicalSubstance {DTXSID: $DTXSID})
            MATCH (h:HazardInfo {species: $species, tox_value_mg_L: $tox_value_mg_L})
            MERGE (c)-[:HAS_HAZARD {
                tox_value_mg_L: $tox_value_mg_L,
                species: $species,
                tox_stat: $tox_stat
            }]->(h)
            """, 
            **row
        )

# Main execution to create the graph
with driver.session() as session:
    session.write_transaction(create_chemical_and_exposure, chemical_data, exposure_data)
    session.write_transaction(create_hazard_info, hazard_data)
    session.write_transaction(create_has_hazard_relationship, hazard_data)

# Close the driver connection
driver.close()
