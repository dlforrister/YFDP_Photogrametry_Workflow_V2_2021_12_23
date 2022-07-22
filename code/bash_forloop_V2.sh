
#Phantom
sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images_V2/Phantom"
cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"
destImage_rel="2018_Oct_02_Phantom_Flight_1_48.JPG" 
destImage="${sourceFolder}/${destImage_rel}"

ls *.JPG | xargs -n 1 -P 9 -I @ python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $sourceFolder -destImage $destImage -image @

#Phantom Reflectance Tartget
sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images_V2/Phantom"
reflectance_folder="2_2018_Oct/2018_Oct_2_V2/Reflectance/Phantom"
cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${reflectance_folder}"
destImage_rel="2018_Oct_02_Phantom_Flight_1_48.JPG" 
destImage="${sourceFolder}/${destImage_rel}"

ls *.JPG | xargs -n 1 -P 9 -I @ python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $reflectance_folder -destImage $destImage -image @ -reflectance_target "yes"


python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $reflectance_folder -destImage $destImage -image "2018_Oct_2_Flight_1_Reflectance_Pre_1.JPG" -reflectance_target



#MAPIR
sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_1_3"

cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"

destImage_rel="2018_Oct_02_MAPIR_Flight_1_18_A.tif" 

destImage="${sourceFolder}/${destImage_rel}"

ls *.tif | xargs -n 1 -P 9 -I @ python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $sourceFolder -destImage $destImage -image @

#MAPIR second round

sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_4_5"

cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"

destImage_rel="2018_Oct_02_MAPIR_Flight_1_18_A.tif" 

destImage="${sourceFolder}/${destImage_rel}"

ls *.tif | xargs -n 1 -P 9 -I @ python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $sourceFolder -destImage $destImage -image @



#MAPIR Reflectance Target

sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_4_5"

cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"

destImage_rel="2018_Oct_02_MAPIR_Flight_1_18_A.tif" 

destImage="${sourceFolder}/${destImage_rel}"

ls *.tif | xargs -n 1 -P 9 -I @ python /Users/dlforrister/Documents_Mac/CODE_GIT_HUB_2017_Aug_31/YFDP_Photogrametry_Workflow_V2_2021_12_23/code/normalize_single_image.py -sourceFolder $sourceFolder -destImage $destImage -image @









#exif tool
sourceFolder="2_2018_Oct/2018_Oct_2_V2/Proccessed_Images/MAPIR/Processed_1/Camera_Settings_Flights_1_3"

cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"

ls *.tif

image="2018_Oct_02_MAPIR_Flight_3_98_A.tif"
output="./output/2018_Oct_02_MAPIR_Flight_3_98_A_HSV_V_fixed.tif" 

add_exif() {
	image=$1;
    outputname="${image/.tif/_HSV_V_fixed.tif}";
    output="./output/${outputname}";
    eval "exiftool -overwrite_original_in_place -TagsFromFile ${image} $'-all:all>all:all' ${output}"
    }


export -f add_exif
add_exif "2018_Oct_02_MAPIR_Flight_3_98_A.tif"

ls 2018_Oct_02_MAPIR_Flight_3_9*.tif | xargs -n 1 -P 9 -I @ add_exif @

parallel -j8 add_exif {} ::: ls *.tif

for i in ls 2018_Oct_02_MAPIR_Flight_3_9*.tif


for f in 2018_Oct_02_MAPIR_Flight_3_9*.tif; do
  add_exif $f
done