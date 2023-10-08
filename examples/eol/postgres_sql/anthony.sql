DROP TABLE IF EXISTS mcs_t2dm.trt_var_v8; 

CREATE TABLE mcs_t2dm.trt_var_v8 (
    WITH 
    -- Condition #1: Patient has at least a year of observational data 
    one_year AS (
        SELECT person_id
        FROM cdm.observation_period
        WHERE EXTRACT(EPOCH FROM (observation_period_end_date - observation_period_start_date))/(24*60*60) >= EXTRACT(EPOCH FROM (1 * INTERVAL '1 year'))/(24*60*60)
    ),

    -- Condition #2: Patient received a diabetes-related perscription
    diabetes_rx AS (
        SELECT DISTINCT de.person_id
        FROM diabetes_drug_concepts ddc
        JOIN cdm.drug_exposure de ON de.drug_concept_id = ddc.drug_concept_id 
        WHERE de.person_id != -1 
    )

    --Condition #3: Patient has received over 3 HbA1C measurments 
    hba1c_counts AS (
        SELECT person_id
        FROM cdm.measurement
        WHERE measurement_concept_id IN (HBA1C) 
        GROUP BY person_id
        HAVING COUNT(*) >= 3
    )

    -- Creates a table that combines all three conditions
    SELECT *
    FROM cdm.person p
    JOIN one_year_obs oyo ON p.person_id = oyo.person_id
    JOIN diabetes_rx drx ON p.person_id = drx.person_id
    JOIN hba1c_counts hc ON p.person_id = hc.person_id;


