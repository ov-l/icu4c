# /bin/bash

# This script updates the version of ICU in the project.

# Read version.txt

VERSION=$(cat version.txt)
VERSION_DASH=$(echo $VERSION | sed 's/\./-/g')
VERSION_UNDERSCORE=$(echo $VERSION | sed 's/\./_/g')

# Update the version in the project files
echo "Updating ICU version to $VERSION..."
mkdir -p temp
cd temp
curl -L -o src.tgz https://github.com/unicode-org/icu/releases/download/release-$VERSION_DASH/icu4c-$VERSION_UNDERSCORE-src.tgz
if [ $? -ne 0 ]; then
    echo "Failed to download ICU version $VERSION"
    exit 1
fi
tar -xzf src.tgz 
if [ $? -ne 0 ]; then
    echo "Failed to extract ICU version $VERSION"
    exit 1
fi

curl -L -o data.zip https://github.com/unicode-org/icu/releases/download/release-$VERSION_DASH/icu4c-$VERSION_UNDERSCORE-data.zip
if [ $? -ne 0 ]; then
    echo "Failed to download ICU data version $VERSION"
    exit 1
fi
unzip -o data.zip 
if [ $? -ne 0 ]; then
    echo "Failed to extract ICU data version $VERSION"
    exit 1
fi

cp -r data  icu/source/

cd icu/source

./runConfigureICU Linux && make

if [ $? -ne 0 ]; then
    echo "Failed to configure and build ICU version $VERSION"
    exit 1
fi

rm data/in/icudt*.dat
rm -rf data/out

ICU_DATA_FILTER_FILE=../../../u_data.json ./runConfigureICU Linux --with-data-packaging=common
if [ $? -ne 0 ]; then
    echo "Failed to configure ICU data packaging for version $VERSION"
    exit 1
fi

make

if [ $? -ne 0 ]; then
    echo "Failed to build ICU data for version $VERSION"
    exit 1
fi

cd data

make

if [ $? -ne 0 ]; then
    echo "Failed to build ICU data output for version $VERSION"
    exit 1
fi

# Move the built data to the appropriate directory
mv out/icudt*.dat ../../../../

cd ../../../../

python update.py --dat-path icudt*.dat --engine-root ./

if [ $? -ne 0 ]; then
    echo "Failed to update ICU data in the project"
    exit 1
fi