import torch.nn as nn

class BaselineCNN(nn.Module):
    def __init__(self):
        super(BaselineCNN, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), 
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True), 
            nn.MaxPool2d(2),
            
            nn.Conv2d(16, 32, 3, padding=1), 
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True), 
            nn.MaxPool2d(2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(32, 16, 2, stride=2), 
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(16, 1, 2, stride=2)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))