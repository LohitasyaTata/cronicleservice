# cronicleservice
Cronicle as ECS service

Hi,

Cronicle is an OSS developed by jhuckaby | https://github.com/jhuckaby/Cronicle.git
Cronicle is a multi-server task scheduler and runner, with a web based front-end UI. It handles both scheduled, repeating and on-demand jobs, targeting any number of worker servers, with real-time stats and live log viewer. It's basically a fancy Cron replacement written in Node.js. You can give it simple shell commands, or write Plugins in virtually any language.

jhuckaby has developed this using js and other languages.

But limitations were this application can be run as stand-alone/monolithic server or master-slave architecture.

To minimize this I have dockerized this application into a docker image which can be used as AWS ECS microservice.

Please follow the below steps for the setup.

1) Confire the storage class as AWS S3 bucket and conigure the config.json

2) Build the docker file in local system and push in AWS ECR.

3) Make sure the ec-2 instance where the service running has proper read-write access to push data

4) Cronicle stores all the job data in AWS S3 as a storage space.

5) Before registring the new task make sure to delete folders under respective bucket mentioned. This is done because a stamp is created aganist the server Ip and master hostname in S3 s3://<bucket-name>/cronicle_service/global/ folder marking that deployed cronicle service as master node.
But when deployed again we have the same S3 bucket which confused the newly deployed cronicle serive marking that there is already a master service hence serive will be unsteady and can't detect who is master. 

If there is any CICD for aws ecs service deploy you can add these lines before creating task defination.
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/api_keys.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/api_keys/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/categories.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/categories/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/plugins.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/plugins/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/server_groups.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/server_groups/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/servers.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/servers/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/users.json 
+ aws s3 rm --recursive s3://<bucket-name>/cronicle_service/global/users/ 
+ aws s3 rm s3://<bucket-name>/cronicle_service/global/state.json 
