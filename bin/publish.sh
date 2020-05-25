set -e 

PUBLISH_MESSAGE=`git log -1 --pretty=%B`
BUILD_DIR=`mktemp -d`

git clone git@github.com:JeremyLWright/JeremyLWright.github.io.git $BUILD_DIR
hugo
rm -rf $BUILD_DIR/*
mv public/* $BUILD_DIR
cp CNAME $BUILD_DIR
pushd $BUILD_DIR
git add -A
git commit -m"${PUBLISH_MESSAGE}"
git push
popd
echo "Site published from ${BUILD_DIR}"
