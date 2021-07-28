import os
import glob
import random
from numpy import append, floor
import pandas as pd
import xml.etree.ElementTree as ET

# format should be:
# 1st col= TRAIN/VALIDATION/TEST/UNASSIGNED
# 2nd col= URI
# 3rd col= label
# 4th col= bounding box(2 titik: xmin, ymin,, , xmax, ymax,, / 4titik: xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)

img_dir=os.path.join(os.getcwd(), 'Object-Tagging-PascalVOC-export/JPEGImages/')

image_paths = os.listdir(img_dir)
random.shuffle(image_paths)

train_size=0.8
validation_size=0.1
test_size=0.1
n_images=len(image_paths)

train_data = image_paths[:int((n_images+1)*train_size)]
val_data = image_paths[int((n_images+1)*train_size):(int((n_images+1)*train_size)+int((n_images+1)*validation_size))]
test_data = image_paths[(int((n_images+1)*train_size)+int((n_images+1)*validation_size)):]
print(len(image_paths))
print(len(train_data),len(val_data),len(val_data))


def xml_to_csv_train(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            width=int(root.find('size')[0].text)
            height=int(root.find('size')[1].text)
            
            xmin=int(float(member[4][0].text))
            ymin=int(float(member[4][1].text))
            xmax=int(float(member[4][2].text))
            ymax=int(float(member[4][3].text))
            
            xminrel=float(xmin/width)
            yminrel=float(ymin/height)
            xmaxrel=float(xmax/width)
            if xmaxrel > 1:
              xmaxrel=floor(xmaxrel)
            ymaxrel=float(ymax/height)
            if ymaxrel > 1:
              ymaxrel=floor(ymaxrel)

            image_filename=root.find('filename').text
            if image_filename in train_data:
                data_type='TRAIN'
            elif image_filename in val_data:
                data_type='VALIDATION'
            elif image_filename in test_data:
                data_type='TEST'
            
            label=member[0].text
            # bbox=str(xminrel)+','+str(yminrel)+',,,'+str(xmaxrel)+','+str(ymaxrel)+',,'
            value = (data_type,
                    img_dir+(image_filename),
                    label,
                    # bbox
                    xminrel,yminrel,'','',xmaxrel,ymaxrel,'',''
                    )
            xml_list.append(value)
    xml_df = pd.DataFrame(xml_list)
    return xml_df


def main():
    # for folder in ['train']:#,'test']:
        # image_path = os.path.join(os.getcwd(), ('images/' + folder))
    image_path = os.path.join(os.getcwd(), 'Object-Tagging-PascalVOC-export/Annotations')
    print(image_path)
    xml_df = xml_to_csv_train(image_path)
    xml_df.to_csv(( 'train_labels.csv'), index=None)
    print('Successfully converted xml to csv.')


main()