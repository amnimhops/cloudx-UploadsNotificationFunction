After building the app, I tried to execute it but got an error:
```bash
➜  cloudx-cf-UploadsNotificationFunction sam build
...
➜  cloudx-cf-UploadsNotificationFunction sam local invoke
Invoking app.lambda_handler (python3.9)                                                                                                                                                                                     
Local image was not found.                                                                                                                                                                                                  
Removing rapid images for repo public.ecr.aws/sam/emulation-python3.9                                                                                                                                                       
Building image...docker/credentials/store.py:21: UserWarning: docker-credential-pierone not installed or not available in PATH
```
DIAL guess is that I need the sam-cli emulation image, so I install it:
```bash
docker pull amazon/aws-sam-cli-emulation-image-python3.9:latest
```

Neither that worked. The problem was that ~/.docker/config.json was using the old Zalando
pierone registry. I removed it and the image installed correctly

Yet, the command didn't work because there was no app.py application.
- The template.yaml file defines a HelloWorldFunction.Handler that states which file/function should be present and execute: app.lambda_handler, so I create a `/app.py` file
with a `def lambda_handler()` function
- Also, noticed that lambda had a `CodeUri: hello_world/`, so I had to move the `/app.py` to `/hellow_world/app.py`
- Now it worked, but complained about "name 'println' is not defined". I used println instead of the right `print`, after it was corrected the app worked fine

Cool, the template.yaml can use the !ImportValue from other stacks already deployed, very helpful when we want to pass env vars to the lambda. Moreover, it can work with local override using the env.json file:
```
sam local invoke --env-vars env.json
```
here, the env.json file is in the root folder, but could be placed anywhere

Now, let's see how to package the project to be used in CodeDeploy:
```
sam package \
  --template-file template.yaml \
  --output-template-file packaged.yaml \
  --s3-bucket manuel-lillo-cloudx-cf-bucket
Error: Cannot use both --resolve-s3 and --s3-bucket parameters. Please use only one.
```

First try failed because it turns out that `samconfig.toml` defines the value `resolve_s3 = true`. Changed and tried again:

