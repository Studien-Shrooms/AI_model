<div align="center">
<h1>AI Model Repository</h1>
<img src="https://img.shields.io/github/last-commit/Studien-Shrooms/AI_model">
<img src="https://img.shields.io/github/languages/top/Studien-Shrooms/AI_model">
<img src="https://img.shields.io/github/languages/count/Studien-Shrooms/AI_model">
<img src="https://img.shields.io/github/repo-size/Studien-Shrooms/AI_model">
<img src="https://img.shields.io/github/stars/Studien-Shrooms/AI_model?style=social">
<br>
<br>
<b>Repository for fine-tuning and deploying AI models using LLaMA from Meta</b>
<br>
<br>
</div>

---

## Table of Contents
1. [Overview](#overview)
2. [Resources](#resources)
3. [Setup](#setup)
4. [Fine-Tuning](#fine-tuning)
5. [Example Code](#example-code)
6. [Backend Logic](#backend-logic)
7. [Datasets](#datasets)

---

## Overview
This repository contains the code and resources for fine-tuning AI models using the LLaMA architecture from Meta. The fine-tuning process was executed on Kaggle using GPU T4 x2 instances.

---

## Resources
- **Model Architecture**: LLaMA by Meta
- **Platform**: Kaggle (GPU T4 x2)
- **Dependencies**: Python, PyTorch, Transformers library
- **Documentation**: Refer to the official [LLaMA documentation](https://github.com/facebookresearch/llama).

---

## Setup
### Prerequisites
- Python 3.8 or higher
- Kaggle account with GPU access
- Required Python libraries:
  ```
  pip install torch transformers datasets
  ```

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/Studien-Shrooms/AI_model.git
   cd AI_model
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

---

## Fine-Tuning
The fine-tuning process involves the following steps:
1. Upload the dataset to Kaggle.
2. Configure the training script with the dataset path and model parameters.
3. Run the training script on Kaggle with GPU T4 x2.

Example command:
```
python train.py --model llama --dataset /path/to/dataset --epochs 5 --batch_size 16
```

---

## Example Code
Below is an example of how to test the fine-tuned model:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the fine-tuned model
model = AutoModelForCausalLM.from_pretrained("path/to/fine-tuned-model")
tokenizer = AutoTokenizer.from_pretrained("path/to/fine-tuned-model")

# Generate text
input_text = "Once upon a time"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs["input_ids"], max_length=50)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## Backend Logic
The backend logic is implemented in the `backend/` directory. Key components include:
- **API Endpoints**: RESTful APIs for model inference.
- **Deployment**: Dockerized backend for scalable deployment.
- **Scripts**:
  - `train.py`: Fine-tuning script.
  - `inference.py`: Model inference script.

---

## Datasets
The datasets used for fine-tuning are located in the `datasets/` directory. Each dataset is preprocessed and split into training, validation, and test sets.

- **Raw Data**: `datasets/raw/`
- **Processed Data**: `datasets/processed/`

Ensure the dataset format matches the requirements of the LLaMA model.

---