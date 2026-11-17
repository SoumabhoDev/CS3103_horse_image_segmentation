import os
import base64
import subprocess

def encode_img(p):
    with open(p, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

logo_iitp = encode_img("results/poster_assets/iitp_logo_cropped.png")
img_arch = encode_img("results/poster_figures/fig1_unet_clean.png")
img_results = encode_img("results/poster_figures/fig2_results_clean.png")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Research Poster - Semantic Segmentation</title>
<style>
@page {{
  size: 13.333in 7.5in;
  margin: 0;
}}
* {{
  box-sizing: border-box;
}}
html, body {{
  margin: 0;
  padding: 0;
  width: 13.333in;
  height: 7.5in;
  font-family: 'Times New Roman', Times, serif;
  background-color: #ffffff;
  color: #111111;
  overflow: hidden;
  -webkit-print-color-adjust: exact;
}}

.poster-container {{
  width: 13.333in;
  height: 7.5in;
  padding: 3.5mm 6mm 3mm 6mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

/* Top Header */
.poster-header {{
  background: #f4f7fb;
  border: 1px solid #c9d7e8;
  border-radius: 4px;
  padding: 2.5mm 6mm;
  display: flex;
  align-items: center;
  height: 23mm;
}}
.header-logo {{
  height: 19mm;
  width: 19mm;
  flex-shrink: 0;
}}
.header-center {{
  text-align: center;
  flex-grow: 1;
  padding: 0 10mm;
}}
.poster-title {{
  font-size: 13.5pt;
  font-weight: bold;
  color: #0d233a;
  line-height: 1.18;
}}
.poster-authors {{
  font-size: 10pt;
  font-weight: bold;
  color: #222222;
  margin-top: 1.2mm;
}}
.poster-dept {{
  font-size: 8.8pt;
  color: #444444;
  margin-top: 0.6mm;
}}

/* Main 3-Column Layout */
.poster-body {{
  display: grid;
  grid-template-columns: 30% 39% 31%;
  gap: 4.5mm;
  height: 151mm;
  margin-top: 2.5mm;
}}

.col {{
  display: flex;
  flex-direction: column;
  gap: 2.2mm;
}}

/* Section Headings - Pill Badge Style */
.badge-title {{
  display: inline-block;
  background: #1b365d;
  color: #ffffff;
  font-size: 8.8pt;
  font-weight: bold;
  padding: 1.5px 11px;
  border-radius: 9px;
  margin-bottom: 1.2mm;
}}

.card-box {{
  background: #ffffff;
  border: 0.6px solid #d5dfec;
  border-radius: 3px;
  padding: 2mm 2.5mm;
}}

p, li {{
  font-size: 7.5pt;
  line-height: 1.25;
  color: #1a1a1a;
  text-align: justify;
  margin: 0 0 1mm 0;
}}

ul {{
  margin: 0;
  padding-left: 12px;
}}
li {{
  margin-bottom: 0.8mm;
}}

/* Callout Boxes */
.callout-problem {{
  background: #fdfaf6;
  border-left: 3px solid #d97706;
  padding: 1.5mm 2.2mm;
  font-size: 7.3pt;
  line-height: 1.22;
}}

.callout-conclusion {{
  background: #f0f7f0;
  border-left: 3px solid #2e7d32;
  padding: 1.5mm 2.2mm;
  font-size: 7.3pt;
  line-height: 1.22;
}}

/* Algorithm Box */
.algo-card {{
  border: 1px solid #1b365d;
  background: #fbfcfe;
  border-radius: 3px;
  padding: 1.8mm 2.5mm;
  font-size: 6.8pt;
  line-height: 1.2;
}}
.algo-header {{
  font-weight: bold;
  color: #1b365d;
  border-bottom: 0.6px solid #1b365d;
  padding-bottom: 0.8mm;
  margin-bottom: 1mm;
  font-size: 7pt;
}}
.algo-line {{
  font-family: 'Courier New', Courier, monospace;
  margin-bottom: 0.5mm;
}}

/* Table */
table.results-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 7pt;
  margin: 1mm 0;
}}
table.results-table th {{
  background: #e8eef7;
  color: #0d233a;
  border: 0.5px solid #b0c4de;
  padding: 2.2px 2px;
  text-align: center;
  font-weight: bold;
}}
table.results-table td {{
  border: 0.5px solid #d0d8e2;
  padding: 1.8px 2px;
  text-align: center;
}}
table.results-table tr.highlight-row {{
  background: #edf7ed;
  font-weight: bold;
  color: #1b5e20;
}}

/* Figures */
.fig-box {{
  width: 100%;
  margin: 1mm 0;
}}
.fig-box img {{
  width: 100%;
  height: auto;
  display: block;
  border: 0.5px solid #cccccc;
  border-radius: 2px;
}}
.fig-label {{
  font-size: 6.6pt;
  font-weight: bold;
  color: #222222;
  margin-top: 0.8mm;
  text-align: center;
}}

/* Footer References */
.poster-footer {{
  height: 10mm;
  border-top: 0.8px solid #b0c4de;
  padding-top: 1mm;
  display: flex;
  align-items: flex-start;
  gap: 2.5mm;
}}
.ref-title {{
  font-size: 7.2pt;
  font-weight: bold;
  color: #1b365d;
  white-space: nowrap;
}}
.ref-content {{
  font-size: 6.4pt;
  line-height: 1.2;
  color: #333333;
}}
</style>
</head>
<body>

<div class="poster-container">

  <!-- TOP HEADER BANNER (NO IMPACT LOGO) -->
  <div class="poster-header">
    <img src="{logo_iitp}" class="header-logo" alt="IIT Patna Seal">
    <div class="header-center">
      <div class="poster-title">Deep Learning-Based Semantic Segmentation of Natural Objects:<br>A Comparative Study of Baseline Autoencoders and Skip-Connected U-Net Architectures on the Weizmann Dataset</div>
      <div class="poster-authors">Soumabho Pal, Roll No: 2401AI09, soumabho_2401ai09@iitp.ac.in</div>
      <div class="poster-dept">Department of Computer Science and Engineering, Indian Institute of Technology Patna</div>
    </div>
    <!-- Clean symmetry placeholder without text -->
    <div style="width: 19mm; height: 19mm; flex-shrink: 0;"></div>
  </div>

  <!-- MAIN 3-COLUMN CONTENT -->
  <div class="poster-body">

    <!-- COLUMN 1: LEFT -->
    <div class="col">
      <div class="card-box">
        <div class="badge-title">Abstract</div>
        <p>This work explores deep learning architectures for dense pixel-level semantic segmentation of natural objects on the benchmark Weizmann Horse Database. A 4-layer Baseline CNN autoencoder is evaluated against a lightweight U-Net featuring horizontal skip connections. Evaluated on 65 unseen test images, the proposed U-Net achieves <strong>85.15% Mean IoU</strong> and <strong>91.68% Dice score</strong>, delivering an <strong>+11.11% IoU improvement</strong> over the baseline with sharp boundary reconstruction and minimal parameter overhead.</p>
      </div>

      <div class="card-box">
        <div class="badge-title">Introduction</div>
        <ul>
          <li>Semantic segmentation performs pixel-wise classification essential for autonomous robotic vision, animal monitoring, and natural scene parsing [1].</li>
          <li>Conventional autoencoders compress inputs into a narrow bottleneck, permanently destroying high-frequency spatial features (slender legs, hooves, tails) [2].</li>
          <li>Skip-connected U-Net architectures bypass the bottleneck by copying shallow encoder features to the decoder, restoring fine boundary contours without heavy backbones.</li>
        </ul>
      </div>

      <div class="card-box">
        <div class="badge-title">Problem Statement</div>
        <div class="callout-problem">
          Conventional convolutional autoencoders suffer from severe spatial information bottlenecking during aggressive downsampling, resulting in blurred object boundaries and loss of slender equine limb geometry under complex, camouflaged outdoor backgrounds.
        </div>
      </div>

      <div class="card-box">
        <div class="badge-title">Key Contributions</div>
        <ul>
          <li><strong>Edge-Preserving Preprocessing:</strong> Enforced nearest-neighbor mask interpolation, eliminating floating-point boundary artifacts caused by bilinear resizing.</li>
          <li><strong>Lightweight U-Net Design:</strong> Designed a compact U-Net (467k parameters) that avoids overfitting on moderate-sized datasets (327 images).</li>
          <li><strong>Quantitative &amp; Real-Time Gain:</strong> Attained +11.11% IoU gain (85.15% vs 74.04%) with 128 FPS inference speed on GPU.</li>
        </ul>
      </div>
    </div>

    <!-- COLUMN 2: MIDDLE -->
    <div class="col">
      <div class="card-box">
        <div class="badge-title">Methodology &amp; Proposed Architecture</div>
        <p style="margin-bottom: 1.2mm;">We formulate an end-to-end lightweight U-Net with DoubleConv blocks [Conv3x3 + BN + ReLU x2] with channel depths 32 &rarr; 64 &rarr; 128, and horizontal skip connections fusing shallow spatial maps directly into transposed convolutional decoder stages.</p>
        <div class="fig-box">
          <img src="{img_arch}" alt="Architecture Comparison">
          <div class="fig-label">Figure 1: Architectural Comparison: Baseline Autoencoder vs Proposed Lightweight U-Net</div>
        </div>
      </div>

      <div class="algo-card">
        <div class="algo-header">Algorithm 1: Supervised Semantic Segmentation Training with Adam and BCE with Logits</div>
        <div class="algo-line"><strong>Require:</strong> Dataset <i>D</i> = {{(<i>x</i><sub><i>i</i></sub>, <i>y</i><sub><i>i</i></sub>)}}, Epochs <i>E</i>=100, Batch size <i>B</i>=4, lr <i>η</i>=0.005, Model parameters <b>θ</b></div>
        <div class="algo-line"><strong>Ensure:</strong> Optimal model weights <b>θ</b>* maximizing validation IoU</div>
        <div class="algo-line">1. Partition <i>D</i> into 80% train (262 samples) and 20% test (65 samples) with fixed seed 42.</div>
        <div class="algo-line">2. Preprocess images with ImageNet normalization; binarize masks via nearest-neighbor resizing.</div>
        <div class="algo-line">3. Initialize Lightweight U-Net with DoubleConv blocks and horizontal skip connections.</div>
        <div class="algo-line">4. <strong>for</strong> epoch = 1 <strong>to</strong> <i>E</i> <strong>do</strong>: compute BCEWithLogitsLoss, backpropagate gradients, update weights via Adam.</div>
        <div class="algo-line">5. Monitor validation IoU; checkpoint the best model weights <b>θ</b>*.</div>
        <div class="algo-line">6. Evaluate test set across IoU, Dice, Pixel Accuracy, and Precision/Recall. Return <b>θ</b>*.</div>
      </div>
    </div>

    <!-- COLUMN 3: RIGHT -->
    <div class="col">
      <div class="card-box">
        <div class="badge-title">Result and Discussion</div>
        <div style="font-size: 6.8pt; font-weight: bold; margin-bottom: 0.6mm;">Table 1: Proposed Model Results Compared to Baseline (Isolated Test Set N=65)</div>
        <table class="results-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>IoU</th>
              <th>Dice</th>
              <th>Pixel Acc</th>
              <th>Precision</th>
              <th>Recall</th>
              <th>Params</th>
              <th>Gain</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Baseline CNN</td>
              <td>74.04%</td>
              <td>84.54%</td>
              <td>92.68%</td>
              <td>84.56%</td>
              <td>85.27%</td>
              <td>141,105</td>
              <td>—</td>
            </tr>
            <tr class="highlight-row">
              <td>Proposed (U-Net)</td>
              <td>85.15%</td>
              <td>91.68%</td>
              <td>95.99%</td>
              <td>92.24%</td>
              <td>91.69%</td>
              <td>467,809</td>
              <td>+11.11%</td>
            </tr>
          </tbody>
        </table>

        <div class="fig-box">
          <img src="{img_results}" alt="Results Visualizations">
          <div class="fig-label">Figure 2: Loss/IoU Convergence Curves &amp; Qualitative Test Predictions</div>
        </div>
      </div>

      <div class="card-box">
        <div class="badge-title">Conclusion</div>
        <div class="callout-conclusion">
          The proposed Lightweight U-Net significantly enhances semantic segmentation accuracy on natural scenes, achieving <strong>85.15% IoU</strong> and <strong>91.68% Dice (+11.11% gain)</strong>, proving that skip connections are indispensable for recovering fine structural equine contours.
        </div>
      </div>
    </div>

  </div>

  <!-- FOOTER REFERENCES -->
  <div class="poster-footer">
    <div class="ref-title">References:</div>
    <div class="ref-content">
      [1] Ronneberger, O., Fischer, P., &amp; Brox, T. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. <em>MICCAI</em>, pp. 234–241.<br>
      [2] Long, J., Shelhamer, E., &amp; Darrell, T. (2015). Fully Convolutional Networks for Semantic Segmentation. <em>CVPR</em>, pp. 3431–3440.<br>
      [3] Borenstein, E. &amp; Ullman, S. (2008). Combined top-down and bottom-up segmentation. <em>IEEE TPAMI</em>, 30(12), 2109–2125.
    </div>
  </div>

</div>

</body>
</html>
"""

with open("poster.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated fitted poster.html successfully.")
