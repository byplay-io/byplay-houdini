#!/bin/zsh

dir=/tmp/byplay-win-package/byplay
rm -rf $dir
mkdir -p "$dir"

cp -r package/* $dir/
rm $dir/data/*

cp -r distribution/windows/* $dir/

target=$(pwd)/distribution/out/Byplay-Windows-$(date +"%Y%m%d%H%M").zip
echo $target
cd $dir && zip -r $target ./*


