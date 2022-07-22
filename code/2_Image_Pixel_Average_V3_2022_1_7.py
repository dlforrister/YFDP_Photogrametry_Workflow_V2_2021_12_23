# Calculate the mean pixel values for each drone image
import PIL.Image
from PIL import ImageStat
from PIL.TiffTags import TAGS
import pandas as pd
from numpy import asarray
import os
import glob
import concurrent.futures
from datetime import datetime
from GPSPhoto import gpsphoto
from pandas.tseries.offsets import Nano
import piexif

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def proc_image(i):
    if any(i.endswith(s) for s in [".JPG", ".tif"]):
        if i.endswith(".tif"):
            img = PIL.Image.open(i, mode = "r")
            meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
            data = asarray(img)
            df = pd.DataFrame({'file_name': os.path.basename(i), 'flight': os.path.basename(i).split("_")[5], 'image': os.path.basename(i).split("_")[6], 'date': meta_dict["DateTime"], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
            img.close()
            return(df)
        else:
            img = PIL.Image.open(i, mode = "r")
            data = asarray(img)
            df = pd.DataFrame({'file_name': os.path.basename(i), 'flight': os.path.basename(i).split("_")[5], 'image': os.path.basename(i).split("_")[6], 'date': img._getexif()[36867], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
            img.close()
            return(df)

def proc_image_post_norm(i):
    try:
        if any(i.endswith(s) for s in [".JPG", ".tif"]):
            img = PIL.Image.open(i, mode = "r")
            data = asarray(img)
            df = pd.DataFrame({'file_name': os.path.basename(i), 'flight': os.path.basename(i).split("_")[5], 'image': os.path.basename(i).split("_")[6], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
            img.close()
            return(df)
    except:
        print("Image has issue")

   


      
# Driver program



def calc_image_average(path = False, post_norm = False):
    if post_norm == True:
        paths = list(listdir_nohidden(path+"output/"))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            df_list = executor.map(proc_image_post_norm, paths)
    else:
        paths = list(listdir_nohidden(path))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            df_list = executor.map(proc_image, paths,post_norm)

    df_list = list(df_list)
    df = pd.concat(list(df_list))
    print("Writing CSV with mean reflectance for {} images".format(len(df.file_name)))        
    df.to_csv(path + "image_mean_reflectance.csv")

def extract_gps_metadat(i):
    if any(i.endswith(s) for s in [".JPG", ".tif"]):
        gpsdata = gpsphoto.getGPSData(i)
        return(pd.DataFrame({"Label":os.path.basename(i), "X":	gpsdata['Longitude'], "Y": gpsdata['Latitude'], "Z": gpsdata['Altitude']}, index=[0]))

def extract_gps_metadat_multi_thred(path):
    paths = list(listdir_nohidden(path))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_list = executor.map(extract_gps_metadat, paths)
    df_list = list(df_list)
    df = pd.concat(list(df_list))
    print("Writing CSV with GPS info for {} images".format(len(df.Label)))        
    df.to_csv(path + "images_metadata_gps.csv",index=False)


#October Phantom reflectance
#October Phantom Images
path='/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/Proccessed_Images_V2/Phantom/'

calc_image_average(path)
calc_image_average(path,post_norm=True)

#October Mapir Images Reflectance
#flight_1_3
path = '/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_1_3/'
calc_image_average(path)
#after normalization
calc_image_average(path,post_norm=True)

extract_gps_metadat_multi_thred(path)

#flight_4_5
path='/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_4_5/'
calc_image_average(path)
calc_image_average(path,post_norm=True)

#October MAPIR reflectance target
calc_image_average('/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/Reflectance/Mapir/Processed_1/')

#October Phantom reflectance target
calc_image_average('/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/2_2018_Oct/2018_Oct_2_V2/Reflectance/Phantom/')


#October stationary reflectance Target

def calc_image_average_reflectance(path = False):
    paths = list(listdir_nohidden(path))

    n=0
    for i in paths:
        n+=1
        #if i.endswith(".JPG"):
        if any(i.endswith(s) for s in [".JPG", ".tif"]):
            try:

                if i.endswith(".tif"):
                    with PIL.Image.open(i, mode = "r") as img:
                        meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
                        stats = PIL.ImageStat.Stat(img)
                    df = df.append({'file_name': os.path.basename(i), 'flight': 1, 'image': n, 'date': meta_dict["DateTime"][0], 'mean_red': stats.mean[0],'sd_red': stats.stddev[0], 'mean_green': stats.mean[1],'sd_green': stats.stddev[1], 'mean_blue': stats.mean[2],'sd_blue': stats.stddev[2]}, ignore_index=True)
            except:
                continue
    print("Writing CSV with mean reflectance for {} images".format(len(df.file_name)))        
    df.to_csv(path + "image_mean_reflectance.csv")



def convert_tif_to_png(path):
    paths = glob.glob(os.path.join(path, 'Group*/*'), recursive = False)
    with concurrent.futures.ThreadPoolExecutor() as executor:
    df_list = executor.map(proc_image, paths,post_norm)
    

