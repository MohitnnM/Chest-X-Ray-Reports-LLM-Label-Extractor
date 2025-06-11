import json
import os
import re
from generator import generate_prompt

LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion", "Pleural Other",
    "Pneumonia", "Pneumothorax", "Support Devices"
]

def prompt_create(report_text):
    prompt = f"""
You are a board-certified radiologist analyzing a radiology report. Your task is to:
1. Carefully read the entire report
2. Label each condition STRICTLY according to these rules:
   - 1: Condition is definitively present (clear, unambiguous evidence)
   - 0: Condition is definitively absent (explicit negation like "no evidence of")
   - -1: Condition is uncertain (terms like "possible", "cannot exclude")
   - null: Condition is not mentioned at all

CRITICAL RULES:
1. "No Finding" must be 1 ONLY if ALL other conditions are either 0 or null
2. For any condition explicitly negated ("no X", "ruled out"), you MUST label it 0
3. Only label conditions 1 when there is direct, unambiguous evidence
4. Pay special attention to negation phrases and absence statements

CONDITIONS TO LABEL:
{json.dumps(LABELS, indent=4)}

EXAMPLE OUTPUT FOR REFERENCE:
{{
    "Atelectasis": null,
    "Cardiomegaly": null,
    "Consolidation": 0,
    "Edema": 0,
    "Enlarged Cardiomediastinum": null,
    "Fracture": null,
    "Lung Lesion": 0,
    "Lung Opacity": null,
    "No Finding": 1,
    "Pleural Effusion": 0,
    "Pleural Other": null,
    "Pneumonia": null,
    "Pneumothorax": 0,
    "Support Devices": null
}}

REPORT TO ANALYZE:
{json.dumps(report_text)}

YOUR OUTPUT MUST BE:
1. Valid JSON ONLY
2. Contain ALL {len(LABELS)} specified keys
3. Follow the labeling rules EXACTLY
4. No additional commentary or explanation

OUTPUT:
```json
"""
    return prompt

def parse_output(output):
    results = {}
    match = re.search(r'\{.*?\}', output, re.DOTALL)
    if match:
        raw_json = match.group(0)
        parsed = json.loads(raw_json)
        for k, v in parsed.items():
            if k in LABELS:
                if v is not None:
                    results[k] = int(v)
                else:
                    results[k] = None
    return results

def main():
    all_lab = {}
    os.makedirs("debug_outputs", exist_ok=True)

    tot_proc = 0
    file_name = 'processed_reports.json'

    with open(file_name, 'r', encoding='utf-8') as f:
        reports = json.load(f)

    for i, (fname, sections) in enumerate(reports.items(), start=1):
        tot_proc += 1
        report_text = (sections.get('findings') or '') + "\n" + (sections.get('impression') or '')
        prompt = prompt_create(report_text)

        llm_response = generate_prompt(prompt)
        with open(f'debug_outputs/{fname}_llm_response.txt', 'w', encoding='utf-8') as fout:
            fout.write(llm_response or 'None')

        labels = parse_output(llm_response or '')
        if not any(val == 1 for val in labels.values()):
            labels["No Finding"] = 1
        all_lab[fname] = labels

        if tot_proc % 10 == 0:
            with open('extracted_labels_deepseek_all.json', 'w', encoding='utf-8') as fout:
                json.dump(all_lab, fout, indent=4)
                print("Saved")

if __name__ == '__main__':
    main()
