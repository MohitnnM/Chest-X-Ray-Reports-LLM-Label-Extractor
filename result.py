import pandas as pd
import json
from collections import defaultdict

LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion",
    "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"
]

def calculate_per_label_accuracy(ground_truth_path, predictions_path):
    ground_truth = pd.read_excel(ground_truth_path, sheet_name='Original_Data', header=1)
    ground_truth.columns = ground_truth.columns.str.strip()  

    with open(predictions_path) as f:
        preds = json.load(f)

    label_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    

    for filename, pred_labels in preds.items():


        study_id = int(filename[1:-4]) '
        truth_row = ground_truth[ground_truth['study_id'] == study_id]
            
        for label in LABELS:

            truth_value = truth_row[label].values[0]

            pred_value = pred_labels.get(label)

            if isinstance(pred_value, str):
                pred_value = pred_value.strip()
                if pred_value in ["null", "None", ""]:
                    pred_value = None
                elif pred_value in ["1", "0", "-1"]:
                    pred_value = int(pred_value)


            if pred_value == truth_value:
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
    per_label_results = calculate_per_label_accuracy(
        ground_truth_path="DataChecking.xlsx",
        predictions_path="llama_results/all_extracted_labels_llama.json"
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