import os
import re 
from bs4 import BeautifulSoup

class Report_Parser():
    def __init__(self, data_dir = 'data/all_cases/s56138591.txt'):
        self.data_dir = data_dir

        
    def extract_text(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as patient_reports:
            soup = BeautifulSoup(patient_reports, 'html.parser')

        find_report = soup.find("pre")
        if not find_report:
            return None, None
        
        report = find_report.get_text()
        lines = report.strip().splitlines()
        findings = []
        impression = []
        current_sec = None

        for line in lines:
            line = line.strip()
            upper = line.upper()

            if upper.startswith("FINDINGS"):
                current_sec = "findings"
                findings.append(line)
                continue
            elif upper.startswith("IMPRESSION"):
                current_sec = "impression"
                impression.append(line)
                continue
            
            if current_sec == "findings":
                findings.append(line)

            elif current_sec == "impression":
                impression.append(line)

        return "\n".join(findings).strip() if findings else None, \
            "\n".join(impression).strip() if impression else None


    def extract_reports(self):
        reports = {}
        for fname in os.listdir(self.data_dir):
            if not fname.endswith('.txt'):
                continue
            path = os.path.join(self.data_dir, fname)
            findings, impression = self.extract_text(path)
            reports[fname] = {
                'findings': findings,
                'impression': impression
            }
        return reports
