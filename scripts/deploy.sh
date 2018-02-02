set -x
pip install transcriptic
cp scripts/.transcriptic ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$EMAIL/$email/g" ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$TOKEN/$token/g" ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$ORGANIZATION_ID/$organization_id/g" ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$USER_ID/$user_id/g" ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$FEATURE1/$feature1/g" ~/.transcriptic
cat ~/.transcriptic
sed -i "s/\$FEATURE2/$feature2/g" ~/.transcriptic
cat ~/.transcriptic
transcriptic projects
transcriptic packages
transcriptic build-release
transcriptic upload-release release.zip pk1b6etjw8x2ep
