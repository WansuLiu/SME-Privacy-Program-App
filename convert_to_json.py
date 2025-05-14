import csv
import json


# Input and output file paths
csv_file = "SOC 2 to NIST Privacy Framework - Roadmap.csv"
json_file = "roadmap_data.json"

output = []

with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for index, row in enumerate(reader, start=1):
        task = {
            "id": f"T{index:03}",  # e.g., T001, T002
            "category": row["Category"].strip(),
            "task": row["Item"].strip(),
            "tier": int(row["Tier"]),
            "role": row["Responsible Role"].strip(),
            "type": row["Relevant to "].strip(),
            "third_party_collection": row["Only Applicable if Third Party Collection Exists"].strip().upper() == "TRUE",
            "third_party_disclosure": row["Only Applicable if Third Party Disclosure Related"].strip().upper() == "TRUE",
            "done": False
        }
        output.append(task)

# Write to JSON
with open(json_file, mode='w', encoding='utf-8') as file:
    json.dump(output, file, indent=2)

print(f"✅ Successfully converted to {json_file}")
