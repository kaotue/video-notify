STAGE=dev
echo STAGE=$STAGE

sam build
sam deploy \
--stack-name kaotue-vn-$STAGE \
--s3-bucket kaotue-vn-$STAGE \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides \
  Stage=$STAGE \
  LineChannelAccessToken=$LINE_CHANNEL_ACCESS_TOKEN \
