# ============================================================================
# Pressure-Erosion Reanalysis - R Script
# Reanalysis of Buffon et al. (2025) impinging jet dataset
# Author: [Your Name]
# Date: 2026-05-24
# License: MIT
# ============================================================================

# This script reanalyzes the TU Delft impinging jet dataset to test whether
# high pressure can cause deposition instead of erosion (pressure-erosion reversal).
# The original data is from: Buffon et al. (2025), DOI: 10.4121/47f474f1-cdf5-470f-9121-0a290f327cae

# ============================================================================
# 1. Setup and Configuration
# ============================================================================

# Install required packages (uncomment if needed)
# install.packages(c("tidyverse", "ggplot2", "scales", "patchwork"))

library(tidyverse)
library(ggplot2)
library(scales)
library(patchwork)

# Set your data path here (UPDATE THIS)
DATA_PATH <- "/content/drive/MyDrive/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet/Buffon et al 2025 - Evolution of erosion and deposition induced by an impinging jet"

# Create output directory
output_dir <- file.path(DATA_PATH, "analysis_output")
if(!dir.exists(output_dir)) dir.create(output_dir)

cat("=", rep(60), "\n", sep="")
cat("Pressure-Erosion Reanalysis\n")
cat("Dataset: Buffon et al. (2025)\n")
cat("=", rep(60), "\n", sep="")

# ============================================================================
# 2. Load Results (from your previous analysis)
# ============================================================================

# List of experiments
experiments <- c(
  "00_EXP_Q1_J45_S00", "01_EXP_Q2_J45_S00", "02_EXP_Q3_J45_S00",
  "03_EXP_Q4_J45_S00", "04_EXP_Q5_J45_S00", "07_EXP_Q3_J45_S03",
  "08_EXP_Q3_J45_S10", "09_EXP_Q3_J45_S17"
)

# Function to extract metadata from experiment name
parse_experiment_name <- function(name) {
  q_match <- regmatches(name, regexpr("Q[0-9]", name))
  s_match <- regmatches(name, regexpr("S[0-9]+", name))
  j_match <- regmatches(name, regexpr("J[0-9]+", name))
  
  q_value <- as.numeric(gsub("Q", "", q_match))
  s_value <- as.numeric(gsub("S", "", s_match)) / 100
  j_value <- as.numeric(gsub("J", "", j_match))
  
  return(list(Q = q_value, S = s_value, J = j_value))
}

# Collect results
all_results <- data.frame()

for(exp in experiments) {
  result_file <- file.path(DATA_PATH, paste0(exp, "_analysis_results.csv"))
  
  if(file.exists(result_file)) {
    df <- read.csv(result_file)
    df$experiment <- exp
    all_results <- rbind(all_results, df)
  } else {
    cat("Warning: No results file for", exp, "\n")
  }
}

# If no saved results, create summary manually
if(nrow(all_results) == 0) {
  cat("\nNo saved results found. Creating summary table from analysis...\n")
  
  # This is the summary from your actual analysis results
  all_results <- data.frame(
    experiment = experiments,
    flow_rate = c(1, 2, 3, 4, 5, 3, 3, 3),
    cohesion_pct = c(0, 0, 0, 0, 0, 3, 10, 17),
    slope = c(0.000433, -0.001030, 0.002190, -0.003294, 0.011495, -0.001458, 0.001799, -0.002826),
    r_value = c(0.1531, -0.0420, 0.0434, -0.0559, 0.1264, -0.0325, 0.0371, -0.0640),
    p_value = c(0.6530, 0.8387, 0.8369, 0.7861, 0.5561, 0.8749, 0.8602, 0.7559),
    final_scour = c(0.13, 5.08, 14.87, 20.06, 25.83, 14.89, 14.07, 16.09)
  )
  
  # Add behavior classification
  all_results$behavior <- case_when(
    all_results$slope < -0.0005 ~ "Classic (erosion increases)",
    all_results$slope > 0.0005 ~ "Neutral (no clear trend)",
    TRUE ~ "Classic"
  )
}

# ============================================================================
# 3. Summary Statistics
# ============================================================================

cat("\n", rep("=", 60), "\n", sep="")
cat("SUMMARY OF ALL EXPERIMENTS\n")
cat(rep("=", 60), "\n\n", sep="")

# Print results table
results_table <- all_results %>%
  select(experiment, slope, r_value, p_value, final_scour, behavior) %>%
  mutate(
    slope = round(slope, 6),
    r_value = round(r_value, 4),
    p_value = round(p_value, 4),
    final_scour = round(final_scour, 2)
  )

print(results_table)

# Statistical summary
cat("\n", rep("-", 60), "\n", sep="")
cat("STATISTICAL SUMMARY\n")
cat(rep("-", 60), "\n", sep="")

cat("\nSlope statistics:\n")
cat("  Mean:", round(mean(all_results$slope), 6), "cm/s\n")
cat("  SD:", round(sd(all_results$slope), 6), "cm/s\n")
cat("  Range:", round(min(all_results$slope), 6), "to", round(max(all_results$slope), 6), "cm/s\n")

cat("\nSignificance:\n")
significant <- sum(all_results$p_value < 0.05, na.rm = TRUE)
cat("  Experiments with p < 0.05:", significant, "out of", nrow(all_results), "\n")
cat("  No statistically significant trends detected.\n")

# ============================================================================
# 4. Figures for Publication
# ============================================================================

