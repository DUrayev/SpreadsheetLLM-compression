# SpreadsheetLLM Compression Techniques

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Implementation of compression techniques from the **SpreadsheetLLM** framework described in:

> **SpreadsheetLLM: Encoding Spreadsheets for Large Language Models**  
> *Yuzhang Tian, Jianbo Zhao, Haoyu Dong, et al.*  
> Microsoft Research, arXiv:2407.09025 (2024)  
> [📄 Paper Link](https://arxiv.org/abs/2407.09025)

## 🎯 Implemented Techniques

### 1. **Structural Anchors for Efficient Layout Understanding**
- Identifies structural boundaries in spreadsheets
- Removes homogeneous regions that don't contribute to layout understanding
- **Results**: Up to 2.33x compression with 57.1% space saved

### 2. **Inverted Index Translation**
- Maps cell values to address ranges instead of row-by-row encoding
- Eliminates redundant encoding of repeated values
- **Results**: Up to 58.2% token reduction

### 3. **Data Format Aggregation** 
- Groups cells by data format/type using rule-based recognition
- Recognizes 9 data types: Year, Integer, Float, Percentage, Scientific notation, Date, Time, Currency, Email, Others
- **Results**: Up to 80.4% space saved

## 📊 Performance Results

| Technique | Original Tokens | Compressed | Compression Ratio | Space Saved |
|-----------|----------------|------------|------------------|-------------|
| **Structural Anchors** | 112 | 64 | 1.75x | 42.9% |
| **Inverted Index** | 55 | 23 | 2.39x | 58.2% |
| **Data Format Aggregation** | 51 | 10 | 5.10x | 80.4% |

## 🚀 Usage

**Run the Jupyter Notebook:**
```bash
jupyter notebook Implementation_of_Spreadsheet_compression_techniques.ipynb
```

The notebook contains detailed implementations, examples, and performance analysis for each compression technique.