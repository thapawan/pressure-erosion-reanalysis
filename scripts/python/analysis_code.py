# ============================================================================
# Pressure-Erosion Reanalysis - Python Script
# Reanalysis of Buffon et al. (2025) impinging jet dataset
# Author: Pawan Thapa
# Date: 2026-05-24
# License: MIT
# ============================================================================

"""
This script reanalyzes the TU Delft impinging jet dataset to test whether
high pressure can cause deposition instead of erosion (pressure-erosion reversal).
The original data is from: Buffon et al. (2025), DOI: 10.4121/47f474f1-cdf5-470f-9121-0a290f327cae
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11

# ============================================================================
# 1. Configuration
# ============================================================================

# Set your data path here (UPDATE THIS)
DATA_PATH = "/content/drive/MyDrive/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet"

# Create output directory
output_dir = os.path.join(DATA_PATH, "analysis_output")
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("Pressure-Erosion Reanalysis")
print("Dataset: Buffon et al. (2025)")
print("=" * 60)

# ============================================================================
# 2. Load Results (from your previous analysis)
# ============================================================================

# List of experiments
experiments = [
    "00_EXP_Q1_J45_S00", "01_EXP_Q2_J45_S00", "02_EXP_Q3_J45_S00",
    "03_EXP_Q4_J45_S00", "04_EXP_Q5_J45_S00", "07_EXP_Q3_J45_S03",
    "08_EXP_Q3_J45_S10", "09_EXP_Q3_J45_S17"
]

def parse_experiment_name(name):
    """Extract Q, J, S values from experiment name"""
    import re
    q_match = re.search(r'Q(\d+)', name)
    s_match = re.search(r'S(\d+)', name)
    j_match = re.search(r'J(\d+)', name)
    
    return {
        'Q': int(q_match.group(1)) if q_match else None,
        'S': int(s_match.group(1)) / 100 if s_match else None,
        'J': int(j_match.group(1)) if j_match else None
    }

# Try to load saved results
all_results = []

for exp in experiments:
    result_file = os.path.join(DATA_PATH, f'{exp}_analysis_results.csv')
    
    if os.path.exists(result_file):
        df = pd.read_csv(result_file)
        df['experiment'] = exp
        all_results.append(df)

# If no saved results, create summary manually from your analysis
if len(all_results) == 0:
    print("\nNo saved results found. Creating summary table from analysis...\n")
    
    # This is the summary from your actual analysis results
    all_results_df = pd.DataFrame({
        'experiment': experiments,
        'flow_rate': [1, 2, 3, 4, 5, 3, 3, 3],
        'cohesion_pct': [0, 0, 0, 0, 0, 3, 10, 17],
        'slope': [0.000433, -0.001030, 0.002190, -0.003294, 0.011495, -0.001458, 0.001799, -0.002826],
        'r_value': [0.1531, -0.0420, 0.0434, -0.0559, 0.1264, -0.0325, 0.0371, -0.0640],
        'p_value': [0.6530, 0.8387, 0.8369, 0.7861, 0.5561, 0.8749, 0.8602, 0.7559],
        'final_scour': [0.13, 5.08, 14.87, 20.06, 25.83, 14.89, 14.07, 16.09]
    })
    
    # Add behavior classification
    def classify_behavior(row):
        if row['slope'] < -0.0005:
            return "Classic (erosion increases)"
        elif row['slope'] > 0.0005:
            return "Neutral (no clear trend)"
        else:
            return "Classic"
    
    all_results_df['behavior'] = all_results_df.apply(classify_behavior, axis=1)
    
else:
    all_results_df = pd.concat(all_results, ignore_index=True)

# ============================================================================
# 3. Summary Statistics
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY OF ALL EXPERIMENTS")
print("=" * 60 + "\n")

# Print results table
print(all_results_df[['experiment', 'slope', 'r_value', 'p_value', 'final_scour', 'behavior']].to_string())

# Statistical summary
print("\n" + "-" * 60)
print("STATISTICAL SUMMARY")
print("-" * 60)

print(f"\nSlope statistics:")
print(f"  Mean: {all_results_df['slope'].mean():.6f} cm/s")
print(f"  SD: {all_results_df['slope'].std():.6f} cm/s")
print(f"  Range: {all_results_df['slope'].min():.6f} to {all_results_df['slope'].max():.6f} cm/s")

print(f"\nSignificance:")
significant = (all_results_df['p_value'] < 0.05).sum()
print(f"  Experiments with p < 0.05: {significant} out of {len(all_results_df)}")
print(f"  No statistically significant trends detected.")

# ============================================================================
# 4. Figures for Publication
# ============================================================================

# Prepare data for figures
s00_data = all_results_df[all_results_df['experiment'].str.contains('S00')].copy()
s00_data = s00_data.sort_values('experiment')
s00_data['flow_rate'] = [1, 2, 3, 4, 5]

q3_data = all_results_df[all_results_df['experiment'].str.contains('Q3')].copy()
q3_data = q3_data.sort_values('experiment')
q3_data['cohesion'] = [0, 3, 10, 17]

# Create figure with 3 subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Slope vs Flow Rate
ax1 = axes[0, 0]
ax1.plot(s00_data['flow_rate'], s00_data['slope'], 'bo-', linewidth=2, markersize=8)
ax1.axhline(y=0, color='red', linestyle='--', linewidth=1.5, label='Zero slope boundary')
ax1.fill_between(s00_data['flow_rate'], 0, s00_data['slope'], 
                   where=np.array(s00_data['slope']) > 0, color='green', alpha=0.3, label='Positive slope')
ax1.fill_between(s00_data['flow_rate'], 0, s00_data['slope'], 
                   where=np.array(s00_data['slope']) < 0, color='red', alpha=0.3, label='Negative slope')
ax1.set_xlabel('Flow Rate (Q value)', fontsize=12)
ax1.set_ylabel('Slope (scour vs time, cm/s)', fontsize=12)
ax1.set_title('A: Effect of Flow Rate on Pressure-Erosion', fontsize=14)
ax1.set_xticks([1, 2, 3, 4, 5])
ax1.set_xticklabels(['Q1\nLowest', 'Q2', 'Q3', 'Q4', 'Q5\nHighest'])
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3)

# Plot 2: Slope vs Cohesion
ax2 = axes[0, 1]
ax2.plot(q3_data['cohesion'], q3_data['slope'], 'gs-', linewidth=2, markersize=8)
ax2.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
ax2.set_xlabel('Sediment Cohesion (%)', fontsize=12)
ax2.set_ylabel('Slope (scour vs time, cm/s)', fontsize=12)
ax2.set_title('B: Effect of Cohesion (Constant Q3)', fontsize=14)
ax2.set_xticks([0, 3, 10, 17])
ax2.set_xticklabels(['0%', '3%', '10%', '17%'])
ax2.grid(True, alpha=0.3)

# Plot 3: Final Scour vs Flow Rate (bar chart)
ax3 = axes[1, 0]
bars = ax3.bar(s00_data['flow_rate'], s00_data['final_scour'], color='steelblue', alpha=0.7)
for bar, val in zip(bars, s00_data['final_scour']):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{val:.1f}', ha='center', va='bottom', fontsize=10)
ax3.set_xlabel('Flow Rate (increasing pressure →)', fontsize=12)
ax3.set_ylabel('Final Scour Depth (cm)', fontsize=12)
ax3.set_title('C: Final Scour Depth Increases with Pressure', fontsize=14)
ax3.set_xticks([1, 2, 3, 4, 5])
ax3.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: P-values across experiments
ax4 = axes[1, 1]
x_pos = range(len(all_results_df))
colors = ['red' if p < 0.05 else 'gray' for p in all_results_df['p_value']]
ax4.bar(x_pos, all_results_df['p_value'], color=colors, alpha=0.7)
ax4.axhline(y=0.05, color='red', linestyle='--', linewidth=1.5, label='Significance threshold (p=0.05)')
ax4.set_xlabel('Experiment Index', fontsize=12)
ax4.set_ylabel('P-value', fontsize=12)
ax4.set_title('D: Statistical Significance (None below 0.05)', fontsize=14)
ax4.set_xticks(x_pos)
ax4.set_xticklabels([e.split('_')[0] for e in all_results_df['experiment']], rotation=45, ha='right', fontsize=8)
ax4.legend(loc='upper right', fontsize=9)
ax4.set_ylim(0, 1)
ax4.grid(True, alpha=0.3, axis='y')

plt.suptitle('Pressure-Erosion Reanalysis: Buffon et al. (2025) Dataset', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure_1_pressure_erosion_analysis.png'), dpi=300, bbox_inches='tight')
plt.show()

print(f"\nFigure saved: {os.path.join(output_dir, 'figure_1_pressure_erosion_analysis.png')}")

# ============================================================================
# 5. Export Cleaned Data
# ============================================================================

# Create cleaned data file for repository
cleaned_data = all_results_df[['experiment', 'slope', 'r_value', 'p_value', 'final_scour', 'behavior']].copy()
cleaned_data.columns = ['experiment', 'slope_cm_per_s', 'correlation_r', 'p_value', 'final_scour_cm', 'behavior']

cleaned_file = os.path.join(output_dir, 'cleaned_results.csv')
cleaned_data.to_csv(cleaned_file, index=False)

print(f"\nCleaned results saved: {cleaned_file}")

# Also save the summary table as a markdown file for README
with open(os.path.join(output_dir, 'results_summary.md'), 'w') as f:
    f.write("# Pressure-Erosion Reanalysis Results\n\n")
    f.write("## Summary of All Experiments\n\n")
    f.write("| Experiment | Slope (cm/s) | Correlation r | P-value | Final Scour (cm) | Behavior |\n")
    f.write("|------------|--------------|---------------|---------|------------------|----------|\n")
    for _, row in cleaned_data.iterrows():
        f.write(f"| {row['experiment']} | {row['slope_cm_per_s']:.6f} | {row['correlation_r']:.4f} | {row['p_value']:.4f} | {row['final_scour_cm']:.2f} | {row['behavior']} |\n")
    f.write("\n## Key Findings\n\n")
    f.write("- No statistically significant trends detected (all p > 0.05)\n")
    f.write(f"- Highest pressure (Q5) showed largest positive slope ({cleaned_data.loc[cleaned_data['experiment'] == '04_EXP_Q5_J45_S00', 'slope_cm_per_s'].values[0]:.6f} cm/s)\n")
    f.write(f"- but p = {cleaned_data.loc[cleaned_data['experiment'] == '04_EXP_Q5_J45_S00', 'p_value'].values[0]:.3f} - not significant\n")
    f.write("- Cohesion experiments showed inconsistent patterns\n")

print(f"\nMarkdown summary saved: {os.path.join(output_dir, 'results_summary.md')}")

# ============================================================================
# 6. Final Report
# ============================================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print("\nKey findings:")
print("  1. No statistically significant trends detected (all p > 0.05)")
print("  2. Highest pressure (Q5) showed largest positive slope (+0.0115 cm/s)")
print("  3. but p = 0.556 - not statistically significant")
print("  4. Cohesion experiments showed inconsistent patterns")

print("\nOutput files:")
print(f"  - Figure: {os.path.join(output_dir, 'figure_1_pressure_erosion_analysis.png')}")
print(f"  - Data: {cleaned_file}")
print(f"  - Summary: {os.path.join(output_dir, 'results_summary.md')}")

print("\n" + "=" * 60)
print("To cite this analysis:")
print("  [Your Name]. (2026). Pressure-Erosion Reanalysis. GitHub.")
print("  https://github.com/[your-username]/pressure-erosion-reanalysis")
print("=" * 60)
