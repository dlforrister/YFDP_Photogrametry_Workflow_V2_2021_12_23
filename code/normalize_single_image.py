import sys, os
os.chdir("/Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/")
import histogram_specification_v4_HSV_simple as HistSpecHSV
import argparse



parser = argparse.ArgumentParser()
parser.add_argument(
    '-sourceFolder', help='Directory with images to be noromalized', required=True
    )

parser.add_argument(
    '-destImage',
    help='Path and name of Destimage - image whose values will be used for normalization ',
    required=True
)

parser.add_argument(
    '-output',
    help='Relative path of output folder, defaults to output',
    default="/output/"
)

parser.add_argument(
    '-image',
    help='image to be normalized', required=True
)

parser.add_argument(
    '-reflectance_target',
    help='yes or no if running reflectance target', required=False, default='no')



if __name__ == '__main__':
    arguments = parser.parse_args()
 
    #create output folder
    destOutput = "/Volumes/Seagate_14_TB/Google_Drive_Back_up/2018_Yasuni_Drone_Mapping/" + arguments.sourceFolder + arguments.output
    refimage = "/Volumes/Seagate_14_TB/Google_Drive_Back_up/2018_Yasuni_Drone_Mapping/" + arguments.destImage
    if not os.path.exists(destOutput):
        print("creating output folder at {}".format(destOutput))
        os.mkdir(destOutput)
    #make complete path of image
    srcImg = "/Volumes/Seagate_14_TB/Google_Drive_Back_up/2018_Yasuni_Drone_Mapping/" + arguments.sourceFolder + "/" + arguments.image
    if ".JPG" in os.path.basename(srcImg):
        outName = destOutput + os.path.basename(srcImg).split('.JPG')[0] + '_HSV_V_fixed.JPG'

    if ".tif" in os.path.basename(srcImg):
        outName = destOutput + os.path.basename(srcImg).split('.tif')[0] + '_HSV_V_fixed.tif'
    if not os.path.exists(outName):
        print(srcImg)
        #process a single image    
        HistSpecHSV.ImageTransform(srcImg, refimage,destOutput,arguments.reflectance_target)

