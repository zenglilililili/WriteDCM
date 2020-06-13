from pydicom.multival import MultiValue as mv
from pydicom.valuerep import DSfloat
from tools import getDir,convert_to_dcm
import os
#根目录下的所有数据
def getData(root_Path,doc,pat):
    labels = ['doctor','patient','position','imgName','contour']
    dataList = []
    pos_list = getDir(root_Path + '/' + doc + '/' + pat)
    for pos in pos_list:#对部位循环
        img_list = os.listdir(root_Path + '/' + doc + '/' + pat + '/'+pos)
        for img in img_list:#对图片循环
            img_name = img.split('_')[0]
            img_path = root_Path + '/' + doc + '/' + pat + '/'+pos+'/'+img
            patPath = root_Path + '/' + doc + '/' + pat
            slicepoint = convert_to_dcm(img_path,img_name,patPath)

            contourData = slicepoint.split(',')
            point = mv(DSfloat, contourData)

            sliceList = []
            sliceList.append(doc)
            sliceList.append(pat)
            sliceList.append(pos)
            sliceList.append(img_name)#包含了同一切片的所有连通区域
            sliceList.append(point)
            dataList.append(sliceList)
    return dataList