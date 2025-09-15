import pandas as pd
import mysql.connector
# import json

df = pd.read_csv('preprocessed_trials.csv')

conn = mysql.connector.connect(
  host = "",                        # add your connector details here
  port = 4000,
  user = ".root",
  password = "",
  database = "test",
  ssl_ca = ".pem",
  ssl_verify_cert = True,
  ssl_verify_identity = True
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinical_trials_latest (
        nct_number VARCHAR(20) PRIMARY KEY,
        study_title TEXT,
        study_url TEXT,
        acronym VARCHAR(50),
        study_status VARCHAR(50),
        brief_summary TEXT,
        study_results VARCHAR(10),  -- e.g., 'YES'/'NO'
        conditions TEXT,
        interventions TEXT,
        primary_outcome_measures TEXT,
        secondary_outcome_measures TEXT,
        other_outcome_measures TEXT,
        sponsor TEXT,
        collaborators TEXT,
        sex VARCHAR(50),
        age TEXT,
        phases TEXT,
        enrollment FLOAT,
        funder_type VARCHAR(50),
        study_type VARCHAR(50),
        study_design TEXT,
        other_ids TEXT,
        start_date DATE,
        primary_completion_date DATE,
        completion_date DATE,
        first_posted DATE,
        results_first_posted DATE,
        last_update_posted DATE,
        locations TEXT,
        study_documents TEXT,
        text_for_embedding TEXT,
        embedding VECTOR(384)
    );
""")

cursor.execute("ALTER TABLE clinical_trials_latest ADD VECTOR INDEX vec_idx ((VEC_COSINE_DISTANCE(embedding))) ADD_COLUMNAR_REPLICA_ON_DEMAND;")
conn.commit()

# Batch insert
batch_size = 200
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i + batch_size]
    values = []
    for _, row in batch.iterrows():
        def safe_text(val):
            return val.replace("'", "''") if pd.notna(val) else None
        
        values.append((
            row['NCT Number'],
            safe_text(row['Study Title']),
            safe_text(row['Study URL']),
            safe_text(row['Acronym']),
            safe_text(row['Study Status']),
            safe_text(row['Brief Summary']),
            safe_text(row['Study Results']),
            safe_text(row['Conditions']),
            safe_text(row['Interventions']),
            safe_text(row['Primary Outcome Measures']),
            safe_text(row['Secondary Outcome Measures']),
            safe_text(row['Other Outcome Measures']),
            safe_text(row['Sponsor']),
            safe_text(row['Collaborators']),
            safe_text(row['Sex']),
            safe_text(row['Age']),
            safe_text(row['Phases']),
            row['Enrollment'] if pd.notna(row['Enrollment']) else None,
            safe_text(row['Funder Type']),
            safe_text(row['Study Type']),
            safe_text(row['Study Design']),
            safe_text(row['Other IDs']),
            row['Start Date'] if pd.notna(row['Start Date']) else None,
            row['Primary Completion Date'] if pd.notna(row['Primary Completion Date']) else None,
            row['Completion Date'] if pd.notna(row['Completion Date']) else None,
            row['First Posted'] if pd.notna(row['First Posted']) else None,
            row['Results First Posted'] if pd.notna(row['Results First Posted']) else None,
            row['Last Update Posted'] if pd.notna(row['Last Update Posted']) else None,
            safe_text(row['Locations']),
            safe_text(row['Study Documents']),
            safe_text(row['text_for_embedding']),
            row['embedding']
        ))

    sql = """
        INSERT IGNORE INTO clinical_trials_latest 
        (nct_number, study_title, study_url, acronym, study_status, brief_summary, study_results, conditions, interventions, 
         primary_outcome_measures, secondary_outcome_measures, other_outcome_measures, sponsor, collaborators, sex, age, 
         phases, enrollment, funder_type, study_type, study_design, other_ids, start_date, primary_completion_date, 
         completion_date, first_posted, results_first_posted, last_update_posted, locations, study_documents, 
         text_for_embedding, embedding) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, values)
    conn.commit()
    print(f"Inserted batch {i//batch_size + 1} of {len(df)//batch_size + 1}")

cursor.close()
conn.close()
print("Ingestion complete!")