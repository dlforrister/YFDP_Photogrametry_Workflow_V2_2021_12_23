# Goal of this code is to organize aerial photos aquired overd the YFDP
import os
import pandas as pd
import PIL
from PIL import Image
from PIL import ImageStat
import glob
from datetime import datetime
import shutil

baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/"

def mapir_rename(baseDir):
    failed_photos = pd.DataFrame(columns={'filename': [], 'flight': [], 'n': [],'message': []})
    if not os.path.exists(baseDir + '/Proccessed_Images/'):
        os.makedirs(baseDir + '/Proccessed_Images/')
    if not os.path.exists(baseDir + "/Proccessed_Images/MAPIR/"):
        os.makedirs(baseDir + "/Proccessed_Images/MAPIR/")
        
    
    for flight in os.listdir(baseDir + "/MAPIR/")[:-1]:
        structure_check = True
        i = int(flight[7])
        if i not in [1,2,3,4,5]:
            print("flight number in correct! flight = {} ".format(i))
            structure_check = False
            continue
        print("starting flight {} ".format(i))
        x=1
        file_list = glob.glob(baseDir + "//MAPIR" + "/" + flight+ "/Processed_1/*")
        file_list.sort()
        for file_n in range(len(file_list)-1):
            pic_date = datetime.strptime(str(os.path.basename(file_list[file_n])[:-4]), '%Y_%m%d_%H%M%S_%f')
            shutil.copy(file_list[file_n], baseDir + "/Proccessed_Images/MAPIR/" + pic_date.strftime("%Y") + "_" + pic_date.strftime('%b') + "_" + pic_date.strftime('%d') + "_MAPIR_Flight_" + str(i) + "_" + str(x) + ".JPG")
            print(x)
            x+=1                    



mapir_rename(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2") 
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_9") # Not working

#Done calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/3_2018_Nov/Nov_06_2018")
#Donecalculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/3_2018_Nov/Nov_12_2018")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/4_2018_Dec/Dic_03_2018")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/4_2018_Dec/Dic_10_2018")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/5_2019_Jan/Jan_08_2019")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/5_2019_Jan/Jan_15_2019")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/6_2019_Feb/2019_Feb_6")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/6_2019_Feb/2019_Feb_11")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/7_2019_Mar/Feb_28_2019")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/7_2019_Mar/Mar_06_2019_V2")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/8_2019_Apr/2019_April_3_V2")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/8_2019_Apr/2019_April_8_V2")


#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/9_2019_May/2019_May_5")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/9_2019_May/2019_May_9")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/10_2019_JUNE/2019_May_29")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/11_2019_July/2019_July_2")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/11_2019_July/2019_July_6")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/12_2019_Aug/2019_July_23")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/12_2019_Aug/2019_August_1")

#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/13_2019_Sept/2019_Sept_06")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/13_2019_Sept/2019_Sept_11")
#calculate_and_copy(baseDir = "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/13_2019_Sept/2019_Sept_13")ß

