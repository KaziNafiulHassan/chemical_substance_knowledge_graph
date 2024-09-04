from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase
import math

app = Flask(__name__)

# Neo4j connection details
uri = "bolt://localhost:7687"  # Adjust to your Neo4j instance
user = "neo4j"
password = "password"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(user, password))

# Utility function to execute queries
def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

# Route for the home page with Dropdown Menu and Search
@app.route('/', methods=['GET', 'POST'])
def index():
    query = "MATCH (c:ChemicalSubstance) RETURN c.Name AS name, c.DTXSID AS dtxsid ORDER BY c.Name"
    chemicals = run_query(query)
    
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_value = request.form.get('search_value')
        
        if search_type == 'name':
            return redirect(url_for('search_by_name', name=search_value))
        elif search_type == 'filter':
            return redirect(url_for('filter', filter=search_value))
        elif search_type == 'location':
            return redirect(url_for('search_by_location', location=search_value))
    
    return render_template('index.html', chemicals=chemicals)

# Route for searching by Substance Name
@app.route('/search_by_name/<name>')
def search_by_name(name):
    query = """
    MATCH (c:ChemicalSubstance)-[r:EXPOSED_AT]->(e:ExposureEvent)
    WHERE c.Name CONTAINS $name
    RETURN c.Name AS name, c.DTXSID AS dtxsid, e.concentration_value AS concentration_value, 
           e.station_name_n AS station, e.country AS country
    """
    results = run_query(query, {'name': name})
    return render_template('result.html', results=results, search_type="Substance Name")

# Route for filtering chemicals based on various attributes
@app.route('/filter/<filter>')
def filter(filter):
    query = f"""
    MATCH (c:ChemicalSubstance)-[r:EXPOSED_AT]->(e:ExposureEvent)
    WHERE e.{filter} IS NOT NULL
    RETURN c.Name AS name, c.DTXSID AS dtxsid, e.{filter} AS filter_value, 
           e.station_name_n AS station, e.country AS country
    """
    results = run_query(query)
    return render_template('result.html', results=results, search_type=filter)

# Route for searching by location (water body, river basin)
@app.route('/search_by_location/<location>')
def search_by_location(location):
    query = """
    MATCH (e:ExposureEvent)-[:EXPOSED_AT]-(c:ChemicalSubstance)
    WHERE e.water_body_name_n CONTAINS $location OR e.river_basin_name_n CONTAINS $location
    RETURN e.water_body_name_n AS water_body, e.river_basin_name_n AS river_basin, 
           c.Name AS name, c.DTXSID AS dtxsid, e.station_name_n AS station, e.country AS country
    """
    results = run_query(query, {'location': location})
    return render_template('result.html', results=results, search_type="Location")

# Route for paginated list of all chemical substances
@app.route('/chemicals')
@app.route('/chemicals/page/<int:page>')
def paginated_chemicals(page=1):
    per_page = 10
    skip = (page - 1) * per_page
    
    count_query = "MATCH (c:ChemicalSubstance) RETURN COUNT(c) AS count"
    count_result = run_query(count_query)
    total_chemicals = count_result[0]['count']
    total_pages = math.ceil(total_chemicals / per_page)
    
    query = """
    MATCH (c:ChemicalSubstance)
    RETURN c.Name AS name, c.DTXSID AS dtxsid
    ORDER BY c.Name
    SKIP $skip LIMIT $per_page
    """
    chemicals = run_query(query, {'skip': skip, 'per_page': per_page})
    
    return render_template('chemicals.html', chemicals=chemicals, page=page, total_pages=total_pages)

# Route for displaying detailed information about a chemical
@app.route('/chemical/<dtxsid>')
def chemical_details(dtxsid):
    query = """
    MATCH (c:ChemicalSubstance {DTXSID: $dtxsid})-[:EXPOSED_AT]->(e:ExposureEvent)
    OPTIONAL MATCH (c)-[:HAS_HAZARD]->(h:HazardInfo)
    RETURN c.Name AS name, e.concentration_value AS concentration_value, e.station_name_n AS station, 
           e.country AS country, h.species AS species, h.tox_value_mg_L AS tox_value, 
           h.tox_stat AS tox_stat
    """
    details = run_query(query, {'dtxsid': dtxsid})
    return render_template('chemical_details.html', details=details, name=details[0]['name'])

# Route for interactive graph visualization
@app.route('/visualize')
def visualize():
    query = """
    MATCH (c:ChemicalSubstance)-[:EXPOSED_AT]->(e:ExposureEvent)
    OPTIONAL MATCH (c)-[:HAS_HAZARD]->(h:HazardInfo)
    RETURN c.Name AS name, c.DTXSID AS dtxsid, e.station_name_n AS station, 
           e.country AS country, h.species AS species, h.tox_value_mg_L AS tox_value, 
           h.tox_stat AS tox_stat
    """
    results = run_query(query)
    return render_template('visualize.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port = 5002)
