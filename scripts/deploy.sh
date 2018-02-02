set -x
echo "hi I'm the start $PWD"
env | sort
cp scripts/.transcriptic ~/.transcriptic
pipenv install
transcriptic packages
transcriptic build-release
transcriptic upload-release release.zip pk1b6etjw8x2ep
echo "hi I'm the end"
