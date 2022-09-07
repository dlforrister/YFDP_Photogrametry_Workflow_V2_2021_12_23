#!/usr/bin/bash

add_exif() {
    path=$1
    cd $path
    image=$2;
    outputname="${image/.JPG/_HSV_V_fixed.JPG}";
    output="./output/${outputname}";
    eval "/home1/08531/dlforr/src/Image-ExifTool-12.44/exiftool -overwrite_original_in_place -TagsFromFile ${image} $'-all:all>all:all' ${output} -m"
    }
    
add_exif $1 $2