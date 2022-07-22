#!/usr/bin/bash
sourceFolder=$1

cd "/Volumes/GoogleDrive/My Drive/2018_Yasuni_Drone_Mapping/${sourceFolder}"

add_exif() {
	image=$1;
    outputname="${image/.tif/_HSV_V_fixed.tif}";
    output="./output/${outputname}";
    eval "exiftool -overwrite_original_in_place -TagsFromFile ${image} $'-all:all>all:all' ${output}"
    }

export -f add_exif

parallel -j8 add_exif {} ::: ls *.tif