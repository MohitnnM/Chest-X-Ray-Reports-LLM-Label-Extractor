import pandas as pd
import json

LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion",
    "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"
]

def calculate_accuracy(excelData_path, results_path):
    excelData = pd.read_excel(excelData_path, sheet_name='Original_Data', header=1)
    excelData.columns = excelData.columns.str.strip() 

    with open(results_path) as f:
        results = json.load(f)

    tot_corr = 0
    tot_lab = 0
    
    for filename, result_labels in results.items():
        study_id = int(filename[1:-4])

        data_row = excelData[excelData['study_id'] == study_id]

        for label in LABELS:
            data_value = data_row[label].values[0]

            if data_value not in [1, 0, -1]:
                continue

            result_value = result_labels.get(label)

            if isinstance(result_value, str):
                result_value = result_value.strip()
                if result_value in ["null", "None", ""]:
                    result_value = None
                elif result_value in ["1", "0", "-1"]:
                    result_value = int(result_value)

            if result_value == data_value:
                tot_corr += 1

            tot_lab += 1

    overall_accuracy = tot_corr / tot_lab if tot_lab > 0 else 0.0
    return overall_accuracy, tot_corr, tot_lab

if __name__ == "__main__":
    accuracy, correct, total = calculate_accuracy(
        excelData_path="DataChecking.xlsx",
        results_path="llama_results/all_extracted_labels_llama.json"
    )
    print(f"\nOverall Accuracy: {accuracy:.2%} ({correct}/{total} labels correct)")
