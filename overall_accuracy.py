import pandas as pd
import json

# Constants
LABELS = [
    "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
    "Enlarged Cardiomediastinum", "Fracture", "Lung Lesion",
    "Lung Opacity", "No Finding", "Pleural Effusion",
    "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"
]

def calculate_overall_accuracy(ground_truth_path, predictions_path):
    # Load ground truth (Excel)
    ground_truth = pd.read_excel(ground_truth_path, sheet_name='Original_Data', header=1)
    ground_truth.columns = ground_truth.columns.str.strip()  # remove whitespace

    # Load LLM predictions (JSON)
    with open(predictions_path) as f:
        preds = json.load(f)

    # Initialize counters
    total_correct = 0
    total_labels = 0
    
    # Compare each report
    for filename, pred_labels in preds.items():
        # Extract study_id from filename (e.g., "s55477042.txt" -> 55477042)
        try:
            study_id = int(filename[1:-4])  # Remove 's' and '.txt'
        except ValueError:
            print(f"Skipping invalid filename format: {filename}")
            continue

        # Find matching ground truth row
        truth_row = ground_truth[ground_truth['study_id'] == study_id]
        if truth_row.empty:
            print(f"Warning: No ground truth for {filename}")
            continue
            
        # Compare each label
        for label in LABELS:
            if label not in ground_truth.columns:
                print(f"Label {label} missing in ground truth. Skipping.")
                continue

            truth_value = truth_row[label].values[0]

            # Only process if ground truth is valid (1, 0, or -1)
            if truth_value not in [1, 0, -1]:
                continue

            pred_value = pred_labels.get(label)

            # Handle string forms
            if isinstance(pred_value, str):
                pred_value = pred_value.strip()
                if pred_value in ["null", "None", ""]:
                    pred_value = None
                elif pred_value in ["1", "0", "-1"]:
                    pred_value = int(pred_value)

            if pred_value == truth_value:
                total_correct += 1

            total_labels += 1

    # Calculate overall accuracy
    overall_accuracy = total_correct / total_labels if total_labels > 0 else 0.0
    return overall_accuracy, total_correct, total_labels

# Usage
if __name__ == "__main__":
    accuracy, correct, total = calculate_overall_accuracy(
        ground_truth_path="DataChecking.xlsx",
        predictions_path="llama_results/all_extracted_labels_llama.json"
    )
    print(f"\nOverall Accuracy: {accuracy:.2%} ({correct}/{total} labels correct)")
#extracted_labels_deepseek_all