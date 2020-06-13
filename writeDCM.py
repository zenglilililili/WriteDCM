import os
from getData import getData
from wDcm import writeDCM

root_Path = 'Data'
Doc_list = os.listdir(root_Path)
for doc in Doc_list:#对医生循环
    pat_list = os.listdir(root_Path+'/'+doc)
    for pat in pat_list:#对病人循环
        data = getData(root_Path,doc,pat)
        writeDCM(root_Path, doc, pat,data)