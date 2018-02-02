set -x
source ~/virtualenv/python2.7/bin/activate
echo "hi I am the start $PWD"
env | sort
cp scripts/.transcriptic ~/.transcriptic
transcriptic packages
transcriptic build-release
transcriptic upload-release release.zip pk1b6etjw8x2ep
echo "hi I'm the end"
