import torch
import torch.nn as nn

class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.down1 = DoubleConv(3, 32)
        self.pool1 = nn.MaxPool2d(2)
        self.down2 = DoubleConv(32, 64)
        self.pool2 = nn.MaxPool2d(2)
        
        self.bottleneck = DoubleConv(64, 128)
        
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.up_conv1 = DoubleConv(128, 64)
        self.up2 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.up_conv2 = DoubleConv(64, 32)
        
        self.out_conv = nn.Conv2d(32, 1, 1)

    def forward(self, x):
        x1 = self.down1(x)
        x2 = self.down2(self.pool1(x1))
        b = self.bottleneck(self.pool2(x2))
        
        d1 = self.up1(b)
        d1 = torch.cat([d1, x2], dim=1)
        d1 = self.up_conv1(d1)
        
        d2 = self.up2(d1)
        d2 = torch.cat([d2, x1], dim=1)
        d2 = self.up_conv2(d2)
        
        return self.out_conv(d2)