import os
import glob
from numpy import append
import pandas as pd
import xml.etree.ElementTree as ET

# format should be:
# 1st col= TRAIN/VALIDATION/TEST/UNASSIGNED
# 2nd col= URI
# 3rd col= label
# 4th col= bounding box(2 titik: xmin, ymin,, , xmax, ymax,, / 4titik: xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)

root = r"/content/Object-Tagging-PascalVOC-export" #root directory path
root_path = root +'/Annotations/' #input folder

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
            
            xmin=int(member[4][0].text)
            ymin=int(member[4][1].text)
            xmax=int(member[4][2].text)
            ymax=int(member[4][3].text)
            
            xminrel=float(xmin/width)
            yminrel=float(ymin/height)
            xmaxrel=float(xmax/width)
            ymaxrel=float(ymax/height)

            type='TRAIN'
            img_path=root_path.append(root.find('filename').text)
            label=member[0].text
            # value = ('TRAIN',
            #         root_path.append(root.find('filename').text),
            #         member[0].text,
            #         xminrel,
            #         yminrel,
            #         ',,',
            #         xmaxrel,
            #         ymaxrel,
            #         ",,"
            #         )
            xml_list.append(type,img_path,label,xminrel,yminrel,',,',xmaxrel,ymaxrel,',,')
    xml_df = pd.DataFrame(xml_list)
    return xml_df


def main():
    for folder in ['train']:#,'test']:
        # image_path = os.path.join(os.getcwd(), ('images/' + folder))
        image_path = os.path.join(os.getcwd(), 'Annotations')
        xml_df = xml_to_csv_train(image_path)
        xml_df.to_csv((folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')


main()