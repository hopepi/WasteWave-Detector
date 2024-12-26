import os
import uuid
import shutil


def rename_paired_files(root_folder, output_base_folder):
    output_images_dir = os.path.join(output_base_folder, "images")
    output_labels_dir = os.path.join(output_base_folder, "labels")
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    images_dir = os.path.join(root_folder, "images")
    labels_dir = os.path.join(root_folder, "labels")


    paired_files = {}


    image_extensions = {'.png', '.jpg', '.jpeg'}
    for filename in os.listdir(images_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() in image_extensions:
            paired_files[name] = {
                'image': (filename, ext)
            }


    for filename in os.listdir(labels_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() == '.txt' and name in paired_files:
            paired_files[name]['label'] = (filename, ext)


    for original_name, files in paired_files.items():
        if 'image' in files and 'label' in files:

            new_name = str(uuid.uuid4())


            image_filename, image_ext = files['image']
            label_filename, label_ext = files['label']


            new_image_path = os.path.join(output_images_dir, f"{new_name}{image_ext}")
            new_label_path = os.path.join(output_labels_dir, f"{new_name}{label_ext}")


            try:
                shutil.copy2(
                    os.path.join(images_dir, image_filename),
                    new_image_path
                )
                shutil.copy2(
                    os.path.join(labels_dir, label_filename),
                    new_label_path
                )
                print(f"Successfully processed pair: {original_name} -> {new_name}")
            except Exception as e:
                print(f"Error processing {original_name}: {str(e)}")

    return True


root_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni klasör\oceana waste.v2i.yolov11\valid"
output_base_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni klasör\ismiDegisen\valid"
rename_paired_files(root_folder, output_base_folder)
