import pandas as pd
import json

LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion",
    "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"
]

def calculate_overall_accuracy(ground_truth_path, predictions_path):
    ground_truth = pd.read_excel(ground_truth_path, sheet_name='Original_Data', header=1)
    ground_truth.columns = ground_truth.columns.str.strip() 

    with open(predictions_path) as f:
        preds = json.load(f)

    total_correct = 0
    total_labels = 0
    
    for filename, pred_labels in preds.items():
        study_id = int(filename[1:-4])

        truth_row = ground_truth[ground_truth['study_id'] == study_id]

        for label in LABELS:
            truth_value = truth_row[label].values[0]

            if truth_value not in [1, 0, -1]:
                continue

            pred_value = pred_labels.get(label)

            if isinstance(pred_value, str):
                pred_value = pred_value.strip()
                if pred_value in ["null", "None", ""]:
                    pred_value = None
                elif pred_value in ["1", "0", "-1"]:
                    pred_value = int(pred_value)

            if pred_value == truth_value:
                total_correct += 1

            total_labels += 1

    overall_accuracy = total_correct / total_labels if total_labels > 0 else 0.0
    return overall_accuracy, total_correct, total_labels

if __name__ == "__main__":
    accuracy, correct, total = calculate_overall_accuracy(
        ground_truth_path="DataChecking.xlsx",
        predictions_path="llama_results/all_extracted_labels_llama.json"
    )
    print(f"\nOverall Accuracy: {accuracy:.2%} ({correct}/{total} labels correct)")
