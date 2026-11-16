import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image

class WeizmannHorseDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.img_dir = os.path.join(root_dir, 'horse')
        self.mask_dir = os.path.join(root_dir, 'mask')
        self.images = sorted(os.listdir(self.img_dir))
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = self.images[idx]
        image = Image.open(os.path.join(self.img_dir, img_name)).convert("RGB")
        mask = Image.open(os.path.join(self.mask_dir, img_name)).convert("L")
        
        if self.transform:
            image = self.transform(image)
            
        mask = mask.resize((128, 128), Image.NEAREST)
        mask_np = np.array(mask)
        mask_tensor = torch.from_numpy(mask_np).float().unsqueeze(0)
        
        # Robust binarization
        mask_tensor = (mask_tensor > 0).float()
        return image, mask_tensor

def get_loaders(root_dir, batch_size=8, test_split=0.2):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dataset = WeizmannHorseDataset(root_dir=root_dir, transform=transform)
    test_size = int(test_split * len(dataset))
    train_size = len(dataset) - test_size
    
    # Generator ensures reproducible splits across different runs
    generator = torch.Generator().manual_seed(42)
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size], generator=generator)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=4, shuffle=False)
    
    return train_loader, test_loader