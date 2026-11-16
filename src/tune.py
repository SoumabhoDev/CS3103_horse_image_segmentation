import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import KFold
import numpy as np

from data_loader import get_base_datasets
from models.unet import UNet
from utils import calculate_iou

def tune_hyperparameters(dataset, k_folds=3, epochs=10):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Grid search space
    learning_rates = [1e-3, 5e-4]
    batch_sizes = [4, 8]
    
    best_iou = 0.0
    best_params = {}
    
    kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    
    print(f"Starting Grid Search with {k_folds}-Fold Cross Validation...")
    
    for lr in learning_rates:
        for bs in batch_sizes:
            fold_ious = []
            print(f"\nTesting LR: {lr} | Batch Size: {bs}")
            
            for fold, (train_idx, val_idx) in enumerate(kf.split(np.arange(len(dataset)))):
                train_sub = Subset(dataset, train_idx)
                val_sub = Subset(dataset, val_idx)
                
                train_loader = DataLoader(train_sub, batch_size=bs, shuffle=True)
                val_loader = DataLoader(val_sub, batch_size=bs, shuffle=False)
                
                model = UNet().to(device)
                criterion = nn.BCEWithLogitsLoss()
                optimizer = optim.Adam(model.parameters(), lr=lr)
                
                # Train fold
                model.train()
                for epoch in range(epochs):
                    for images, masks in train_loader:
                        images, masks = images.to(device), masks.to(device)
                        optimizer.zero_grad()
                        outputs = model(images)
                        loss = criterion(outputs, masks)
                        loss.backward()
                        optimizer.step()
                
                # Evaluate fold
                model.eval()
                val_iou = 0
                with torch.no_grad():
                    for images, masks in val_loader:
                        images, masks = images.to(device), masks.to(device)
                        outputs = model(images)
                        val_iou += calculate_iou(outputs, masks)
                
                avg_val_iou = val_iou / len(val_loader)
                fold_ious.append(avg_val_iou)
                print(f"  Fold {fold+1} IoU: {avg_val_iou:.4f}")
            
            mean_cv_iou = np.mean(fold_ious)
            print(f"-> Mean CV IoU for LR {lr}, BS {bs}: {mean_cv_iou:.4f}")
            
            if mean_cv_iou > best_iou:
                best_iou = mean_cv_iou
                best_params = {'lr': lr, 'batch_size': bs}
                
    print("\n=========================================")
    print(f"Optimal Parameters Found:")
    print(f"Learning Rate: {best_params['lr']}")
    print(f"Batch Size: {best_params['batch_size']}")
    print(f"Expected Validation IoU: {best_iou:.4f}")
    print("=========================================")
    return best_params

if __name__ == "__main__":
    data_path = "weizmann_horse_db" if os.path.exists("weizmann_horse_db") else "data/raw/weizmann_horse_db"
    train_val_dataset, _ = get_base_datasets(data_path)
    
    # Run tuning
    optimal_params = tune_hyperparameters(train_val_dataset)