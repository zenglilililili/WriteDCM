import os
import pydicom
import cv2

#获取文件夹下的所有文件夹目录
def getDir(pat_path):
    pos_list = []
    slice_list = os.listdir(pat_path)
    for slice in slice_list:
        slice_path = pat_path + '/' + slice
        if os.path.isdir(slice_path):  # 是文件夹
            # print("it's a directory")
            pos_list.append(slice)
    return pos_list

#转换坐标，得到dcm格式坐标
#输入图片路径，图片名称，病人的路径，纵坐标
def convert_to_dcm(img_path,img_name,patPath):
    # print(patPath+'/CT_'+img_name)
    # print('************')
    CTPath = patPath+'/CT_'+img_name
    CTdata = pydicom.read_file(CTPath,force=True)
    z = CTdata.SliceLocation
    #将图像提取轮廓
    print(img_path)
    imgRes = cv2.imread(img_path, 0)
    contours, mask = cv2.findContours(imgRes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0][:, 0]
    num = contour.shape[0]#点数

    #读取CT的space等数据
    CTData = pydicom.read_file(patPath+'/CT_'+img_name,force="True")
    dcm_origin = CTData.ImagePositionPatient#ImagePositionPatient#['-249.51171875', '-427.51171875', '-582.2']  # 网格原点在世界坐标系的位置
    dcm_spacing =  CTData.PixelSpacing#PixelSpacing#['0.9765625', '0.9765625']  # 采样间隔

    # pointData = []  # 坐标[(x1,y1,z1),(...),...]
    pointStr = ''

    for i in range(0,num):
        x = contour[i][0]  # 轮廓世界坐标系
        y = contour[i][1]

        X = float(x)*float(dcm_spacing[0]) +float(dcm_origin[0])   # 轮廓X坐标
        Y = float(y)*float(dcm_spacing[1]) +float(dcm_origin[1])   # 轮廓Y坐标

        #直接存成字符串形式，以，分割
        if pointStr == '':
            pointStr = str(X) + ',' + str(Y) + ',' + str(z)
        else:
            pointStr = pointStr + ','+ str(X) + ',' + str(Y) + ',' + str(z)

    return pointStr

def getCTName(path,keyword):
    list = os.listdir(path)
    # print(list)
    for name in list:
        if keyword in name and '.dir' not in name and 'RTSTRUCT' not in name:
            return path+'/'+name




#得到dir目录文件的名字
def getDirName(path):
    list = os.listdir(path)
    for name in list:
        if "dir" in name:
            return name


#获取部位列表
def getLablePos(data):
    posList = []
    for slice in data:
        # print(slice)
        if slice[2] not in posList:
            posList.append(slice[2])
    return posList



def getSliceList(data,doc,pat,pos):
    #输入部位名字，和标注后的切片位置
    # 返回有标注切片的列表
    sliceList = []
    for slice in data:
        if slice[0]==doc and slice[1]==pat and slice[2]==pos:
            sliceList.append(slice)
    return sliceList
