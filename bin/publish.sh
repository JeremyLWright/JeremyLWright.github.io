set -e 

PUBLISH_MESSAGE=`git log -1 --pretty=%B`
BUILD_DIR=`mktemp -d`

git clone git@github.com:JeremyLWright/JeremyLWright.github.io.git $BUILD_DIR
hugo --destination $BUILD_DIR
pushd $BUILD_DIR
git add -A
git commit -m"${PUBLISH_MESSAGE}"
git push
popd
echo "Site published from ${BUILD_DIR}"
