import h5py
import sys
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import argparse

from .dataset import ResNetDataset

def test(test_data_path : str, model_load_path : str):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    valid_transformer = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_images = h5py.File(test_data_path, 'r')['x'] #path to folder
    test_labels = h5py.File(test_data_path, 'r')['y'] #path to folder
    test_dataset = ResNetDataset(test_images, test_labels, valid_transformer)
    test_Dataloader = DataLoader(dataset=test_dataset, batch_size=128, shuffle=True, drop_last=True)
    
    criterion = nn.CrossEntropyLoss()

    correct_test = 0
    total_test = 0
    test_loss_C = 0.0

    test_model = torch.load(model_load_path)

    with tqdm(test_Dataloader, desc = 'Test', file = sys.stdout) as iterator:
        iter = 0
        for imgs, gts in iterator:
            with torch.no_grad():
                imgs, gts = imgs.to(device), gts.to(device)

                outputs = test_model(imgs)
                _, preds = torch.max(outputs, dim=1)
                loss = criterion(outputs, gts)

                _, preds = torch.max(outputs, dim=1)
                total_test += gts.size(0)
                correct_test += (preds==gts).sum().item()

                test_loss_C += loss.item()
                iter += 1

        print('test loss: %.3f | test acc: %.3f' % (test_loss_C / iter, correct_test / total_test))


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_data_path', type=str, required=True)
    parser.add_argument('--model_load_path', type=str, required=True)
    args = parser.parse_args()
    
    test(args.test_data_path, args.model_load_path)
    