import os
import numpy as np
from PIL import Image
import argparse


def normalize_color(file_path : str, 
                    save_path : str='./normalized'):
    '''

    Input:
        file_name: file name of image
        save_path: path to save image
    Output:
        Inorm: normalized image
    '''
    os.makedirs(save_path, exist_ok=True)

    img_names = os.listdir(file_path)
    for img_name in img_names:
        img = np.array(Image.open(file_path + img))
        normalize_staining(img, img_name, save_path=save_path)


def normalize_staining(img, name, save_path=None, io=240, alpha=1, beta=0.15):
    ''' Normalize staining appearence of H&E stained images
        
    Input:
        img: RGB input image
        io: (optional) transmitted light intensity
        
    Output:
        Inorm: normalized image
        H: hematoxylin image
        E: eosin image
    '''
             
    HERef = np.array([[0.5626, 0.2159],
                      [0.7201, 0.8012],
                      [0.4062, 0.5581]])
        
    maxCRef = np.array([1.9705, 1.0308])
    
    # define height and width of image
    h, w, c = img.shape
    
    # reshape image
    img = img.reshape((-1, 3))

    # calculate optical density
    OD = -np.log((img.astype(np.float) + 1) / io)
    
    # remove transparent pixels
    ODhat = OD[~np.any(OD < beta, axis=1)]
        
    # compute eigenvectors
    eigvals, eigvecs = np.linalg.eigh(np.cov(ODhat.T))
    
    #eigvecs *= -1
    
    #project on the plane spanned by the eigenvectors corresponding to the two 
    # largest eigenvalues    
    That = ODhat.dot(eigvecs[:,1:3])
    
    phi = np.arctan2(That[:,1],That[:,0])
    
    min_phi = np.percentile(phi, alpha)
    max_phi = np.percentile(phi, 100 - alpha)
    
    v_min = eigvecs[:,1:3].dot(np.array([(np.cos(min_phi), np.sin(min_phi))]).T)
    v_max = eigvecs[:,1:3].dot(np.array([(np.cos(max_phi), np.sin(max_phi))]).T)
    
    # a heuristic to make the vector corresponding to hematoxylin first and the 
    # one corresponding to eosin second
    if v_min[0] > v_max[0]:
        HE = np.array((v_min[:,0], v_max[:,0])).T
    else:
        HE = np.array((v_max[:,0], v_min[:,0])).T
    
    # rows correspond to channels (RGB), columns to OD values
    Y = np.reshape(OD, (-1, 3)).T
    
    # determine concentrations of the individual stains
    C = np.linalg.lstsq(HE, Y, rcond=None)[0]
    
    # normalize stain concentrations
    maxC = np.array([np.percentile(C[0,:], 99), np.percentile(C[1,:],99)])
    tmp = np.divide(maxC, maxCRef)
    C2 = np.divide(C,tmp[:, np.newaxis])
    
    # recreate the image using reference mixing matrix
    Inorm = np.multiply(io, np.exp(-HERef.dot(C2)))
    Inorm[Inorm>  255] = 254
    Inorm = np.reshape(Inorm.T, (h, w, 3)).astype(np.uint8)  
    
    # unmix hematoxylin and eosin
    H = np.multiply(io, np.exp(np.expand_dims(-HERef[:,0], axis=1).dot(np.expand_dims(C2[0,:], axis=0))))
    H[H > 255] = 254
    H = np.reshape(H.T, (h, w, 3)).astype(np.uint8)
    
    E = np.multiply(io, np.exp(np.expand_dims(-HERef[:,1], axis=1).dot(np.expand_dims(C2[1,:], axis=0))))
    E[E > 255] = 254
    E = np.reshape(E.T, (h, w, 3)).astype(np.uint8)
    
    if save_path is not None:
        Image.fromarray(Inorm).save(save_path + name)  

    return Inorm


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./')
    parser.add_argument('--save_path', type=str, default='./normalized')

    args = parser.parse_args()
    normalize_color(args.file_path, args.save_path)
