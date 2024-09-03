import numpy as np
import csv

i_origin = 0 # keypoint index representing the origin
i_scale = 9 #  distance between origin and this keypoint will be used for scale


f = open('data_base.csv', 'r')
csvreader = csv.reader(f)
next(csvreader, None) #skip header

keypoints_array = []
keypoints_array_transformed = []

label_array = []
id_array = []

for row in csvreader:

    label = row[1]
    label_array.append(label)

    id = row[0]
    id_array.append(id)

    row = row[2][1:-1] # takes only keypts and removes brackets from string
    row_array = np.fromstring(row, dtype=int, sep=',')
   
    keypoints_array.append(row_array)


   

for keypoints in keypoints_array:
    
    #transformation:

    x = keypoints[i_origin]
    y = keypoints[i_origin + 1]
    d = np.array([0 - x, 0 - y])

    x_=keypoints[i_scale*2]
    y_=keypoints[i_scale*2+1]
    scale = np.array([[1/abs(x-x_), 0], [0, 1/abs(y-y_)]])


    keypoints_transformed = []
    for i in range(0, len(keypoints), 2):
        
        p = np.array([keypoints[i], keypoints[i+1]])
        p_transformed = p + d
        p_transformed_scaled = p_transformed*scale

        keypoints_transformed.append(p_transformed)
        

    
    keypoints_array_transformed.append(keypoints_transformed)

#write to file:
header = ['ID', 'Label', 'Key points']
counter = 0
with open('data_base_transformed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for kp in keypoints_array_transformed:
        row = [id_array[counter], label_array[counter], np.ravel(kp)]
        writer.writerow(row)
        counter+=1