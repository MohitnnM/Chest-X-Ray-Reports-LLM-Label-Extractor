import pandas as pd
import json

dataset = pd.read_excel("DataChecking.xlsx", sheet_name="Original_Data", header=1)
with open("llama_results/all_extracted_labels_llama.json", "r") as results_data:
    json_data = json.load(results_data)

json_df = pd.DataFrame.from_dict(json_data, orient="index")
json_df.index = json_df.index.str.replace("s", "").str.replace(".txt", "").astype(int)
merged = pd.merge(excel_data[excel_data["study_id"].isin(json_df.index)], 
                  json_df.add_suffix("_pred"), left_on="study_id", right_index=True)

labels = ["Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Enlarged Cardiomediastinum", 
          "Fracture", "Lung Lesion", "Lung Opacity", "No Finding", "Pleural Effusion", 
          "Pleural Other", "Pneumonia", "Pneumothorax", "Support Devices"]


def calc_metrics(df, labels):
    results = []
    for label in labels:
        valid = df[df[label].isin([0,1]) & df[f"{label}_pred"].isin([0,1])]
        if len(valid) == 0:
            results.append([label] + [0]*4 + [None]*4 + [0]*3)
            continue
            
        tp = ((valid[label] == 1) & (valid[f"{label}_pred"] == 1)).sum()
        fp = ((valid[label] == 0) & (valid[f"{label}_pred"] == 1)).sum()
        tn = ((valid[label] == 0) & (valid[f"{label}_pred"] == 0)).sum()
        fn = ((valid[label] == 1) & (valid[f"{label}_pred"] == 0)).sum()
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else None
        fpr = fp / (fp + tn) if (fp + tn) > 0 else None
        precision = tp / (tp + fp) if (tp + fp) > 0 else None
        specificity = tn / (tn + fp) if (tn + fp) > 0 else None
        
        results.append([label, tp, fp, tn, fn, tpr, fpr, precision, specificity, len(valid), tp+fn, fp+tn])
    
    return pd.DataFrame(results, columns=["Label", "TP", "FP", "TN", "FN", "TPR", "FPR", 
                                         "Precision", "Specificity", "Total", "Positive", "Negative"])

df = calc_metrics(merged, labels)


display_df = df.copy()
for col in ["TPR", "FPR", "Precision", "Specificity"]:
    display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")

print("="*100)
print("PERFORMANCE ANALYSIS")
print("="*100)
print(display_df.to_string(index=False))

valid_metrics = df.dropna(subset=["TPR", "FPR", "Precision", "Specificity"])
totals = df[["TP", "FP", "TN", "FN"]].sum()
overall_tpr = totals.TP / (totals.TP + totals.FN) if (totals.TP + totals.FN) > 0 else 0
overall_fpr = totals.FP / (totals.FP + totals.TN) if (totals.FP + totals.TN) > 0 else 0
overall_precision = totals.TP / (totals.TP + totals.FP) if (totals.TP + totals.FP) > 0 else 0

print(f"\nSUMMARY:")
print(f"Avg TPR: {valid_metrics['TPR'].mean():.4f} | Avg FPR: {valid_metrics['FPR'].mean():.4f}")
print(f"Overall TPR: {overall_tpr:.4f} | Overall FPR: {overall_fpr:.4f} | Overall Precision: {overall_precision:.4f}")


issues = df[(df['FPR'] > 0.1) | (df['TPR'] < 0.7) | (df['FPR'] == 1.0) | (df['TPR'] == 0.0)]
if not issues.empty:
    print(f"\nISSUES FOUND:")
    for _, row in issues.iterrows():
        print(f"• {row['Label']}: TPR={row['TPR']:.3f}, FPR={row['FPR']:.3f}")

print(f"\nTotal cases: {df['Total'].sum()} | Conditions with data: {len(df[df['Total'] > 0])}")