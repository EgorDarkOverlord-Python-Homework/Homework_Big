from PIL import Image, ImageTk  # pip install pillow
import cv2
import numpy as np
from numpy import random


def noise_image(image, percent):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if random.rand() > 1 - percent / 100:
                image[i, j] = random.randint(255, size=(3))


def noise_filtering(image, power):
    if power % 2 == 0:
        power += 1
    median = cv2.medianBlur(image, power)
    return median


def image_equalization(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.equalizeHist(image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def statistic_correction(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    output = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return output


def image_resize(image, width, height):
    image = cv2.resize(image, (width, height))
    return image


def translation(image, x, y):
    height, width = image.shape[:2]
    T = np.float32([[1, 0, x], [0, 1, y]])
    img_translation = cv2.warpAffine(image, T, (width, height))
    return img_translation


def rotation(image, angle):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, M, (width, height))
    return rotated_image


def glass_effect(image, power):
    height, width = image.shape[:2]
    dst = np.zeros(image.shape, np.uint8)
    randon_v = power
    for m in range(height - randon_v):
        for n in range(width - randon_v):
            index = random.randint(1, randon_v)
            (b, g, r) = image[m + index, n + index]
            dst[m, n] = (b, g, r)
    return dst


def motion_blur(image, degree, angle):
    image = np.array(image)
 
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
 
    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
 
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred

