

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as MSE
import cv2

from PIL import Image
import numpy as np
from scipy import signal
from scipy import ndimage
import cv2
import numpy as np




def fspecial_gauss(size, sigma):
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g/g.sum()
 
 
def ssim_1(img1, img2, cs_map=False):
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    size = 11
    sigma = 1.5
    window = fspecial_gauss(size, sigma)
    K1 = 0.01
    K2 = 0.03
    L = 255 #bitdepth of image
    C1 = (K1*L)**2
    C2 = (K2*L)**2
    mu1 = signal.fftconvolve(window, img1, mode='valid')
    mu2 = signal.fftconvolve(window, img2, mode='valid')
    mu1_sq = mu1*mu1
    mu2_sq = mu2*mu2
    mu1_mu2 = mu1*mu2
    sigma1_sq = signal.fftconvolve(window, img1*img1, mode='valid') - mu1_sq
    sigma2_sq = signal.fftconvolve(window, img2*img2, mode='valid') - mu2_sq
    sigma12 = signal.fftconvolve(window, img1*img2, mode='valid') - mu1_mu2
    if cs_map:
        return (((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*
                    (sigma1_sq + sigma2_sq + C2)), 
                (2.0*sigma12 + C2)/(sigma1_sq + sigma2_sq + C2))
    else:
        return ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*
                    (sigma1_sq + sigma2_sq + C2))
 
def mssim_1(img1, img2):

    level = 5
    weight = np.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])
    downsample_filter = np.ones((2, 2))/4.0
    im1 = img1.astype(np.float64)
    im2 = img2.astype(np.float64)
    mssim = np.array([])
    mcs = np.array([])
    for l in range(level):
        ssim_map, cs_map = ssim_1(im1, im2, cs_map=True)
        mssim = np.append(mssim, ssim_map.mean())
        mcs = np.append(mcs, cs_map.mean())
        filtered_im1 = ndimage.filters.convolve(im1, downsample_filter, 
                                                mode='reflect')
        filtered_im2 = ndimage.filters.convolve(im2, downsample_filter, 
                                                mode='reflect')
        im1 = filtered_im1[::2, ::2]
        im2 = filtered_im2[::2, ::2]
    return (np.prod(mcs[0:level-1]**weight[0:level-1])*
                    (mssim[level-1]**weight[level-1]))



#color    
origin_image_name="Lisa.bmp"
origin_image = cv2.imread(origin_image_name,1)
b, g, r = cv2.split(origin_image)
cv2.imwrite("Blue.bmp", b)
cv2.imwrite("Green.bmp", g)
cv2.imwrite("Red.bmp", r)


reconstructed_image_name="1.0_recon_median.bmp"
reconstructed_image = cv2.imread(reconstructed_image_name,1)
b, g, r = cv2.split(reconstructed_image)
cv2.imwrite("Blue_1.bmp", b)
cv2.imwrite("Green_1.bmp", g)
cv2.imwrite("Red_1.bmp", r)

msee=MSE(cv2.imread("Blue.bmp"),cv2.imread('Blue_1.bmp'))+MSE(cv2.imread("Green.bmp"),cv2.imread('Green_1.bmp'))+MSE(cv2.imread("Red.bmp"),cv2.imread('Red_1.bmp'))
psnrr=psnr(cv2.imread("Blue.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Blue_1.bmp',cv2.IMREAD_GRAYSCALE))+psnr(cv2.imread("Green.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Green_1.bmp',cv2.IMREAD_GRAYSCALE))+psnr(cv2.imread("Red.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Red_1.bmp',cv2.IMREAD_GRAYSCALE))
ssimm=ssim(cv2.imread("Blue.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Blue_1.bmp',cv2.IMREAD_GRAYSCALE))+ssim(cv2.imread("Green.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Green_1.bmp',cv2.IMREAD_GRAYSCALE))+ssim(cv2.imread("Red.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Red_1.bmp',cv2.IMREAD_GRAYSCALE))
msssimm=mssim_1(cv2.imread("Blue.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Blue_1.bmp',cv2.IMREAD_GRAYSCALE))+mssim_1(cv2.imread("Green.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Green_1.bmp',cv2.IMREAD_GRAYSCALE))+mssim_1(cv2.imread("Red.bmp",cv2.IMREAD_GRAYSCALE),cv2.imread('Red_1.bmp',cv2.IMREAD_GRAYSCALE))
print(reconstructed_image_name)
print(msee/3)  
print(psnrr/3)  
print(ssimm/3)  
print(msssimm/3)

print("use packet")
print(MSE(origin_image,reconstructed_image))  
print(psnr(origin_image,reconstructed_image))  
print(ssim(origin_image,reconstructed_image,multichannel=True))  



  
