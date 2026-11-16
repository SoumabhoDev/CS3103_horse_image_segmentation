import torch
import matplotlib.pyplot as plt
from torchvision import transforms

def calculate_iou(preds, masks, threshold=0.5):
    """Calculates Intersection over Union for a batch."""
    preds = torch.sigmoid(preds) > threshold
    masks = masks > threshold
    
    intersection = (preds & masks).float().sum((1, 2, 3))
    union = (preds | masks).float().sum((1, 2, 3))
    
    # Avoid division by zero
    iou = (intersection + 1e-6) / (union + 1e-6)
    return iou.mean().item()

def show_results(baseline, unet, test_loader, device, num_images=4, save_path=None):
    """Generates the comparison plot."""
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
    
    fig, axes = plt.subplots(num_images, 4, figsize=(16, 4 * num_images))
    plt.suptitle("Image Segmentation on Unseen Weizmann Test Set", fontsize=16)
    
    for i in range(num_images):
        img_vis = inv_normalize(images[i]).cpu().permute(1, 2, 0).clamp(0, 1)
        
        axes[i, 0].imshow(img_vis)
        axes[i, 0].set_title("Input Image")
        axes[i, 1].imshow(masks[i].cpu().squeeze(), cmap='gray')
        axes[i, 1].set_title("Ground Truth Mask")
        axes[i, 2].imshow(base_preds[i].cpu().squeeze(), cmap='gray')
        axes[i, 2].set_title("Baseline CNN")
        axes[i, 3].imshow(unet_preds[i].cpu().squeeze(), cmap='gray')
        axes[i, 3].set_title("Improved U-Net")
        
        for ax in axes[i]: 
            ax.axis('off')
            
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()