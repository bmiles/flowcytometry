set -x
source ~/virtualenv/python2.7/bin/activate
pip install transcriptic
cp scripts/.transcriptic ~/.transcriptic
cat ~/.transcriptic
cat ~/.transcriptic | sed "s/\$EMAIL/$email/g" > ~./transcriptic
cat ~/.transcriptic
cat ~/.transcriptic | sed "s/\$TOKEN/$token/g" > ~./transcriptic
cat ~/.transcriptic
cat ~/.transcriptic | sed "s/\$ORGANIZATION_ID/$organization_id/g" > ~./transcriptic
cat ~/.transcriptic
cat ~/.transcriptic | sed "s/\$USER_ID/$user_id/g" > ~./transcriptic
cat ~/.transcriptic
transcriptic packages
transcriptic build-release
transcriptic upload-release release.zip pk1b6etjw8x2ep
