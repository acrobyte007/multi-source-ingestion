import csv
import json
import os

def extract_column_names_as_json(csv_file_path):
    csv_file_path = os.path.normpath(csv_file_path)
    with open(csv_file_path, newline='', encoding='cp1252') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames:
            return json.dumps({"columns": reader.fieldnames}, indent=4, ensure_ascii=False)
    return json.dumps({"error": "No columns found"}, indent=4)

csv_file_path = "E:/ETL/multi-source-ingestion/Articles.csv"
print(extract_column_names_as_json(csv_file_path))
