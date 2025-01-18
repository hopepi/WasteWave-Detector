import os

"""
Büyük veri setini çevirirken kullandığım yol
Box = [14, 15, 45, 48, 31, 27]
Can =  [3, 10, 47, 76]
Plastic = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 41, 58, 59, 60, 57, 64, 65, 66, 67, 69, 32, 31, 71]
Metal = [17, 53, 47, 3]
Glass = [12, 13, 51, 52]
Waste = [35, 36, 38, 18, 54, 55, 46, 79]
                                    if label in Box:
                                        parts[0] = '0'
                                    elif label in Can:
                                        parts[0] = '1'
                                    elif label in Plastic:
                                        parts[0] = '3'
                                    elif label in Metal:
                                        parts[0] = '4'
                                    elif label in Glass:
                                        parts[0] = '5'
                                    elif label in Waste:
                                        parts[0] = '2'
                                    else:
                                        continue
                                    
                                    
                                    if label in plastic_Bottle:
                                        parts[0] = '0'
                                    elif label in plastic_Bag:
                                        parts[0] = '1'
                                    elif label in can:
                                        parts[0] = '2'
                                    elif label in net:
                                        parts[0] = '4'
                                    elif label in glass:
                                        parts[0] = '5'
                                    elif label in mask:
                                        parts[0] = '6'
                                    elif label in glove:
                                        parts[0] = '7'
                                    elif label in other:
                                        parts[0] = '10'
                                    else:
                                        continue

"""

plastic_Bottle = [1,10,11,13,15,43,45]
plastic_Bag = [12,17,32,33,44]
can = [0,3,8,40,48,49]
net = [9,41]
glass = [4,5,36,37]
mask = [7,35,39]
glove = [38]
other = [23,27,42,50]

def process_and_create_folders_with_content_edit(root_folder, output_base_folder):

    for subdir, dirs, _ in os.walk(root_folder):
        for dir_name in dirs:
            current_dir = os.path.join(subdir, dir_name)
            if dir_name in ["train", "test", "valid"]:
                labels_dir = os.path.join(current_dir, "labels")
                sub_dirs = [current_dir, labels_dir] if os.path.exists(labels_dir) else [current_dir]

                for folder in sub_dirs:
                    print(f"Processing: {folder}")

                    output_folder = os.path.join(output_base_folder, os.path.relpath(folder, root_folder))
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"Created/Verified output folder: {output_folder}")

                    for file in os.listdir(folder):
                        if file.endswith(".txt"):
                            input_file_path = os.path.join(folder, file)
                            output_file_path = os.path.join(output_folder, file)

                            # Dosyanın var olup olmadığını kontrol et
                            if not os.path.exists(input_file_path):
                                print(f"Input file does not exist: {input_file_path}")
                                continue

                            try:
                                # Dosyayı oku
                                with open(input_file_path, 'r') as f:
                                    lines = f.readlines()

                                new_lines = []
                                for line in lines:
                                    parts = line.strip().split()
                                    try:
                                        label = int(parts[0])
                                    except ValueError:
                                        print(f"Invalid label format in line: {line}")
                                        continue
                                    if label == 0:
                                        parts[0] = '3'
                                    elif label == 1:
                                        parts[0] = '4'
                                    elif label == 2:
                                        parts[0] = '5'
                                    elif label == 3:
                                        parts[0] = '7'
                                    elif label == 4:
                                        parts[0] = '9'
                                    elif label == 5:
                                        parts[0] = '6'
                                    elif label == 6:
                                        parts[0] = '2'
                                    elif label == 8:
                                        parts[0] = '0'
                                    elif label == 9:
                                        parts[0] = '1'
                                    else:
                                        continue


                                    new_lines.append(' '.join(parts))

                                # Dosyayı yaz
                                with open(output_file_path, 'w') as f:
                                    f.write('\n'.join(new_lines) + '\n')

                                # Dosyanın başarılı bir şekilde yazıldığını kontrol et
                                if os.path.exists(output_file_path):
                                    print(f"Processed and saved file: {input_file_path} -> {output_file_path}")
                                else:
                                    print(f"Failed to create file: {output_file_path}")

                            except Exception as e:
                                print(f"Error processing file: {file}, Error: {str(e)}")

                    print(f"Completed: {folder}\n{'=' * 40}")

# Kullanım
root_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Veri setleri\video fotograf ayiklama.v1i.yolov11"  # Giriş klasörü
output_base_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Veri setleri\yeni_set10"  # Çıkış klasörü

process_and_create_folders_with_content_edit(root_folder, output_base_folder)
print("All folders processed!")
