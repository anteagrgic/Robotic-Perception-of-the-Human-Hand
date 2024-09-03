import cv2
import os



input_dir = r"../ZAVRSNI_2/otvorena_ruka/otvorena ruka"
output_dir = r"../ZAVRSNI_2/otvorena_ruka_resized"



image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png', '.jpeg', '.JPG'))]



for image_file in image_files:
    # Load the image
    image_path = os.path.join(input_dir, image_file)
    img = cv2.imread(image_path)

    # Resize the image (replace 800, 600 with your desired dimensions)
    resized_img = cv2.resize(img, (504, 672))

    # Save the resized image
    output_path = os.path.join(output_dir, image_file)
    cv2.imwrite(output_path, resized_img)