from reports_parser import Report_Parser
import json
import os

def process_reports():
    parse = Report_Parser(data_dir='data/all_cases')

    total_reports = parse.extract_reports()

    print(f"Extracted: {len(total_reports)} reports")

    output = 'processed_reports.json'

    with open(output, 'w', encoding = "utf-8") as reports_fin:
        json.dump(total_reports, reports_fin, indent = 2)

    print("Completed")

if __name__ == "__main__":
    process_reports()