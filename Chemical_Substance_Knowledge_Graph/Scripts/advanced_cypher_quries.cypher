// Add Relationships Between Chemicals Based on Similarity:
// eg.: linking chemicals that belong to the same chemical family:
MATCH (c1:ChemicalSubstance)
MATCH (c2:ChemicalSubstance)
WHERE c1.family = c2.family AND c1.DTXSID <> c2.DTXSID
CREATE (c1)-[:SIMILAR_TO]->(c2)

// Analyze the Most Hazardous Chemicals:
// Identifying chemicals with the highest average toxicity across species:
MATCH (c:ChemicalSubstance)-[r:HAS_HAZARD]->(h:HazardInfo)
RETURN c.DTXSID AS Chemical, AVG(h.tox_value_mg_L) AS AvgToxicity
ORDER BY AvgToxicity DESC
LIMIT 10

