import os
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt

from data_loader import get_base_datasets
from models.baseline_cnn import BaselineCNN
from models.unet import UNet

def save_visual_results(baseline, unet, test_loader, device, num_images=4, save_dir="results/figures", n=1):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"test_predictions_{n}.png")
    
    baseline.eval()
    unet.eval()
    
    images, masks = next(iter(test_loader))
    images, masks = images.to(device), masks.to(device)
    
    with torch.no_grad():
        base_preds = torch.sigmoid(baseline(images)) > 0.5
        unet_preds = torch.sigmoid(unet(images)) > 0.5

    inv_normalize = transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225]
    )
    
    # FIX 1: Add squeeze=False to force a 2D array of axes even if num_images == 1
    fig, axes = plt.subplots(num_images, 4, figsize=(16, 4 * num_images), squeeze=False)
    plt.suptitle("Model Comparison on Isolated Test Set", fontsize=18, y=1.02)
    
    for i in range(num_images):
        img_vis = inv_normalize(images[i]).cpu().permute(1, 2, 0).clamp(0, 1)
        
        axes[i, 0].imshow(img_vis)
        axes[i, 0].set_title("Input Image", fontsize=14)
        axes[i, 1].imshow(masks[i].cpu().squeeze(), cmap='gray')
        axes[i, 1].set_title("Ground Truth Mask", fontsize=14)
        axes[i, 2].imshow(base_preds[i].cpu().squeeze(), cmap='gray')
        axes[i, 2].set_title("Baseline (No Skip Conn.)", fontsize=14)
        axes[i, 3].imshow(unet_preds[i].cpu().squeeze(), cmap='gray')
        axes[i, 3].set_title("Improved U-Net", fontsize=14)
        
        for ax in axes[i]: 
            ax.axis('off')
            
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    print(f"Visualization saved to {save_path}")
    # plt.show() # Optional: You may want to comment this out in a loop so it doesn't pause execution

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    data_path = "weizmann_horse_db" if os.path.exists("weizmann_horse_db") else "data/raw/weizmann_horse_db"
    
    # Grab the isolated test dataset
    _, test_dataset = get_base_datasets(data_path)
    
    # Shuffle=True ensures you get different horses for each of your 10 output files
    test_loader = DataLoader(test_dataset, batch_size=4, shuffle=True)
    
    # Initialize models
    baseline_model = BaselineCNN().to(device)
    unet_model = UNet().to(device)
    
    # Load trained weights
    try:
        baseline_model.load_state_dict(torch.load("results/checkpoints/baseline.pth", map_location=device, weights_only=True))
        unet_model.load_state_dict(torch.load("results/checkpoints/unet.pth", map_location=device, weights_only=True))
        print("Model weights loaded successfully.")
    except FileNotFoundError:
        print("Warning: Model weights not found in results/checkpoints/. Generating visualizations with untrained weights.")

    for i in range(1, 11):
        # FIX 2: Explicitly pass i to the 'n' parameter keyword
        save_visual_results(baseline_model, unet_model, test_loader, device, n=i)