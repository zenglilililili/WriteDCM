'''将dcm读出并保存为需要的格式，即在每个病人文件夹内增加如下文件
--doctor
    --病人
        --ROI
            --ROI编号.png
'''

import os
import shutil
import pydicom
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import misc


#输入文件夹路径和关键词，找到该路径下含有该关键词的文件
def find_file(path,word):
    # print('***********')
    # print(path)
    # print(word)
    rtstruct_path = ''
    Slice_list = os.listdir(path)
    for slice_list in Slice_list:
        if word in slice_list:
            rtstruct_path = path + '/' + slice_list
            # print('RTSTRUCT path = '+rtstruct_path)
    if rtstruct_path == '':
        return -1
    return rtstruct_path#只返回了最后的RTstruct文件名

#转换坐标，得到二维坐标
def convert_global_aix_to_net_pos(pointData,CT_pos):

    label_data =  pointData.ContourData # 返回坐标{uid:data}
    num = pointData.NumberOfContourPoints#点数

    dcm_origin = CT_pos[0]#['-249.51171875', '-427.51171875', '-582.2']  # 网格原点在世界坐标系的位置
    dcm_spacing = CT_pos[1]#['0.9765625', '0.9765625']  # 采样间隔
    point = []  # 坐标[(x1,y1,z1),(...),...]
    for i in range(0,num*3,3):
        x = label_data[i]  # 轮廓世界坐标系
        y = label_data[i + 1]
        X = int((float(x) - float(dcm_origin[0])) / float(dcm_spacing[0]) )  # 轮廓X坐标
        Y = int((float(y) - float(dcm_origin[1])) / float(dcm_spacing[1]) ) # 轮廓Y坐标

        point.append((X, Y))
    point = np.array(point)
    return point


#将插入后完整的连通区域points所围区域填充
def fillColor(point):
    # print(point)
    img = np.zeros((512, 512),dtype=np.int)
    img2 = cv2.fillPoly(img, [point], 1)
    # plt.imshow(img2.T, cmap='gray')
    # plt.show()
    return img2



#输入RTSTRUCT路径、保存的路径、部位，无返回，直接保存
def saveImg(datapath,RT_path,pos_path,pos):
    ROINum = -1
    RTdata = pydicom.read_file(RT_path, force=True)

    CT_path = datapath + "/CT_" + RTdata.ROIContourSequence[0].ContourSequence[0].ContourImageSequence[0].ReferencedSOPInstanceUID
    CT_data = pydicom.read_file(CT_path,force=True)
    CT_pos = [CT_data.ImagePositionPatient,CT_data.PixelSpacing]


    for ROISeq in RTdata.StructureSetROISequence:
        if pos == ROISeq.ROIName:
            # print(ROISeq.ROINumber)
            ROINum = ROISeq.ROINumber
            break
    if ROINum == -1:
        shutil.rmtree(pos_path)
        print('error！无'+pos +'部位数据！')
        return -1
    # print(ROINum)

    for ROISeq in RTdata.ROIContourSequence:
        if ROINum == ROISeq.ReferencedROINumber:
            slice_before_name = -1#记录上一个连通区域的名字
            slice_exist_flag = -1#-1表示还没有这个名字的标签， 1表示为第一个这个切片，2表示为第二个这个切片
            for contour in ROISeq.ContourSequence:
                point_data = convert_global_aix_to_net_pos(contour,CT_pos)
                img_data = fillColor(point_data)
                slice_Lable_name = contour.ContourImageSequence[0].ReferencedSOPInstanceUID
                # print(pos_path+'/'+ slice_Lable_name + '.png')
                if slice_before_name == contour.ContourImageSequence[0].ReferencedSOPInstanceUID:
                    slice_exist_flag += 1
                else:
                    slice_before_name = contour.ContourImageSequence[0].ReferencedSOPInstanceUID
                    slice_exist_flag = 1

                misc.imsave(pos_path+'/'+ slice_Lable_name +"_"+str(slice_exist_flag)+ '.png', img_data)

                # print('save path : '+ pos_path+'/'+ slice_Lable_name + '.png')

            break




# datapath = "Data\dcmHua\doctor1/0002348871/"
# rtname = "RTSTRUCT_2.16.840.1.113669.2.931128.108227473.20190801151803.225328"
# pos_path = 'Data\dcmHua\doctor1/0002348871/CTV'
# pos = 'Bladder'
# saveImg(datapath,rtname,pos_path,pos)


#读取标签图像
def getDCMData(rootpath,position):
    Doc_list = os.listdir(rootpath)
    doctor_i = 0
    for doc_dir in Doc_list:


        Pat_list = os.listdir(rootpath+'/'+doc_dir)
        patient_i = 0
        for pat_list in Pat_list:
            # print(pat_list)

            RT_path = find_file(rootpath+'/'+doc_dir+'/'+pat_list, 'RTSTRUCT_')
            if RT_path == -1:#如果没有标注，则跳过
                print(rootpath+'/'+doc_dir+'/'+pat_list+"  Don't have RTSTRUCT!!!!")
                continue
            pat_path = rootpath+'/'+doc_dir+'/'+pat_list
            # print("patient_path = " + pat_path)
            for pos in position:#对每个部位进行遍历，找出每个部位的图像并保存
                print("doctor " + str(doctor_i) + ' : ' + doc_dir + '  //   patient ' + str(
                    patient_i) + ' : ' + pat_list + "   //  position:  " + pos)
                path_true = os.path.exists(pat_path + '/' + pos)

                if path_true == True:
                    shutil.rmtree(pat_path + '/' + pos)
                    print('path is already exist')
                os.makedirs(pat_path + '/' + pos)

                pos_path = pat_path + '/' + pos
                try:
                    saveImg(pat_path,RT_path,pos_path,pos)
                except BaseException:
                    shutil.rmtree(rootpath+'/'+doc_dir+'/'+pat_list + '/' + pos)
                    print(rootpath+'/'+doc_dir+'/'+pat_list+'没有ContourImageSequence')


                print('\n')
            patient_i += 1
        doctor_i += 1

rootpath = 'Data'
position = ['CTV','Rectum','Bladder'] #标签部位
getDCMData(rootpath,position)