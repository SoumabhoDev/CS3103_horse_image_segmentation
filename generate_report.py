import os
import sys
import base64
import subprocess
import fitz

def encode_image(img_path):
    if not os.path.exists(img_path):
        print(f"Warning: Image not found {img_path}")
        return ""
    with open(img_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

# Pre-encode images
img_pipeline = encode_image("results/figures/pipeline_overview.png")
img_samples = encode_image("results/figures/dataset_samples.png")
img_eda = encode_image("results/figures/eda_distributions.png")
img_arch = encode_image("results/figures/architecture_comparison.png")
img_curves = encode_image("results/figures/training_curves.png")
img_metrics = encode_image("results/figures/metrics_comparison.png")
img_qual = encode_image("results/figures/qualitative_comparison_compact.png")

print("All figures successfully encoded into base64.")

