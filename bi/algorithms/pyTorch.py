import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


class PyTorchNetwork(nn.Module):
    def __init__(self, final_layers):
        super(PyTorchNetwork, self).__init__()

        self.layers = nn.Sequential(*final_layers)


    def forward(self, x):
        # x = torch.from_numpy(x)
        x = self.layers(x)

        return x



# class PyTorchDataset(Dataset):
#     def __init__(self, pandas_df, target_column):
#         super(PyTorchDataset, self).__init__()
#
#         self.X =
