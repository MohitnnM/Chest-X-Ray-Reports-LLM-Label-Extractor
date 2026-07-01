# 🩻 Chest X-Ray Label Extractor using Large Language Models

## Overview

This project explores the use of **Large Language Models (LLMs)** to automatically extract clinical findings from unstructured chest X-ray reports. Traditional rule-based systems such as **CheXpert** and **NegBio** often struggle with ambiguous language, negation, and uncertainty commonly found in radiology reports.

This project investigates whether modern LLMs can improve label extraction by emulating the reasoning process of a radiologist.

The system preprocesses radiology reports, extracts the clinically relevant sections, prompts locally hosted LLMs using **Chain-of-Thought (CoT) prompting**, and produces structured JSON output containing predicted labels for each report.

---

# ✨ Features

- Automated extraction of **Findings** and **Impression** sections
- HTML metadata removal using **BeautifulSoup**
- Standardised preprocessing pipeline
- Local LLM inference using **Ollama**
- Support for multiple LLMs
  - Llama 3.1 8B
  - DeepSeek R1 7B
- Chain-of-Thought prompting
- Structured JSON output
- Automatic checkpoint saving
- Robust handling of malformed model responses
- Performance comparison against manually validated CheXpert labels

---

# 🛠 Technologies

- Python
- Ollama
- Llama 3.1 8B
- DeepSeek R1 7B
- BeautifulSoup
- Requests
- JSON
- MIMIC-CXR Dataset

---

# 🏗 Project Architecture

```text
                Chest X-Ray Reports
                        │
                        ▼
           HTML Metadata Removal
                        │
                        ▼
     Extract Findings & Impression
                        │
                        ▼
         Convert Reports to JSON
                        │
                        ▼
          Prompt Engineering (CoT)
                        │
                        ▼
                Ollama API
                        │
                        ▼
             Large Language Model
                        │
                        ▼
         Structured Label Extraction
                        │
                        ▼
               JSON Predictions
                        │
                        ▼
        Evaluation Against Ground Truth
```

---

# 📂 Dataset

This project uses a subset of the **MIMIC-CXR** dataset containing approximately **500 de-identified chest X-ray reports**.

Each report contains:

- Findings
- Impression
- Indication
- Technique
- Comparison

Only the **Findings** and **Impression** sections are extracted and analysed.

Labels follow the **CheXpert** annotation scheme.

| Value | Meaning |
|-------:|---------|
| **1** | Condition Present |
| **0** | Condition Absent |
| **-1** | Condition Uncertain |
| **null** | Condition Not Mentioned |

---

# ⚙️ Workflow

## 1. Data Validation

The original CheXpert labels were manually reviewed and validated.

This process involved:

- Reviewing over 500 radiology reports
- Verifying extracted labels
- Resolving disagreements through team discussion
- Producing a validated ground-truth dataset

---

## 2. Report Processing

Each report is processed by:

- Removing HTML metadata
- Extracting the **Findings** section
- Extracting the **Impression** section
- Cleaning whitespace and formatting
- Exporting the results into JSON

Example output:

```json
{
  "s52015620.txt": {
    "findings": "Lungs are clear...",
    "impression": "No evidence of CHF."
  }
}
```

---

## 3. Prompt Engineering

A **Chain-of-Thought (CoT)** prompt instructs the LLM to behave like an experienced radiologist.

The prompt includes:

- Classification rules
- Negation handling
- Uncertainty detection
- "No Finding" logic
- Structured JSON output requirements

Example:

```text
You are a board-certified radiologist.

Carefully analyse the report.

For every condition output:

1  -> Present
0  -> Absent
-1 -> Uncertain
null -> Not Mentioned
```

---

## 4. Label Extraction

Each processed report is:

1. Loaded into memory
2. Sent to the Ollama API
3. Analysed by the selected LLM
4. Parsed into JSON
5. Saved to the output file

To minimise data loss, the system automatically saves predictions every **10 reports**.

---

## 5. Evaluation

Generated labels are compared against the manually validated dataset using:

- Accuracy
- Precision
- Recall
- True Positive Rate
- False Positive Rate

---

# 🚧 Challenges

## Medical Terminology

Radiology reports often describe the same condition using different terminology.

Example:

```text
Heart size remains unchanged.
```

This implies **Cardiomegaly is absent**, despite never explicitly mentioning the condition.

---

## Negation

Many reports contain phrases such as:

```text
No evidence of pneumothorax.
```

Prompt engineering was refined to correctly interpret negated conditions.

---

## Uncertainty

Radiology reports frequently contain uncertain language:

```text
Cannot exclude...
Possible...
Likely...
```

The prompt distinguishes uncertain findings from confirmed diagnoses.

---

## Malformed LLM Output

Occasionally, the LLM generated incomplete or invalid JSON.

To improve reliability, the system:

- Detects malformed responses
- Skips invalid outputs
- Continues processing remaining reports
- Prevents the program from crashing

---

## Hardware Constraints

The project was developed on a machine with **16 GB RAM**, requiring inference to run entirely on the CPU.

To improve robustness:

- Automatic checkpoint saving was implemented
- Recovery mechanisms were added
- Long-running inference was optimised

---

# 📈 Results

The project demonstrated that modern LLMs can successfully extract structured clinical labels from unstructured radiology reports.

Key outcomes include:

- Improved contextual reasoning
- Better handling of uncertainty
- More accurate interpretation of negation
- Successful emulation of radiologist-style reasoning through prompt engineering

---

# 💡 Skills Demonstrated

- Artificial Intelligence
- Large Language Models (LLMs)
- Prompt Engineering
- Natural Language Processing
- Python Development
- Data Processing
- JSON Processing
- API Integration
- Machine Learning Evaluation
- Software Engineering
- Error Handling
- Performance Optimisation

---

# 🚀 Future Improvements

Potential future work includes:

- GPU acceleration
- Support for larger open-source LLMs
- Retrieval-Augmented Generation (RAG)
- Fine-tuning on radiology datasets
- Batch inference optimisation
- Docker deployment
- Web application interface
- Integration with hospital information systems

---

# ⚠️ Disclaimer

This project was developed for **academic research purposes**.

The generated predictions are intended **for evaluation only** and **must not be used for clinical diagnosis or medical decision-making.**

---

# 👤 Author

**Mohit Mittal**

Bachelor of Computer Science (Advanced)  
Major in Artificial Intelligence  
University of Adelaide
