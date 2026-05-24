# Pressure-Erosion Reanalysis

**A reproducible reanalysis of the Buffon et al. (2025) impinging jet dataset**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

This repository contains code and processed data from a reanalysis of the impinging jet erosion experiments published by Buffon et al. (2025) in *Water Resources Research*.

**Main question tested:** Does high fluid pressure ever cause deposition instead of erosion? (Pressure-erosion reversal hypothesis)

**Bottom line:** No statistical evidence for reversal was found (all p > 0.05), but the reanalysis workflow and baseline results are shared here for transparency and reproducibility.

## Data Source

- **Original dataset:** Buffon, P., Uijttewaal, W.S.J., Valero, D., & Franca, M.J. (2025)
- **DOI:** [10.4121/47f474f1-cdf5-470f-9121-0a290f327cae](https://doi.org/10.4121/47f474f1-cdf5-470f-9121-0a290f327cae)
- **License:** CC BY 4.0

## Repository Contents

| File | Description |
|------|-------------|
| `analysis_code.R` | R script for loading and analyzing all experiments |
| `analysis_code.py` | Python script (alternative) |
| `cleaned_data.csv` | Processed data ready for analysis |
| `results_summary.csv` | Final results for all 9 experiments |

## Experiments Analyzed

| Code | Flow Rate (Q) | Cohesion (S) | Jet Angle (J) |
|------|---------------|--------------|---------------|
| 00_EXP_Q1_J45_S00 | Q1 (lowest) | 0% | 45° |
| 01_EXP_Q2_J45_S00 | Q2 | 0% | 45° |
| 02_EXP_Q3_J45_S00 | Q3 | 0% | 45° |
| 03_EXP_Q4_J45_S00 | Q4 | 0% | 45° |
| 04_EXP_Q5_J45_S00 | Q5 (highest) | 0% | 45° |
| 07_EXP_Q3_J45_S03 | Q3 | 3% | 45° |
| 08_EXP_Q3_J45_S10 | Q3 | 10% | 45° |
| 09_EXP_Q3_J45_S17 | Q3 | 17% | 45° |

## Key Results Summary

| Experiment | Slope (cm/s) | P-value | Behavior |
|------------|--------------|---------|----------|
| Q1_S00 | +0.00043 | 0.653 | Neutral |
| Q2_S00 | -0.00103 | 0.839 | Classic |
| Q3_S00 | +0.00219 | 0.837 | Neutral |
| Q4_S00 | -0.00329 | 0.786 | Classic |
| Q5_S00 | +0.01150 | 0.556 | Neutral |
| Q3_S03 | -0.00146 | 0.875 | Classic |
| Q3_S10 | +0.00180 | 0.860 | Neutral |
| Q3_S17 | -0.00283 | 0.756 | Classic |

> **Note:** No p-value < 0.05. None of the trends are statistically significant.

## How to Run the Code

### Option 1: R 

```r
# Install required packages
install.packages(c("tidyverse", "ggplot2", "scales"))

# Run the analysis
source("analysis_code.R")

### Option 1: Python

pip install pandas numpy matplotlib scipy
python analysis_code.py

Buffon, P., Uijttewaal, W.S.J., Valero, D., & Franca, M.J. (2025). 
Dataset underlying "Evolution of erosion and deposition induced by 
an impinging jet to manage sediment". 4TU.ResearchData. 
https://doi.org/10.4121/47f474f1-cdf5-470f-9121-0a290f327cae

[Your Name]. (2026). Pressure-Erosion Reanalysis. GitHub. 
https://github.com/[your-username]/pressure-erosion-reanalysis
