import os
import re 
from bs4 import BeautifulSoup
import json

        
def extract_report_info(filepath):
    with open(filepath, 'r', encoding='utf-8') as reports:
        soup = BeautifulSoup(reports, 'html.parser')

    search_report = soup.find("pre")
    if not search_report:
        return None, None
      
    report_txt = search_report.get_text()
    lines = report_txt.strip().splitlines()
    report_findings = []
    report_impression = []
    sec_curr = None

    for line in lines:
        line = line.strip()
        line_uppercase = line.upper()

        if line_uppercase.startswith("FINDINGS"):
            sec_curr = "findings"
            report_findings.append(line)
            continue
        elif line_uppercase.startswith("IMPRESSION"):
            sec_curr = "impression"
            report_impression.append(line)
            continue
        
        if sec_curr == "findings":
            report_findings.append(line)
        elif sec_curr == "impression":
            report_impression.append(line)

        if report_findings:
            report_finding_txt = "\n".join(report_findings).strip()
        else:
            report_finding_txt = None
        
        if report_impression:
            report_impression_txt = "\n".join(report_impression).strip() 
        else:
            report_impression_txt = None
    return report_finding_txt, report_impression_txt


def txt_to_json(data_path):
    reports = {}
    for filename in os.listdir(data_path):
        if not filename.endswith('.txt'):
            continue
    for name in os.listdir(data_path):
        path = os.path.join(data_path, name)
        findings_txt, impression_txt = extract_report_info(path)
        reports[name] = {
        'findings': findings_txt,
            'impression': impression_txt
        }
    return reports

def save_extracted_info(reports_info, save_location):
    with open(save_location, 'w', encoding='utf-8') as saving_data:
        json.dump(reports_info, saving_data, indent=4)

if __name__ == "__main__":
    input_path = "data/all_cases"
    output_path = "JSON_reports/processed_reports.json"
    processed_reports = txt_to_json(input_path)
    save_extracted_info(processed_reports, output_path)