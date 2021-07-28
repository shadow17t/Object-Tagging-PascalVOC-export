import os
import glob
from numpy import append, floor
import pandas as pd
import xml.etree.ElementTree as ET

# format should be:
# 1st col= TRAIN/VALIDATION/TEST/UNASSIGNED
# 2nd col= URI
# 3rd col= label
# 4th col= bounding box(2 titik: xmin, ymin,, , xmax, ymax,, / 4titik: xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)

# root = r"/content/Object-Tagging-PascalVOC-export" #root directory path
# root_path = root +'/Annotations/' #input folder
img_path=os.path.join(os.getcwd(), 'Object-Tagging-PascalVOC-export/Annotations/')

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

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

            tipe='TRAIN'
            image_path=root.find('filename').text
            label=member[0].text
            bbox=str(xminrel)+','+str(yminrel)+',,,'+str(xmaxrel)+','+str(ymaxrel)+',,'
            value = (tipe,
                    img_path+(image_path),
                    label,
                    bbox
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