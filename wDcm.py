from tools import getCTName,getDirName,getLablePos,getSliceList
import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime
from pydicom.sequence import Sequence

def writeDCM(root_Path,doc,pat,data):
    # HUaPath = 'Data/dcmHua/liping(0703)/0014712255/RTSTRUCT_2.16.840.1.113669.2.931128.121126138.20190626165800.28009'
    # RTHuaData = pydicom.read_file(HUaPath, force=True)

    # Create some temporary filenames
    # 获取对应的CT信息
    CTpath = getCTName(root_Path + '/' + doc + '/' + pat, 'CT_')
    CTrefds = pydicom.read_file(CTpath, force=True)

    # 新建RTSTRUCT文件
    # filename = root_Path + '/' + doc + '/' + pat + '/'+'RTSTRUCT_2.16.840.1.113669.2.931128.121126138.20190703172017.764011'
    filename = root_Path + '/' + doc + '/' + pat + '/RTSTRUCT_' + pat + '.dcm'
    RTName = pat + '.dcm'
    # RTName = filename
    dirName = getDirName(root_Path + '/' + doc + '/' + pat)#切片的目录文件.dir的名字
    dirPath = root_Path + '/' + doc + '/' + pat + '/'+dirName
    # print(dirName)
    # dirPath = 'Data\dcmHua\doctor1/0002348871/CT_1.3.12.2.1107.5.1.4.66045.30000014051200211018700037438.dir'


    ds = FileDataset(filename, {},preamble=b"\0" * 128)

    # Specific Character Set
    # ds.SpecificCharacterSet = RTHuaData.SpecificCharacterSet#'ISO_IR 100'#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        ds.SpecificCharacterSet = CTrefds.SpecificCharacterSet
    except BaseException:
        print('对应CT没有 Specific Character Set属性')

    #SOPInstanceUID
    ds.SOPInstanceUID = RTName


    # InstanceCreationDate
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    ds.InstanceCreationDate = str(year) + str(month) + str(day)

    # Instance Creation Time ???????????????????????????????????????????????
    time = datetime.datetime.now()
    ds.InstanceCreationTime =  time

    # SOP Class UID
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3' #RTHuaData.SOPClassUID# "RT Structure Set Storage"

    # Study Date
    ds.StudyDate = CTrefds.StudyDate

    # Study Time
    ds.StudyTime = CTrefds.StudyTime

    # Accession Number
    ds.AccessionNumber = CTrefds.AccessionNumber
    # Modality
    ds.Modality = "RTSTRUCT"

    # Manufacturer????????????????????!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ds.Manufacturer ="UESTC"#'ADAC'

    # Referring Physician's Name
    ds.ReferringPhysicianName =  "Huaxi"

    # Station Name ?????????????????
    ds.StationName =  'pinnsx86c-6' #"UESTC"!!!!!!!!!!!!!!!!!!!!!!!

    # Physician(s) of Record
    ds.PhysiciansOfRecord =  "UESTC"

    # Manufacturer's Model Name
    ds.ManufacturerModelName =  "UESTC"

    # Referenced Study Sequence 写sequence
    beam = Dataset()
    ds.ReferencedStudySequence = Sequence([beam])
    ds.ReferencedStudySequence[0].ReferencedSOPClassUID = "Study Component Management SOP Class"
    ds.ReferencedStudySequence[0].ReferencedSOPInstanceUID = CTrefds.StudyInstanceUID
    # ds.ReferencedStudySequence = RTHuaData.ReferencedStudySequence


    # Patient's Name??????????!!!!!!!!!!!!!!
    ds.PatientName = CTrefds.PatientName#RTHuaData.PatientName#'du qi wen restored^13684p1204224^pelvis^'#RTHuaData.PatientName#'du qi wen restored^13684p1204224^^'#

    # Patient ID
    ds.PatientID = CTrefds.PatientID

    # Patient's Birth Date
    ds.PatientBirthDate = CTrefds.PatientBirthDate

    # Patient's Sex
    ds.PatientSex = CTrefds.PatientSex

    # Software Version
    ds.SoftwareVersions = ['9.2', '9.2']

    # Study Instance UID
    ds.StudyInstanceUID = CTrefds.StudyInstanceUID

    # Series Instance UID ?????????????
    ds.SeriesInstanceUID = RTName#RTHuaData.SeriesInstanceUID#'2.16.840.1.113669.2.931128.121126138.20190703172017.513499'#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Study ID
    ds.StudyID = CTrefds.StudyID

    # Series Number
    ds.SeriesNumber = "1"

    # Structure Set Label
    ds.StructureSetLabel = "Plan_1"

    # Structure Set Name
    ds.StructureSetName ="POIandROIandBOLUS"

    # Structure Set Date
    ds.StructureSetDate = ds.InstanceCreationDate

    # Structure Set Time
    ds.StructureSetTime = datetime.datetime.now()

    # Referenced Frame of Reference Sequence
    beam = Dataset()
    ds.ReferencedFrameOfReferenceSequence = Sequence([beam])
    ds.ReferencedFrameOfReferenceSequence[0].FrameOfReferenceUID = CTrefds.FrameOfReferenceUID

    beam2 = Dataset()
    ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence = Sequence([beam2])
    ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[
        0].ReferencedSOPClassUID = "Study Component Management SOP Class"
    ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[
        0].ReferencedSOPInstanceUID = CTrefds.StudyInstanceUID

    beam3 = Dataset()
    ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence = Sequence(
        [beam3])
    ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[
        0].SeriesInstanceUID = dirName

    # 写dir文件
    # 这个sequence包含的是dir文件中的每一个文件名遍历，思路是先读取dir文件，对每一行进行遍历，然后将每一行放入文件的lengthi处
    print(dirPath)
    print('^^^^^^^^^^^^^')
    dirList = open(dirPath, 'r')
    count_i = 0
    for dirname in dirList:
        # print(count_i)
        block_i = Dataset()
        if count_i == 0:
            beam4 = Dataset()
            ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[
                0].ContourImageSequence = Sequence([beam4])
        else:
            ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[
                0].ContourImageSequence.append(block_i)

        ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[
            0].ContourImageSequence[count_i].ReferencedSOPClassUID = "CT Image Storage"
        ds.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[
            0].ContourImageSequence[count_i].ReferencedSOPInstanceUID = dirname
        count_i += 1

    # 写标注部位
    # 思路：输入标注部位列表，StructureSetROISequenceList,然后对每一个部位进行填充
    # StructureSetROISequenceList = ['locref', 'Spinal Cord  N', 'Liver  N', 'Kidney L  N', 'Kidney R  N', 'Bladder','Femoral Head R', 'Femoral Head L', 'Rectum', 'CTV', 'PTV']

    StructureSetROISequenceList = getLablePos(data)
    print(StructureSetROISequenceList)
    print('@@@@@@@@@@@@')
    count_j = 0
    for ROISequence in StructureSetROISequenceList:
        block_j = Dataset()
        if count_j == 0:
            beam5 = Dataset()
            ds.StructureSetROISequence = Sequence([beam5])
        else:
            ds.StructureSetROISequence.append(block_j)
        ds.StructureSetROISequence[count_j].ROINumber = count_j
        ds.StructureSetROISequence[count_j].ReferencedFrameOfReferenceUID = CTrefds.FrameOfReferenceUID
        ds.StructureSetROISequence[count_j].ROIName = ROISequence
        count_j += 1

    # 对每一个标注部位开始写contour
    # 思路：先建立部位的列表，每个部位包含有该部位的切片列表，然后每个切片包含contour
    count_ROI = 0
    colorList = [['127', '255', '212'], ['0', '255', '0'], ['0', '0', '255'], ['0', '255', '255'], ['255', '150', '0'],
                 ['128', '0', '255'], ['34', '139', '34'], ['255', '0', '0'], ['127', '255', '212'],
                 ['128', '0', '255'], ['165', '161', '55']]
    # print('*******************%%%%%%%%%%%%%%%%%%%')
    for ROISequence in StructureSetROISequenceList:  # 对部位进行循环
        block_ROI = Dataset()
        if count_ROI == 0:
            beam_ROI = Dataset()
            ds.ROIContourSequence = Sequence([beam_ROI])
        else:
            ds.ROIContourSequence.append((block_ROI))

        ds.ROIContourSequence[count_ROI].ROIDisplayColor = colorList[count_ROI]

        count_Slice = 0
        SliceList = getSliceList(data, doc, pat, ROISequence)
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        # print(len(SliceList[0][4]))
        # SliceList = np.array(SliceList)
        # print(SliceList)
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

        # SliceList = ['1.3.12.2.1107.5.1.4.66045.30000014051200211018700037557','1.3.12.2.1107.5.1.4.66045.30000014051200211018700037563']

        # # 对应的contour
        for slice in SliceList:  # 对切片进行循环，这里需要写一个筛选哪些切片有标注，形成一个list
            # print(slice)
            # print('(((((((((((((()))))))))))))))')
            block_Slice = Dataset()
            if count_Slice == 0:
                beam_Slice = Dataset()
                ds.ROIContourSequence[count_ROI].ContourSequence = Sequence([beam_Slice])
            else:
                ds.ROIContourSequence[count_ROI].ContourSequence.append((block_Slice))
            #
            #     # 每张切片单独成一个slice的item，不需要对slice内部进行循环
            #     ''' Png文件存储要求：
            #     1.png文件名是"部位_切片名"
            #     2.写一个文件，读入png及其名称，转换其像素点为dicom坐标contour，判断连通区域，每个联通区域存储成一项，
            #
            #     --RTSTRUCT
            #         --ROI
            #             --slice
            #

            #     '''
            beam_contour = Dataset()
            ds.ROIContourSequence[count_ROI].ContourSequence[count_Slice].ContourImageSequence = Sequence(
                [beam_contour])
            ds.ROIContourSequence[count_ROI].ContourSequence[count_Slice].ContourImageSequence[
                0].ReferencedSOPClassUID = "CT Image Storage"
            ds.ROIContourSequence[count_ROI].ContourSequence[count_Slice].ContourImageSequence[
                0].ReferencedSOPInstanceUID = slice[3]

            ds.ROIContourSequence[count_ROI].ContourSequence[count_Slice].ContourGeometricType = 'CLOSED_PLANAR'
            # contourData = slice[4].split(',')

            ds.ROIContourSequence[count_ROI].ContourSequence[count_Slice].NumberOfContourPoints = len(slice[4]) / 3

            ds.ROIContourSequence[count_ROI].ContourSequence[
                count_Slice].ContourData = slice[4]#mv(DSfloat, contourData)  # ['-39.4297', '-227.672','-1689.79', '-37.346','-228.714', '-1689.79']
            count_Slice += 1

        ds.ROIContourSequence[count_ROI].ReferencedROINumber = count_ROI
        count_ROI += 1





    # ds.ReferencedFrameOfReferenceSequence = RTHuaData.ReferencedFrameOfReferenceSequence
    # ds.StructureSetROISequence = RTHuaData.StructureSetROISequence
    # ds.ROIContourSequence = RTHuaData.ROIContourSequence

    print('&&&&&&&&&&&&&')
    print("Writing test file", filename)
    ds.save_as(filename)
    print("File saved.")

    print('**************')
    # path = pat+'.dcm'
    p = pydicom.read_file(filename)
    print(p)
