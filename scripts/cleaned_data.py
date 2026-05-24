
---

## 📊 Step 3: Export Cleaned Data as CSV (Python)

Run this in your Google Colab to export the cleaned data:

```python
# ============================================================================
# EXPORT CLEANED DATA AS CSV FOR YOUR REPOSITORY
# ============================================================================

import pandas as pd
import numpy as np
from google.colab import drive

drive.mount('/content/drive')

# Path to your data
base_path = '/content/drive/MyDrive/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet'

# Create a list to store all cleaned data
all_cleaned_data = []

# List of experiments
experiments = [
    "00_EXP_Q1_J45_S00", "01_EXP_Q2_J45_S00", "02_EXP_Q3_J45_S00",
    "03_EXP_Q4_J45_S00", "04_EXP_Q5_J45_S00", "07_EXP_Q3_J45_S03",
    "08_EXP_Q3_J45_S10", "09_EXP_Q3_J45_S17"
]

for exp in experiments:
    print(f"Processing {exp}...")
    
    # Load results CSV if it exists
    result_file = os.path.join(base_path, f'{exp}_analysis_results.csv')
    if os.path.exists(result_file):
        df = pd.read_csv(result_file)
        all_cleaned_data.append(df)
    else:
        print(f"  No results file for {exp}")

# Combine all results
if all_cleaned_data:
    final_results = pd.concat(all_cleaned_data, ignore_index=True)
    
    # Select and rename columns for clarity
    final_results = final_results[[
        'experiment', 'slope', 'r_value', 'p_value', 
        'final_scour', 'behavior', 'reversal_score'
    ]]
    
    # Rename columns
    final_results.columns = [
        'experiment', 'slope_cm_per_s', 'correlation_r', 
        'p_value', 'final_scour_cm', 'behavior', 'reversal_score'
    ]
    
    # Save to CSV
    output_file = 'pressure_erosion_reanalysis_results.csv'
    final_results.to_csv(output_file, index=False)
    
    print(f"\n✅ Saved: {output_file}")
    print(f"   Shape: {final_results.shape}")
    print(f"\nPreview:")
    print(final_results.head())
    
    # Also save a more detailed version with time series data
    # This part saves the actual bed change data for the highest pressure experiment (Q5)
    # You'll need to run your original analysis code first to have ARR_bed, X, time_data
    
    print("\n" + "="*50)
    print("Next: Download these files to your computer")
    print("="*50)
    print("1. Click the folder icon in Colab left sidebar")
    print("2. Find pressure_erosion_reanalysis_results.csv")
    print("3. Right-click → Download")
    print("4. Upload to your GitHub repository")
    
else:
    print("No result files found. Run the analysis first.")
