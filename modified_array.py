import csv

input_file = 'data_base_transformed_2.csv'
output_file = 'data_base_new.csv'

keypoints_array_transformed = []

with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        #oduzimamo jedan kako bi imali Label-e od 0-2, a ne od 1-3 zbog RandomForestClassifier-a
        label = int(row['Label']) - 1 
        keypoints_str = row['Key points']
        
        keypoints_str = keypoints_str.replace('[', '').replace(']', '').replace('   ', ' ')
        
        keypoints_values = keypoints_str.split()
        
        keypoints_transformed = []
        for i in range(0, len(keypoints_values), 2):
            x = float(keypoints_values[i])
            y = float(keypoints_values[i + 1])
            keypoints_transformed.append([x, y])
        
        keypoints_array_transformed.append({'Label': label, 'Key points': keypoints_transformed})

with open(output_file, 'w', newline='') as file:
    fieldnames = ['Label', 'Key points']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(keypoints_array_transformed)
