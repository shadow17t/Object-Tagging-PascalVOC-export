# coding=utf-8
import os
import os.path
import xml.dom.minidom
 
# Convert string to int
def to_int(str):
    try:
        int(str)
        return int(str)
    except ValueError: #Report type error, indicating that it is not an integer
        try:
            float(str) #Use this to verify whether it is a floating point string
            return int(float(str))
        except ValueError: #If an error is reported, it means that it is not a floating point or an int string. Is a real string
            return False
 
root = r"/content/Object-Tagging-PascalVOC-export" #root directory path
path = root +'/Annotations' #input folder
save_path = root +'/Annotations2' #output folder
if not os.path.isdir(save_path):
    os.makedirs(save_path)
files = os.listdir(path) # Get the names of all r files in the folder
s = []
for xmlFile in files:
         # Traverse folders
    portion = os.path.splitext(xmlFile)
    if not os.path.isdir(xmlFile):
                 # Determine whether it is a folder, not a folder to open
        print (xmlFile)
 
                 # xml file read operation
                 # Send the obtained xml file name to dom for analysis
        dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))
                 # The core part os.path.join(path,xmlFile), path splicing, the input is the specific path
        root = dom.documentElement
 
                 # Modify xmin
        xmin = root.getElementsByTagName('xmin')
        for i in range(len(xmin)):
            if to_int(xmin[i].firstChild.data) < 0:
                xmin[i].firstChild.data = 0
                print(">>>>>>>>>>>>>>>>>>>xmin is modified to: "+str(xmin[i].firstChild.data))
        
                 # Modify ymin
        ymin = root.getElementsByTagName('ymin')
        for i in range(len(ymin)):
            if to_int(ymin[i].firstChild.data) < 0:
                ymin[i].firstChild.data = 0
                print(">>>>>>>>>>>>>>>>>>>ymin is modified to: "+str(ymin[i].firstChild.data))
        
                 # Get the width and height of the image
        width = 0
        height = 0
        img_w = root.getElementsByTagName('width')
        for i in range(len(img_w)):
            width = to_int(img_w[i].firstChild.data)
        
        img_h = root.getElementsByTagName('height')
        for i in range(len(img_h)):
            height = to_int(img_h[i].firstChild.data)
        
                 # Modify xmax
        xmax = root.getElementsByTagName('xmax')
        for i in range(len(xmax)):
            if to_int(xmax[i].firstChild.data) > width:
                xmax[i].firstChild.data = width
                print(">>>>>>>>>>>>>>>>>>>xmax is modified to "+str(xmax[i].firstChild.data))
        
                 # Modify ymax
        ymax = root.getElementsByTagName('ymax')
        for i in range(len(ymax)):
            if to_int(ymax[i].firstChild.data) > height:
                ymax[i].firstChild.data = height
                print(">>>>>>>>>>>>>>>>>>>ymax is modified to: "+str(ymax[i].firstChild.data))
 
                 # # Modify the size of the image
        # if width > height:
        #     for i in range(len(img_h)):
        #         img_h[i].firstChild.data = width
        # elif width < height:
        #     for i in range(len(img_w)):
        #         img_w[i].firstChild.data = height
        # else:
        #     print("need not alter!")
 
                 # Save the changes to the xml file
        with open(os.path.join(save_path, xmlFile), 'w', encoding='UTF-8') as fh:
            dom.writexml(fh)
            print('process...')
 
        # name = root.getElementsByTagName('name')
        # # pose=root.getElementsByTagName('pose')
                 # # Rename class name
        # for i in range(len(name)):
        #     # print (name[i].firstChild.data)
        #     # print(xmlFile)
        #     # if portion[1] == ".xml":
        #     #     newname = portion[0] + ".jpg"
        #     #     print(newname)
        #     newname = "zero"
        #     if name[i].firstChild.data == "chebiao":
        #         name[i].firstChild.data = newname
        #         print(name[i].firstChild.data)