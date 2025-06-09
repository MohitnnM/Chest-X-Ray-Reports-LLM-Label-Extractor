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

def create_cot_prompt(report_text):
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

def parse_llm_output(llm_output):
    try:
        match = re.search(r'\{.*?\}', llm_output, re.DOTALL)
        if match:
            raw_json = match.group(0)
            parsed = json.loads(raw_json)
            return {k: (int(v) if v is not None else None) for k, v in parsed.items() if k in LABELS}
    except Exception as e:
        print("⚠️ Parse error:", e)
    return {}

def main():
    all_labels = {}
    os.makedirs("debug_outputs", exist_ok=True)

    total_processed = 0

    for file_num in range(1, 11):  # 1 through 10
        file_name = f'processed_reports_{file_num}.json'
        print(f"\n📂 Starting file: {file_name}")

        with open(file_name, 'r', encoding='utf-8') as f:
            reports = json.load(f)

        for i, (fname, sections) in enumerate(reports.items(), start=1):
            total_processed += 1
            report_text = (sections.get('findings') or '') + "\n" + (sections.get('impression') or '')
            prompt = create_cot_prompt(report_text)

            print(f"[{total_processed}] Processing {fname} from {file_name}...")

            try:
                llm_response = generate_prompt(prompt)
                with open(f'debug_outputs/{fname}_llm_response.txt', 'w', encoding='utf-8') as fout:
                    fout.write(llm_response or 'None')

                labels = parse_llm_output(llm_response or '')

                if not any(val == 1 for val in labels.values()):
                    labels["No Finding"] = 1

                all_labels[fname] = labels

            except Exception as e:
                print(f"⚠️ Error processing {fname}: {e}")
                all_labels[fname] = {}

            # Save every 10 reports
            if total_processed % 10 == 0 or total_processed == sum(len(json.load(open(f'processed_reports_{n}.json'))) for n in range(1, 11)):
                with open('extracted_labels_deepseek_all.json', 'w', encoding='utf-8') as fout:
                    json.dump(all_labels, fout, indent=2)
                print(f"✅ Saved progress at {total_processed} reports")

    print(f"\n✅ Extraction complete for {total_processed} reports. Saved to extracted_labels_llama_all.json")

if __name__ == '__main__':
    main()

#important:
#wsl -e bash -c "cd /home/mohit/Chest-X-Ray-Reports-LLM-Label-Extractor-1 && python3 label_extractor.py"