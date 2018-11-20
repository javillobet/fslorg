#!/bin/bash

API_VERSION=44.0
PACKAGE_PATH=$1/./package.xml

sed \$d $PACKAGE_PATH |sed \$d > temp.xml

echo "<types>" >> temp.xml
for i in $(cat $1/./package.xml |grep "\."|grep members | sed -e "s/\..*//" -e "s/^.*>//" | sort | uniq | sed -e "s/^/<members>/" -e "s/$/<\/members>/")
do
    j=$(echo $i | sed -e "s/<members>//" -e "s/<\/members>//")
    z=$1/../work/objects/$j.object
    if [ -f $z ]; then
        echo $i >> temp.xml         
    fi  
done
echo "<name>CustomObject</name>" >> temp.xml
echo "</types>" >> temp.xml

echo "<version>${API_VERSION}</version>" >> temp.xml
echo "</Package>" >> temp.xml

mv temp.xml $PACKAGE_PATH

cat $PACKAGE_PATH
echo "GENERATED"
