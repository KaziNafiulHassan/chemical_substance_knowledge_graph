// Example Queries

// Retrieve All Chemicals and Their Hazards:
MATCH (c:ChemicalSubstance)-[r:HAS_HAZARD]->(h:HazardInfo)
RETURN c.DTXSID AS Chemical, h.species AS Species, h.tox_value_mg_L AS ToxicityValue
LIMIT 25

// Count the Number of Hazards per Chemical:
MATCH (c:ChemicalSubstance)-[r:HAS_HAZARD]->(h:HazardInfo)
RETURN c.DTXSID AS Chemical, COUNT(r) AS NumberOfHazards
ORDER BY NumberOfHazards DESC
LIMIT 10

// Find Chemicals Linked to a Specific Species:
MATCH (c:ChemicalSubstance)-[r:HAS_HAZARD]->(h:HazardInfo {species: 'Daphnia magna'})
RETURN c.DTXSID AS Chemical, h.tox_value_mg_L AS ToxicityValue
LIMIT 10

