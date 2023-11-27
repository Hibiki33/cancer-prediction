import os
import sys
import h5py
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision import models
from torch import optim
import argparse
from tqdm import tqdm
from torch.utils.tensorboard.writer import SummaryWriter

from .dataset import ResNetDataset

def train(train_data_path : str, valid_data_path : str, model_save_path : str, record : bool=False):

    train_images = h5py.File(train_data_path, 'r')['x']
    train_labels = h5py.File(train_data_path, 'r')['y']
    valid_images = h5py.File(valid_data_path, 'r')['x']
    valid_labels = h5py.File(valid_data_path, 'r')['y'] 

    # Transformer
    train_transformer = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    valid_transformer = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = ResNetDataset(train_images, train_labels, train_transformer)
    valid_dataset = ResNetDataset(valid_images, valid_labels, valid_transformer)

    train_Dataloader = DataLoader(dataset=train_dataset, batch_size=128, shuffle=True,  drop_last=True)
    valid_Dataloader = DataLoader(dataset=valid_dataset, batch_size=128, shuffle=True,  drop_last=True)
    
    resnet50 = models.resnet50(pretrained=True)
    for param in resnet50.parameters():
        param.requires_grad = False
       
    resnet50.fc = nn.Linear(resnet50.fc.in_features, 2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    lr = 1e-3
    epochs = 3 

    model = resnet50.to(device)
    opt = optim.SGD(model.parameters(), lr = lr)
    model_name = os.path.join(model_save_path, 'ResNet50.h5')

    criterion = nn.CrossEntropyLoss()

    train_loss_epoch, valid_loss_epoch = [], []
    train_acc, valid_acc = [], []
    best_acc, best_acc = 0.0, 0.0

    if record:
        writer = SummaryWriter("./tensorboard/ResNet50/")

    for epoch in range(epochs):
    
        correct_train, total_train = 0, 0
        correct_valid, total_valid = 0, 0
        train_loss_C, valid_loss_C = 0.0, 0.0

        model.train()
    
        print('epoch: ' + str(epoch + 1) + ' / ' + str(epochs))  
        
        # Training Stage
        
        with tqdm(train_Dataloader, desc='Train', file=sys.stdout) as iterator:
            iter = 0
            for imgs, gts in iterator:
                imgs, gts = imgs.to(device), gts.to(device)
                opt.zero_grad()

                outputs = model(imgs)
                _, preds = torch.max(outputs, dim=1)
                loss = criterion(outputs, gts)

                loss.backward()
                opt.step()

                _, preds = torch.max(outputs, dim=1)
                total_train += gts.size(0)
                correct_train += (preds==gts).sum().item()

                train_loss_C += loss.item()
                iter += 1

            if record:
                writer.add_scalar('Loss', train_loss_C / iter, epoch)
                writer.add_scalar('Accurancy', correct_train / total_train, epoch)
            print('train loss: %.3f | train acc: %.3f' % (train_loss_C / iter, correct_train / total_train))

            # Validating Stage
            
            model.eval()

            with tqdm(valid_Dataloader, desc='Valid', file = sys.stdout) as iterator:
                iter = 0
                for imgs, gts in iterator:
                    with torch.no_grad():
                        imgs, gts = imgs.to(device), gts.to(device)
                        opt.zero_grad()

                        outputs = model(imgs)
                        _, preds = torch.max(outputs, dim=1)
                        loss = criterion(outputs, gts)


                        _, preds = torch.max(outputs, dim=1)
                        total_valid += gts.size(0)
                        correct_valid += (preds==gts).sum().item()

                        valid_loss_C += loss.item()
                        iter += 1

                print('valid loss: %.3f | valid acc: %.3f' % (valid_loss_C / iter, correct_valid / total_valid))
                
                if (correct_valid / total_valid) > best_acc:
                    best_acc = correct_valid / total_valid
                    torch.save(model.state_dict(), model_name)
                    print(f'Model Saves in {model_save_path}.')

            print('---------------------------------------------------------')                              
            train_acc.append(100 * (correct_train / total_train)) # train accuracy
            valid_acc.append(100 * (correct_valid / total_valid))  # valid accuracy
            train_loss_epoch.append(train_loss_C / iter) # train loss
            valid_loss_epoch.append(valid_loss_C / iter) # valid loss


if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data_path', type=str, required=True)
    parser.add_argument('--valid_data_path', type=str, required=True)
    parser.add_argument('--model_save_path', type=str, required=True)
    args = parser.parse_args()

    train(args.train_data_path, args.valid_data_path, args.model_save_path, True)
