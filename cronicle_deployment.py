import os
import git
import pathlib
import pip

import zipfile
import shutil
import logging
import boto3
from botocore.exceptions import ClientError
import sys


if(len(sys.argv) < 6):
    print("Insufficient Arguments.")
    exit(1)

mode = sys.argv[1]
repository_mf = sys.argv[2]
repository_ps = sys.argv[3]
repository_cf = sys.argv[4]
workspace = sys.argv[5]
environment = sys.argv[6]
print("Enviroment:- " + environment)
default_code_directory = workspace + '/code'
mf_path = default_code_directory + '/amccore'
ps_path = default_code_directory + '/ps-verification-bflmfutilslib'
cf_path = default_code_directory + '/mfconfig'

s3_bucket_name = 'bfsenvconfig'
s3_object_name = 'amc-cronicle-worker/code.zip'
code_zip_file_path = default_code_directory + '.zip'

print('Workspace : ' + workspace)
print('Default Code Directory : ' + default_code_directory)
print('Code Zip Path : ' + code_zip_file_path)
print('MFcore repository path : ' + mf_path)
print('PA-Verification-bflmfutilslib repository path : ' + ps_path)
print('MFCOnfig repository path : ' + cf_path)


if (environment == "NPD"):
    s3_object_name = 'npd/' + s3_object_name
    branch_name = "DEV"
elif (environment == "NPQ"):
    s3_object_name = 'npq/' + s3_object_name
    branch_name = "QA"
elif (environment == "NPU"):
    s3_object_name = 'npu1/' + s3_object_name
    branch_name = "N2P"
elif (environment == "PROD"):
    s3_object_name = 'prd/' + s3_object_name
    s3_bucket_name = 'bfsd-prod-envconfigs-mum'
    branch_name = "PROD"
elif (environment == "N2P"):
    s3_object_name = 'n2p/' + s3_object_name
    branch_name = "BFL_N2P"
elif (environment == "BFL_PROD"):
    s3_object_name = 'bpr/' + s3_object_name
    branch_name = "BFL_PROD"
elif(environment == "AMC-NPD"):
    s3_object_name = 'npd/amc/' + s3_object_name
    branch_name = "AMC_NPD"


class LambdaDeployment():

    def __init__(self, code_directory2):
        self.default_code_directory = code_directory2+"/"
        print('Constructor Default Directory : ' + self.default_code_directory)


    def code_download(self, repository_mf, repository_ps, repository_cf, brch_name, mf_path, ps_path, cf_path):
        print("Starting code_prep....")
        repository_mf = repository_mf.replace("http://", "http://bfsduser:bfsduser@")
        repository_ps = repository_ps.replace("http://", "http://bfsduser:bfsduser@")
        repository_cf = repository_cf.replace("http://", "http://bfsduser:bfsduser@")
        print("repository_mf :- "+repository_mf)
        print("repository_ps :- "+repository_ps)
        print("repository_cf :- "+repository_cf)

        self.delete_directory_recursively(self.default_code_directory)

        repo_mf = git.Repo.clone_from(repository_mf, mf_path, branch=brch_name)
        repo_ps = git.Repo.clone_from(repository_ps, ps_path, branch=brch_name)
        repo_cf = git.Repo.clone_from(repository_cf, cf_path, branch=brch_name)
        print(repo_mf)
        print(repo_ps)
        print(repo_cf)
        print("BRANCH_NAME:",brch_name)
        local_cfg = open(cf_path+"/MFConfig/mfcore/local.cfg", "r")

        print("Deleting .git direcotry...")
        self.delete_directory_recursively(mf_path + "/.git")
        self.delete_directory_recursively(ps_path + "/.git")
        self.delete_directory_recursively(cf_path + "/.git")
        print(".git directory deleted.")
        print('Installing requirements..')
        #os.system('sh yum_script.sh '+ self.default_code_directory +' '+mf_path+' '+ps_path)
        

        print("....Ending code_prep")


    def install_dependencies(self, mf_path, ps_path):
        print("Starting install_dependencies....")
        print("install_dependencies -> default_code_directory : " + self.default_code_directory)
        print('Installing modules...')
       
        pip.main(['download', '-t', self.default_code_directory, '-r', mf_path + '/app/requirements.txt'])
        
        #        ps_path + '/PS-Verification-BFLMFutilsLib'])
        print('Installation complete.')   
        print("....Ending install_dependencies")         
    
    
    def create_zip(self):
        #self.default_code_directory = self.get_code_directory(self.default_code_directory)
        print("Starting create_zip....")
        print("create_zip -> default_code_directory : " + self.default_code_directory)

        shutil.make_archive('code', 'zip', self.default_code_directory)
        print('Zip file created successfully.')
        print("....Ending create_zip")


    def upload_zipfile_s3(self, file_path, s3_bucket_name, s3_object_name):
        print("Zipped files upload to S3 bucket started....")
        s3_client = boto3.client('s3')
        try:
            print("Uploading to object "+s3_bucket_name+"/"+s3_object_name+"...")
            response = s3_client.upload_file(
                file_path, s3_bucket_name, s3_object_name)
            print(response)
            print("Zipped files upload to S3 bucket complete.")
        except ClientError as e:
            logging.error(e)
            print(e)
            return False
        return True


    def upload_to_lambda(self, lambda_function_name, s3_bucket_name, s3_object_name):
        print("Zipped files upload to Lambda from S3 bucket started....")
        client = boto3.client('lambda')
        response = client.update_function_code(
            FunctionName=lambda_function_name,
            S3Bucket=s3_bucket_name,
            S3Key=s3_object_name,
        )
        print(response)
        print("Zipped files upload to Lambda complete.")


    def delete_directory_recursively(self, dir_path):
        if (os.path.isdir(dir_path)):
            for root, dirs, files in os.walk(dir_path):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)
            shutil.rmtree(dir_path)


    def get_code_directory(self, code_directory1):
    
        required_file = pathlib.Path(code_directory1 + '/requirements.txt')

        if not required_file.exists():
            print('Scanning Code Directory....')
            directory = []
            for x in os.scandir(code_directory1):
                if x.is_dir(): 
                    print('Directory : ' + x.name)
                    directory.append(x.name)
                    print(directory)

            if directory:
                print("Path Modified : " + code_directory1 + '/' + directory[0])
                return  code_directory1 + '/' + directory[0]

        return code_directory1


x = LambdaDeployment(default_code_directory)


if (mode == 'code_download'):
    x.code_download(repository_mf, repository_ps, repository_cf,branch_name, mf_path, ps_path, cf_path)
elif (mode == 'install_dependencies'):
    x.install_dependencies(mf_path, ps_path)
elif (mode == 'create_zip'):
    x.create_zip()
elif (mode == 'upload_zipfile_s3'):
    x.upload_zipfile_s3(code_zip_file_path, s3_bucket_name, s3_object_name)
