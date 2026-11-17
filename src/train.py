import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim

from data_loader import get_loaders
from models.baseline_cnn import BaselineCNN
from models.unet import UNet
from utils import calculate_iou

def train_model(model, loader, model_name, epochs=15, lr=0.005, save_dir="results/checkpoints"):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    print(f"\\n--- Training {model_name} on {device} ---")
    os.makedirs(save_dir, exist_ok=True)
    
    best_iou = 0.0
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        epoch_iou = 0
        
        for images, masks in loader:
            images, masks = images.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            epoch_iou += calculate_iou(outputs, masks)
            
        avg_loss = epoch_loss / len(loader)
        avg_iou = epoch_iou / len(loader)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:02d}/{epochs} | Loss: {avg_loss:.4f} | Train IoU: {avg_iou:.4f}")
            
        # Save best model
        if avg_iou > best_iou:
            best_iou = avg_iou
            torch.save(model.state_dict(), os.path.join(save_dir, f"{model_name}.pth"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Weizmann Horse Segmentation Models")
    parser.add_argument("--data_dir", type=str, default="weizmann_horse_db", help="Path to raw data")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    args = parser.parse_args()

    # Adjust path assuming script is run from project root or src directory
    data_path = args.data_dir if os.path.exists(args.data_dir) else "weizmann_horse_db"
    if not os.path.exists(data_path):
        data_path = os.path.join("data", "raw", "weizmann_horse_db")
        
    print(f"Loading data from: {data_path}")
    train_loader, test_loader = get_loaders(data_path, batch_size=args.batch_size)
    
    train_model(BaselineCNN(), train_loader, "baseline", epochs=args.epochs)
    train_model(UNet(), train_loader, "unet", epochs=args.epochs)