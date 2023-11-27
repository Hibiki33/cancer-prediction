import torch
from torchvision import models, transforms
from PIL import Image


if __name__ == "__main__":

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    resnet50 = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    resnet50 = torch.nn.Sequential(*list(resnet50.children())[:-1])
    resnet50.to(device)

    transformer = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    input_image = Image.open("./dataset/TCGA20/normalized/0000/0000_3_42.jpg")
    input_image = transformer(input_image).unsqueeze(0).to(device)

    output_feature = resnet50(input_image)
    output_feature = output_feature.squeeze().cpu().detach().numpy()
    print(output_feature.shape)

