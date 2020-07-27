#!/bin/bash

rm -rf package/python2.7libs/
mkdir -p package/python2.7libs/
cp -r byplay package/python2.7libs/byplay/
3to2 --no-diffs -w -n package/python2.7libs/byplay

find ./package/python2.7libs/byplay -type f -exec sed -i '' 's#from typing .*##' {} \;
