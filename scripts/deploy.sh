set -x
pip install transcriptic
cp scripts/.transcriptic ~/.transcriptic
sed -i "s/\$EMAIL/$email/g" ~/.transcriptic
sed -i "s/\$TOKEN/$token/g" ~/.transcriptic
sed -i "s/\$ORGANIZATION_ID/$organization_id/g" ~/.transcriptic
sed -i "s/\$USER_ID/$user_id/g" ~/.transcriptic
sed -i "s/\$FEATURE1/$feature1/g" ~/.transcriptic
sed -i "s/\$FEATURE2/$feature2/g" ~/.transcriptic
cat ~/.transcriptic
transcriptic --config ~/.transcriptic projects
transcriptic --config ~/.transcriptic packages
transcriptic --config ~/.transcriptic build-release
transcriptic --config ~/.transcriptic upload-release release.zip pk1b6etjw8x2ep > out
cat out
curl "https://secure.transcriptic.com/$organization_id/protocols/pr1b6hu37yypk8/publish" -X POST  -H 'Content-Type: application/json; charset=UTF-8' -H 'Accept: application/json' -H "X-User-Token: $token" -H 'X-User-Email: $email" 
