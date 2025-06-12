import pandas as pd
import json
from collections import defaultdict

LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion",
    "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"
]

def calculate_label_accuracy(excelData_path, result_path):
    data = pd.read_excel(excelData_path, sheet_name='Original_Data', header=1)
    data.columns = data.columns.str.strip()  

    with open(result_path) as f:
        results = json.load(f)

    label_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    

    for filename, result_labels in results.items():
        study_id = int(filename[1:-4]) 
        data_row = data[data['study_id'] == study_id]
            
        for label in LABELS:
            data_value = truth_row[label].values[0]

            result_value = result_labels.get(label)

            if isinstance(result_value, str):
                result_value = result_value.strip()
                if result_value in ["null", "None", ""]:
                    result_value = None
                elif result_value in ["1", "0", "-1"]:
                    result_value = int(result_value)


            if result_value == data_value:
                label_stats[label]['correct'] += 1
            label_stats[label]['total'] += 1

    results = {}
    for label in LABELS:
        if label_stats[label]['total'] > 0:
            accuracy = label_stats[label]['correct'] / label_stats[label]['total']
            results[label] = {
                'accuracy': accuracy,
                'correct': label_stats[label]['correct'],
                'total': label_stats[label]['total']
            }
        else:
            results[label] = {
                'accuracy': 0.0,
                'correct': 0,
                'total': 0
            }
    
    return results


if __name__ == "__main__":
    per_label_results = calculate_label_accuracy(
        excelData_path="DataChecking.xlsx",
        result_path="llama_results/all_extracted_labels_llama.json"
    )
    

    print("\nPer-Label Accuracy Results:")
    print("{:<25} {:<10} {:<15} {:<10}".format(
        "Label", "Accuracy", "Correct/Total", "Percentage"
    ))
    print("-" * 60)
    
    for label, stats in per_label_results.items():
        print("{:<25} {:<10.4f} {:<5}/{:<8} {:<10.2%}".format(
            label,
            stats['accuracy'],
            stats['correct'],
            stats['total'],
            stats['accuracy']
        ))


    total_correct = sum(stats['correct'] for stats in per_label_results.values())
    total_labels = sum(stats['total'] for stats in per_label_results.values())
    overall_accuracy = total_correct / total_labels if total_labels > 0 else 0.0
    print("\nOverall Accuracy Across All Labels: {:.2%} ({}/{})".format(
        overall_accuracy, total_correct, total_labels
    ))