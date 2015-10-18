'''
Created on Oct 20, 2014

@author: Akshay Ashwathanarayana
'''
import time

from matplotlib.pyplot import imshow, plot
from numpy import arange, shape, empty, zeros, argmin, delete
from skimage import img_as_float
from skimage.filter.edges import hsobel, vsobel
from skimage.io._io import show, imread


def dual_gradient_energy(img):
    img = img_as_float(img)
    w, h = img.shape[:2]
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    hR = hsobel(R)
    hG = hsobel(G)
    hB = hsobel(B)

    hR = hR * hR
    hG = hG * hG
    hB = hB * hB

    deltaSquareH = hR + hG + hB

    vR = vsobel(R)
    vG = vsobel(G)
    vB = vsobel(B)

    vR = vR * vR
    vG = vG * vG
    vB = vB * vB

    deltaSquareV = vR + vG + vB
    dualGradientEnergy = deltaSquareH + deltaSquareV
    return dualGradientEnergy


def plot_seam(img, seam=None):
    imshow(img)
    if seam is not None:
        c = arange(len(seam))
        plot(seam, c, "r")
    show()


def find_seam(img=None):
    energy_matrix = dual_gradient_energy(img)
    l, w = shape(energy_matrix)
    path_calc_matrix = empty([l, w], dtype=EnergyPathHolder)
    seam_array = zeros((l))
    for i in range(w):
        path_calc_matrix[1, i] = EnergyPathHolder(energy_matrix[1, i], i)
    for i in range(2, l-1):
        current_min = 0
        for j in range(1, w-2):
            min_index = j
            current_min = path_calc_matrix[i-1, j].value
            if j > 1 and path_calc_matrix[i-1, j-1].value < current_min:
                min_index = j-1
                current_min = path_calc_matrix[i-1, j-1].value
            if j < w-3 and path_calc_matrix[i-1, j+1].value < current_min:
                min_index = j+1
                current_min = path_calc_matrix[i-1, j+1].value
            energy_sum = current_min+energy_matrix[i, j]
            path_calc_matrix[i, j] = EnergyPathHolder(energy_sum, min_index)
    seam_array[l-2] = argmin(path_calc_matrix[l-2, 1:w-2])+1
    energy_cost = energy_matrix[l-2, seam_array[l-2]]
    for i in range(l-3, 0, -1):
        seam_array[i] = path_calc_matrix[i+1, int(seam_array[i+1])].parentIndex
        energy_cost = energy_cost + energy_matrix[i, int(seam_array[i])]
    seam_array[0] = seam_array[1]
    seam_array[l-1] = seam_array[l-2]
    return seam_array


def remove_seam(img, seam):
    img = img_as_float(img)
    l, w = img.shape[:2]
    img_after_removal = zeros((l, w-1, 3))
    for i in range(l):
        img_after_removal[i, :, :] = delete(img[i, :, :], seam[i], axis=0)
    return img_after_removal


class EnergyPathHolder(object):
    def __init__(self, value, parentIndex):
        self.value = value
        self.parentIndex = parentIndex

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return other.__le__(self)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.value)

    def __repr__(self, *args, **kwargs):
        return str(self.value)


def main():
    img = imread("HJoceanSmall.png")
#     imshow(img)
    reduced_img = img
    start_time = time.time()
    i = 10
    while i > 0:
        seam = find_seam(reduced_img)
        reduced_img = remove_seam(reduced_img, seam)
#         imsave(str(i), reduced_img)
        i = i-1
    stop_time = time.time()
    plot_seam(reduced_img)
    show()
    print "Time taken :", stop_time - start_time

if __name__ == '__main__':
    main()