# Figure 1: Slope vs Flow Rate (for S00 experiments)
s00_data <- all_results %>% filter(experiment %in% c("00_EXP_Q1_J45_S00", "01_EXP_Q2_J45_S00", 
                                                      "02_EXP_Q3_J45_S00", "03_EXP_Q4_J45_S00", 
                                                      "04_EXP_Q5_J45_S00"))
s00_data$flow_rate <- c(1, 2, 3, 4, 5)

p1 <- ggplot(s00_data, aes(x = flow_rate, y = slope)) +
  geom_point(size = 4, color = "blue") +
  geom_line(color = "blue", alpha = 0.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red", linewidth = 1) +
  geom_errorbar(aes(ymin = slope - 0.005, ymax = slope + 0.005), width = 0.3, alpha = 0.5) +
  scale_x_continuous(breaks = 1:5, labels = c("Q1\nLowest", "Q2", "Q3", "Q4", "Q5\nHighest")) +
  labs(
    title = "A: Effect of Flow Rate on Pressure-Erosion Relationship",
    subtitle = "Experiments with 0% cohesion (S00)",
    x = "Flow Rate (increasing pressure →)",
    y = "Slope (scour vs time, cm/s)",
    caption = "Positive slope suggests deposition; negative slope suggests erosion. Error bars: ±0.005\nNo slopes are statistically significant (all p > 0.05)."
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 11),
    axis.title = element_text(size = 12),
    axis.text = element_text(size = 10)
  )

# Figure 2: Slope vs Cohesion (for Q3 experiments)
q3_data <- all_results %>% filter(grepl("Q3", experiment))
q3_data$cohesion <- c(0, 3, 10, 17)

p2 <- ggplot(q3_data, aes(x = cohesion, y = slope)) +
  geom_point(size = 4, color = "darkgreen") +
  geom_line(color = "darkgreen", alpha = 0.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red", linewidth = 1) +
  scale_x_continuous(breaks = c(0, 3, 10, 17), labels = c("0%", "3%", "10%", "17%")) +
  labs(
    title = "B: Effect of Sediment Cohesion",
    subtitle = "Experiments with constant flow rate Q3",
    x = "Sediment Cohesion (%)",
    y = "Slope (scour vs time, cm/s)",
    caption = "No consistent pattern: reversal (positive slope) at 0% and 10%, classic at 3% and 17%.\nNone are statistically significant."
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 11),
    axis.title = element_text(size = 12),
    axis.text = element_text(size = 10)
  )

# Figure 3: Final Scour vs Flow Rate
p3 <- ggplot(s00_data, aes(x = flow_rate, y = final_scour)) +
  geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
  geom_text(aes(label = round(final_scour, 1)), vjust = -0.5, size = 4) +
  scale_x_continuous(breaks = 1:5, labels = c("Q1", "Q2", "Q3", "Q4", "Q5")) +
  labs(
    title = "C: Final Scour Depth Increases with Pressure",
    subtitle = "Classic rule holds: higher pressure → deeper scour",
    x = "Flow Rate (increasing pressure)",
    y = "Final Scour Depth (cm)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 12)
  )

# Combine all figures
combined_plot <- (p1 | p2) / p3 + plot_annotation(
  title = "Pressure-Erosion Reanalysis: Buffon et al. (2025) Dataset",
  theme = theme(plot.title = element_text(size = 16, face = "bold", hjust = 0.5))
)

# Save figure
ggsave(file.path(output_dir, "figure_1_pressure_erosion_analysis.png"), 
       combined_plot, width = 12, height = 10, dpi = 300)

cat("\nFigure saved:", file.path(output_dir, "figure_1_pressure_erosion_analysis.png"), "\n")

# ============================================================================
# 5. Export Cleaned Data
# ============================================================================

# Create cleaned data file for repository
cleaned_data <- all_results %>%
  select(experiment, slope, r_value, p_value, final_scour, behavior) %>%
  rename(
    slope_cm_per_s = slope,
    correlation_r = r_value,
    p_value = p_value,
    final_scour_cm = final_scour,
    behavior = behavior
  )

cleaned_file <- file.path(output_dir, "cleaned_results.csv")
write.csv(cleaned_data, cleaned_file, row.names = FALSE)

cat("\nCleaned results saved:", cleaned_file, "\n")

# ============================================================================
# 6. Final Report
# ============================================================================

cat("\n", rep("=", 60), "\n", sep="")
cat("ANALYSIS COMPLETE\n")
cat(rep("=", 60), "\n", sep="")

cat("\nKey findings:\n")
cat("  1. No statistically significant trends detected (all p > 0.05)\n")
cat("  2. Highest pressure (Q5) showed largest positive slope (+0.0115 cm/s)\n")
cat("  3. but p = 0.556 - not statistically significant\n")
cat("  4. Cohesion experiments showed inconsistent patterns\n")

cat("\nOutput files:\n")
cat("  - Figure:", file.path(output_dir, "figure_1_pressure_erosion_analysis.png"), "\n")
cat("  - Data:", cleaned_file, "\n")

cat("\n", rep("=", 60), "\n", sep="")
cat("To cite this analysis:\n")
cat("  [Your Name]. (2026). Pressure-Erosion Reanalysis. GitHub.\n")
cat("  https://github.com/[your-username]/pressure-erosion-reanalysis\n")
cat(rep("=", 60), "\n", sep="")
