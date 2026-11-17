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

img_pipeline = encode_image("results/figures/pipeline_overview.png")
img_samples = encode_image("results/figures/dataset_samples.png")
img_eda = encode_image("results/figures/eda_distributions.png")
img_arch = encode_image("results/figures/architecture_comparison.png")
img_curves = encode_image("results/figures/training_curves.png")
img_metrics = encode_image("results/figures/metrics_comparison.png")
img_qual = encode_image("results/figures/qualitative_comparison_compact.png")

print("Building HTML report...")

# CSS styling: Classic academic paper styling
css = """
@page {
  size: A4 portrait;
  margin: 0;
}
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  padding: 0;
  font-family: 'Times New Roman', Times, Georgia, serif;
  color: #1a1a1a;
  background-color: #ffffff;
  -webkit-font-smoothing: antialiased;
}
.page {
  width: 210mm;
  height: 297mm;
  box-sizing: border-box;
  padding: 22mm 20mm 20mm 20mm;
  position: relative;
  page-break-after: always;
  overflow: hidden;
  background: #ffffff;
}
.page:last-child {
  page-break-after: avoid;
}

/* Running Headers and Footers */
.running-header {
  position: absolute;
  top: 10mm;
  left: 20mm;
  right: 20mm;
  display: flex;
  justify-content: space-between;
  font-size: 8.5pt;
  font-style: italic;
  color: #555555;
  border-bottom: 0.6pt solid #bbbbbb;
  padding-bottom: 3px;
}
.running-footer {
  position: absolute;
  bottom: 10mm;
  left: 20mm;
  right: 20mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 8.5pt;
  color: #555555;
  border-top: 0.6pt solid #bbbbbb;
  padding-top: 3px;
}
.running-footer .center {
  margin: 0 auto;
}

/* Typography */
h1.chapter-title {
  font-size: 15pt;
  font-weight: bold;
  text-align: center;
  text-transform: uppercase;
  margin-top: 0;
  margin-bottom: 12px;
  color: #000000;
  letter-spacing: 0.5px;
}
h2.section-title {
  font-size: 11.5pt;
  font-weight: bold;
  margin-top: 10px;
  margin-bottom: 4px;
  color: #111111;
  border-bottom: 0.4pt solid #e0e0e0;
  padding-bottom: 1px;
}
h3.subsection-title {
  font-size: 10.5pt;
  font-weight: bold;
  font-style: italic;
  margin-top: 7px;
  margin-bottom: 2px;
  color: #222222;
}
p {
  font-size: 9.8pt;
  line-height: 1.38;
  margin-top: 0;
  margin-bottom: 6px;
  text-align: justify;
  text-justify: inter-word;
}
ul, ol {
  font-size: 9.8pt;
  line-height: 1.35;
  margin-top: 2px;
  margin-bottom: 6px;
  padding-left: 20px;
}
li {
  margin-bottom: 3px;
  text-align: justify;
}

/* Figures and Tables */
.fig-container {
  text-align: center;
  margin: 6px 0;
}
.fig-container img {
  max-width: 100%;
  height: auto;
  border: 0.5pt solid #cccccc;
  border-radius: 2px;
}
.fig-caption {
  font-size: 8.8pt;
  font-weight: bold;
  color: #222222;
  margin-top: 3px;
  text-align: center;
}
.table-caption {
  font-size: 8.8pt;
  font-weight: bold;
  color: #222222;
  margin-bottom: 3px;
  text-align: center;
}
table.report-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8.8pt;
  margin: 5px 0 6px 0;
}
table.report-table th {
  border-top: 1.2pt solid #111111;
  border-bottom: 1pt solid #111111;
  padding: 4px 6px;
  background-color: #f7f7f7;
  font-weight: bold;
  text-align: center;
}
table.report-table td {
  border-bottom: 0.5pt solid #dddddd;
  padding: 3.5px 6px;
  text-align: center;
}
table.report-table tr:last-child td {
  border-bottom: 1.2pt solid #111111;
}

/* Equations */
.equation-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 5px 0;
  padding: 0 10px;
  font-size: 9.8pt;
  font-style: italic;
}
.equation-text {
  flex-grow: 1;
  text-align: center;
}
.equation-num {
  font-style: normal;
  font-weight: bold;
}

/* Algorithm box */
.algo-box {
  border-top: 1.2pt solid #111111;
  border-bottom: 1.2pt solid #111111;
  padding: 6px 10px;
  margin: 6px 0;
  font-size: 8.8pt;
  background-color: #fafafa;
}
.algo-title {
  font-weight: bold;
  border-bottom: 0.6pt solid #888888;
  padding-bottom: 3px;
  margin-bottom: 5px;
}
.algo-line {
  line-height: 1.35;
  font-family: 'Courier New', Courier, monospace;
}
.algo-indent {
  padding-left: 15px;
}

/* Code box */
.code-box {
  font-family: 'Courier New', Courier, monospace;
  font-size: 8.2pt;
  background: #f8f9fa;
  border: 0.6pt solid #cccccc;
  border-left: 3pt solid #333333;
  padding: 6px 8px;
  margin: 5px 0;
  line-height: 1.3;
  white-space: pre-wrap;
  color: #222222;
}

/* Title Page styling */
.title-page {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  text-align: center;
  padding: 10mm 5mm 5mm 5mm;
}
.title-univ {
  font-size: 13pt;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #111111;
}
.title-dept {
  font-size: 10.5pt;
  color: #444444;
  margin-top: 4px;
}
.title-main-box {
  margin: 25mm 0;
}
.project-type {
  font-size: 10.5pt;
  font-style: italic;
  color: #555555;
  margin-bottom: 12px;
}
.project-title {
  font-size: 16pt;
  font-weight: bold;
  line-height: 1.35;
  color: #000000;
  text-transform: uppercase;
}
.project-subtitle {
  font-size: 11pt;
  margin-top: 10px;
  color: #333333;
}
.title-meta-grid {
  display: flex;
  justify-content: space-between;
  text-align: left;
  font-size: 10pt;
  line-height: 1.45;
  margin-top: 20mm;
  padding: 0 10mm;
}
.title-date {
  font-size: 10.5pt;
  font-weight: bold;
  color: #222222;
  margin-top: 15mm;
}

/* TOC Table */
.toc-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 9.6pt;
  line-height: 1.4;
  margin-bottom: 2.5px;
}
.toc-title {
  flex-shrink: 0;
}
.toc-dots {
  flex-grow: 1;
  border-bottom: 1px dotted #888888;
  margin: 0 6px 3px 6px;
}
.toc-page {
  flex-shrink: 0;
  font-weight: bold;
}
"""

print("Writing HTML report generator...")

