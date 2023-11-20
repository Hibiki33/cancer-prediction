import h5py
import numpy as np
import os, torch, torchvision, random
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import Dataset, random_split, DataLoader
from torchvision.datasets import ImageFolder
from torchvision import models
from torch import optim
from torchsummary import summary

train_images = h5py.File('path to folder', 'r')['x'] #path to folder
train_labels = h5py.File('path to folder', 'r')['y'] #path to folder
valid_images = h5py.File('path to folder', 'r')['x'] #path to folder
valid_labels = h5py.File('path to folder', 'r')['y'] #path to folder
test_images = h5py.File('path to folder', 'r')['x'] #path to folder
test_labels = h5py.File('path to folder', 'r')['y'] #path to folder

print('train count: ', len(train_images))
print('valid count: ', len(valid_images))
print('test count: ', len(test_images))


class Dataset(Dataset):
  
    def __init__(self, images, labels, transform):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):

        image = self.transform(self.images[idx]) # Transform image
        label = np.squeeze(self.labels[idx])
                
        return image, label # return 模型訓練所需的資訊
    

normalize = transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])

# Transformer
train_transformer = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    normalize
])
 
valid_transformer = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),  
    transforms.ToTensor(),
    normalize
])

train_dataset = Dataset(train_images, train_labels, train_transformer)
valid_dataset = Dataset(valid_images, valid_labels, valid_transformer)
test_dataset = Dataset(test_images, test_labels, valid_transformer)

train_Dataloader = DataLoader(dataset = train_dataset, batch_size = 128, shuffle = True,  drop_last = True)
valid_Dataloader = DataLoader(dataset = valid_dataset, batch_size = 128, shuffle = True,  drop_last = True)
test_Dataloader = DataLoader(dataset = test_dataset, batch_size = 128, shuffle = True,  drop_last = True)

resnet50 = models.resnet50(pretrained=True)

for param in resnet50.parameters():
    param.requires_grad = False

in_features = resnet50.fc.in_features    
resnet50.fc = nn.Linear(in_features, 2)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

lr = 1e-3
epochs = 3 
save_path = 'save path' #please input path

model = resnet50.to(device)
opt = optim.SGD(model.parameters(), lr = lr)
model_name = os.path.join(save_path, 'ResNet50.h5')

# Loss function
criterion = nn.CrossEntropyLoss()

train_loss_epoch, valid_loss_epoch = [], []
train_acc, valid_acc = [], []
best_acc, best_auc = 0.0, 0.0

import sys
from tqdm import tqdm

if __name__ == '__main__':    
  
  for epoch in range(epochs):
  
    
    correct_train, total_train = 0, 0
    correct_valid, total_valid = 0, 0
    train_loss_C, valid_loss_C = 0.0, 0.0

    model.train()
  
    print('epoch: ' + str(epoch + 1) + ' / ' + str(epochs))  
    
    # ---------------------------
    # Training Stage
    # ---------------------------
    
    with tqdm(train_Dataloader, desc = 'Train', file = sys.stdout) as iterator:
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
      
      print('train loss: %.3f | train acc: %.3f' % \
            (train_loss_C / iter, correct_train / total_train))

    
    # --------------------------
    # Validating Stage
    # --------------------------
    
    model.eval() # 設定 train 或 eval

    with tqdm(valid_Dataloader, desc = 'Valid', file = sys.stdout) as iterator:
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

        print('valid loss: %.3f | valid acc: %.3f' % \
                (valid_loss_C / iter, correct_valid / total_valid))
        
        if((correct_valid / total_valid) > best_acc):
            best_acc = correct_valid / total_valid
            torch.save(model.state_dict(), model_name)
            print('Model Save!!')

    print('---------------------------------------------------------')                              
    train_acc.append(100 * (correct_train / total_train)) # train accuracy
    valid_acc.append(100 * (correct_valid / total_valid))  # valid accuracy
    train_loss_epoch.append(train_loss_C / iter) # train loss
    valid_loss_epoch.append(valid_loss_C / iter) # valid loss


import matplotlib.pyplot as plt

plt.figure()

plt.plot(train_loss_epoch) # plot your loss
plt.plot(valid_loss_epoch)

plt.title('Loss')
plt.ylabel('loss'), plt.xlabel('epoch')
plt.legend(['train', 'valid'], loc = 'upper left')
plt.show()

plt.figure()

plt.plot(train_acc) # plot your training accuracy
plt.plot(valid_acc) # plot your testing accuracy

plt.title('Accuracy')
plt.ylabel('acc (%)'), plt.xlabel('epoch')
plt.legend(['train', 'valid'], loc = 'upper left')
plt.show()

test_model = resnet50
test_model.eval()
test_model.load_state_dict(torch.load('path to ResNet50 h5')) # path to resnet 50 


if __name__ == '__main__':  
  for epoch in range(1):
  
    correct_test, total_test, test_loss_C = 0, 0, 0.0

    # --------------------------
    # Testing Stage
    # --------------------------
    
    

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

        print('test loss: %.3f | test acc: %.3f' % \
                (test_loss_C / iter, correct_test / total_test))
