#!/bin/zsh

dir=/tmp/byplay-nix-package/byplay
rm -rf $dir
mkdir -p "$dir"

cp -r package/* $dir/
rm $dir/data/*

cp -r distribution/nix/* $dir/

target=$(pwd)/distribution/out/Byplay-nix-$(date +"%Y%m%d%H%M").zip
cd $dir && zip -r $target ./*


