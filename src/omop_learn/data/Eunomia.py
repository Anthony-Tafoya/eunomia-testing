import pandas as pd
from sqlalchemy import create_engine

# Create a connection to your PostgreSQL database
engine = create_engine('postgresql://user@localhost/user')

# Load the care_site table and write to PostgreSQL
data = pd.read_csv('/Users/user/Desktop/Research/omop-learn/src/omop_learn/data/GiBleed_5.3/DRUG_ERA.csv')
data.to_sql('drug_era', engine, if_exists='replace', index=False)

# Define the diabetes drug code you're interested in
diabetes_drug_code = 738818  # Replace with the actual drug code

# Define the SQL query
sql_query = f"""
    SELECT *
    FROM drug_era
    WHERE (CAST("DRUG_ERA_END_DATE" AS DATE) - CAST("DRUG_ERA_START_DATE" AS DATE)) >= 30
    AND "DRUG_CONCEPT_ID" = {diabetes_drug_code};
"""

# Execute the query and load the result into a pandas DataFrame
data = pd.read_sql(sql_query, engine)
print(data)

# PLANNED query for the actual database

# SELECT *
# FROM drug_era
# JOIN hbA1c_measurements ON drug_era.person_id = hbA1c_measurements.person_id
# WHERE drug_era_start_date AND drug_era_end_date >= INTERVAL '1 year'
# AND drug_concept_id = {diabetes_drug_code}
# GROUP BY drug_era.person_id
# HAVING COUNT(hbA1c_measurements) >= 3 AND AVG(hbA1c_measurements over (ORDER BY measurement_date DESC ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)) IS NOT NULL;




