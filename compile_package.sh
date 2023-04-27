#!/bin/bash

function clear_and_copy() {
    rm -rf $1/
    mkdir -p $1/
    cp -r byplay $1/byplay/
}

dir_name="package/python2.7"
clear_and_copy $dir_name
3to2 --no-diffs -w -n $dir_name/byplay

find ./$dir_name/byplay -type f -exec sed -i '' 's#from typing .*##' {} \;

clear_and_copy "package/python3"

cd package
find . -name '__pycache__'  -exec rm -rf {} \;
find . -name '*.DS_Store'  -exec rm -rf {} \;

rm package.zip

zip -r package.zip ./*

mv package.zip ..

#target_dir="/Users/vadim/Library/Application Support/Byplay Desktop/plugins/byplay-houdini/current/"
#echo "Removing $target_dir"
#rm -rf $target_dir/*
#cp -r ./* $target_dir/
