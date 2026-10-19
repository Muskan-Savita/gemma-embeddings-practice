# Gemma Embeddings Practice
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Muskan-Savita/gemma-embeddings-practice/blob/main/notebooks/gemma-embeddings-practice.ipynb)
This project teaches how to create text embeddings with Gemma 2, sanitize personal data (PII) before embedding, and run semantic search with FAISS.

## Project structure

```
gemma-embeddings-practice/
├── app/
│   ├── __init__.py
│   └── detection.py   # PII detection (regex + Luhn check) and sanitize
├── .gitignore
└── README.md
```

## What was done

1. **PII detection:** Email, phone, SSN, IPv4, and credit card (validated with the Luhn check) are detected with regex.
2. **Sanitize:** Detected PII is replaced with tokens such as `<EMAIL>` and `<PHONE>`.
3. **Embedding:** Embeddings are created with Gemma 2 (`google/gemma-2-2b`) using mean pooling.
4. **Semantic search:** Top-k search with cosine similarity using FAISS `IndexFlatIP`.
5. **Evaluation:** Gemma 2 was compared with `all-MiniLM-L6-v2` using top-3 accuracy.

## Results (small test set, 5 sentences)

| Model | Top-3 accuracy |
|---|---|
| Gemma 2 2B (mean pooling) | 0.8 |
| all-MiniLM-L6-v2 | 1.0 |

## Results (20 documents, 10 queries)

| Model | Top-3 accuracy |
|---|---|
| Gemma 2 2B (mean pooling) | 0.5 |
| all-MiniLM-L6-v2 | 0.9 |

The dataset is small and custom-made, so these numbers are a rough comparison, not a benchmark. The Gemma results show that mean pooling on a generative model is much weaker than a dedicated embedding model for this task.

## Setup

1. Accept the license for [google/gemma-2-2b](https://huggingface.co/google/gemma-2-2b) on Hugging Face.
2. Create a Hugging Face token (Read access is enough).
3. Choose the T4 GPU in Colab.
4. Save the token in Colab Secrets as `HF_TOKEN`.
5. Run the notebook cells in order.

## Privacy rule

Embeddings are always created from **sanitized text**. Raw PII is never stored in the vector index.

## Limitations

- Regex detection covers only some PII types. NER (names, addresses) is not included yet.
- The test set is small. Accurate evaluation needs 50+ labeled sentences.
- Embeddings can still leak some information about their input.
