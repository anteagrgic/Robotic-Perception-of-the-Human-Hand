import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
from src import util
from src.hand import Hand
import os
import csv



#body_estimation = Body('model2/body_pose_model.pth')
hand_estimation = Hand('model2/hand_pose_model.pth')



# ubaciti slike u odgovarajuće napravljene foldere
# input za jedan_prst, otkomentirati 1. komentar za whole_hand, 2. komentar za like
folder_path = "/home/muflcima/openpose/pytorch-openpose-master/resizing/resized"
#folder_path = "/home/muflcima/openpose/pytorch-openpose-master/whole_hand"
#folder_path = "/home/muflcima/openpose/pytorch-openpose-master/like"

# za sve točke output
output_path = "/home/muflcima/openpose/pytorch-openpose-master/DataBase/data_base.csv"



#lista slika izvađena iz foldera
def load_images_from_folder(folder_path):

    images =[]

    for image in os.listdir(folder_path):
        img = cv2.imread(os.path.join(folder_path, image))
        if img is not None:
            images.append(img)

    return images



#hvata točke
def get_peaks(image):

    peaks = hand_estimation(image)
    peaks[:, 0] = np.where(peaks[:, 0]==0, peaks[:, 0], peaks[:, 0])
    peaks[:, 1] = np.where(peaks[:, 1]==0, peaks[:, 1], peaks[:, 1])

    return peaks



#potrebno je prije iscitavanja slika iz svakog file-a otkomentirati odgovarajuću liniju koda
#npr. za whole_hand, potrebno je otkomentirati 1. komentar, a za like otkomentirati 2. komentar
def build_database(folder_path, output_path):
    #otkomentirati odgovarauće countere prije svrtnje vake mape sa slikama
    #jedan prst
    counter = 0
    #like
    #counter = 1075
    #whole_hand
    #counter = 1308
    one_finger = 1
    whole_hand = 2
    like = 3
    header = ['ID', 'Label', 'Key points']
    images = load_images_from_folder(folder_path)

    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for image in images: 
            peaks = get_peaks(image)
            flattened_peaks = np.ravel(peaks)
            row = [counter, one_finger, flattened_peaks.tolist()]
            #row = [counter, whole_hand, flattened_peaks.tolist()]
            #row = [counter, like, flattened_peaks.tolist()]
            writer.writerow(row)
            counter+=1
  


def hand_draw(folder_path):

    oriImgs = load_images_from_folder(folder_path)

    for image in oriImgs:
        peaks = hand_estimation(image)
        peaks[:, 0] = np.where(peaks[:, 0]==0, peaks[:, 0], peaks[:, 0])
        peaks[:, 1] = np.where(peaks[:, 1]==0, peaks[:, 1], peaks[:, 1])
        canvas = copy.deepcopy(image)
        canvas = util.draw_handpose(canvas, [peaks])
    
        plt.imshow(canvas[:, :, [2, 1, 0]])
        plt.axis('off')
        plt.show()



hand_draw(folder_path)
build_database(folder_path, output_path)
