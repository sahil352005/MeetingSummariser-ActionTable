#!/usr/bin/env python3

from extractor import rule_based_action_extraction
import pandas as pd

# Test with your sample transcript
with open('sample_transcript2.txt', 'r') as f:
    transcript = f.read()

print("Testing action item extraction...")
items = rule_based_action_extraction(transcript)

if items:
    df = pd.DataFrame(items)
    print(f"\nFound {len(items)} action items:")
    print(df.to_string(index=False))
    
    print(f"\nOwners: {df['owner'].unique()}")
    print(f"Deadlines: {df['deadline'].dropna().unique()}")
else:
    print("No action items found!")