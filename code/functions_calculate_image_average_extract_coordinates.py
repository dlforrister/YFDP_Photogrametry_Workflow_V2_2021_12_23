
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

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def proc_image(i):
    try:
        if any(i.endswith(s) for s in [".JPG", ".tif",".jpg"]):
            file_name = os.path.basename(i)[:-4]
            if i.endswith(".tif"):
                img = PIL.Image.open(i, mode = "r")
                meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
                data = asarray(img)
                df = pd.DataFrame({'file_name': file_name, 'flight': file_name.split("_")[5], 'image': file_name.split("_")[6], 'date': meta_dict["DateTime"], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
                img.close()
                return(df)
            else:
                img = PIL.Image.open(i, mode = "r")
                data = asarray(img)
                df = pd.DataFrame({'file_name': file_name, 'flight': file_name.split("_")[5], 'image': file_name.split("_")[6], 'date': img._getexif()[36867], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
                img.close()
                return(df)
    except:
        print("Image has issue")

def proc_image_stationary(i):
    if any(i.endswith(s) for s in [".JPG", ".tif"]):
        file_name = os.path.basename(i)[:-4]
        if i.endswith(".tif"):
            img = PIL.Image.open(i, mode = "r")
            meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
            data = asarray(img)
            df = pd.DataFrame({'file_name': file_name, 'date': meta_dict["DateTime"], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
            img.close()
            return(df)
        else:
            img = PIL.Image.open(i, mode = "r")
            data = asarray(img)
            df = pd.DataFrame({'file_name': file_name, 'date': img._getexif()[36867], 'mean_red': round(data[:, :, 0].mean(),2),'sd_red': round(data[:, :, 0].std(),2), 'mean_green': round(data[:, :, 1].mean(),2),'sd_green': round(data[:, :, 1].std(),2), 'mean_blue': round(data[:, :, 2].mean(),2),'sd_blue': round(data[:, :, 2].std(),2)}, index=[0])
            img.close()
            return(df)

   
def calc_image_average(path = False, post_norm = False):
    if post_norm == True:
        paths = list(listdir_nohidden(path+"output/"))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            df_list = executor.map(proc_image, paths)
    else:
        paths = list(listdir_nohidden(path))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            df_list = executor.map(proc_image, paths)

    df_list = list(df_list)
    df = pd.concat(list(df_list))
    print("Writing CSV with mean reflectance for {} images".format(len(df.file_name)))
    if post_norm == True:
        df.to_csv(path+"output/" "image_mean_reflectance.csv")
    else:
        df.to_csv(path + "image_mean_reflectance.csv")

def calc_image_average_stationary(path = False):
    glob.glob(os.path.join(path,"*"), recursive = False)
    paths = list(listdir_nohidden(path))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_list = executor.map(proc_image_stationary, paths)
    
    df_list = list(df_list)
    df = pd.concat(list(df_list))
    print("Writing CSV with mean reflectance for {} images".format(len(df.file_name)))        
    df.to_csv(path + "image_mean_reflectance.csv")


def extract_gps_metadat(i):
    if any(i.endswith(s) for s in [".JPG", ".tif"]):
        gpsdata = gpsphoto.getGPSData(i)
        try:
            return(pd.DataFrame({"Label":os.path.basename(i), "X":	gpsdata['Longitude'], "Y": gpsdata['Latitude'], "Z": gpsdata['Altitude']}, index=[0]))
        except:
            return(pd.DataFrame({"Label":os.path.basename(i), "X": "", "Y": "", "Z": ""}, index=[0]))

def extract_gps_metadat_multi_thred(path):
    paths = list(listdir_nohidden(path))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_list = executor.map(extract_gps_metadat, paths)
    df_list = list(df_list)
    df = pd.concat(list(df_list))
    print("Writing CSV with GPS info for {} images".format(len(df.Label)))        
    df.to_csv(path + "images_metadata_gps.csv",index=False)

