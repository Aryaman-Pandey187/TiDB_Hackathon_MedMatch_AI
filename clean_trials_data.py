import pandas as pd
from sentence_transformers import SentenceTransformer
import json

df = pd.read_csv("ctg-studies.csv", low_memory=False)

df = df.drop_duplicates(subset=['NCT Number'])
df = df.dropna(subset=['Conditions', 'Study Status', 'Brief Summary', 'Locations'])

# Generate embeddings on combined text
model = SentenceTransformer('all-MiniLM-L6-v2')
df['text_for_embedding'] = df['Conditions'] + ' ' + df['Brief Summary']
df['embedding'] = df['text_for_embedding'].apply(lambda x: json.dumps(model.encode(x).tolist()))

df.to_csv('preprocessed_trials.csv', index=False)
print(f"Preprocessed {len(df)} diverse trials.")