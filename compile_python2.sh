#!/bin/bash

dir_name="package/python"
rm -rf $dir_name/
mkdir -p $dir_name/
cp -r byplay $dir_name/byplay/
find $dir_name/byplay -name '__pycache__'  -exec rm -rf {} \;
3to2 --no-diffs -w -n $dir_name/byplay

find ./$dir_name/byplay -type f -exec sed -i '' 's#from typing .*##' {} \;
