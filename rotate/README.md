### Commands

```bash
AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | sed -n '2p' | cut -d "=" -f2)
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:1}

AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | sed -n '3p' | cut -d "=" -f2)
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:1}

docker image build -t rotate-lambda-dist:latest .
docker container run -d  \
    --name rotate-lambda-dist \
    --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    rotate-lambda-dist:latest
    
docker cp rotate-lambda-dist:/dist .
    
docker container stop rotate-lambda-dist
docker container rm rotate-lambda-dist
```

**For Reference: Local Steps with Virtual Environment**

> This will not work on most machines because the cryptography module contains machine dependent files.

```bash
# Create a new distribution of this Lambda function using a virtual environment.
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

cd venv/lib/python3.8/site-packages
zip -r9 ../../../../../dist/SaintsXCTFRotate.zip .
cd -
zip -g ../dist/SaintsXCTFRotate.zip function.py 
```

**For Reference: Steps without Virtual Environment**

> This does not work on Mac when using Homebrew to install Python.

```bash
pip3 install -r requirements.txt --target ./package
zip -r9 ../dist/SaintsXCTFRotate.zip ./package
zip -g ../dist/SaintsXCTFRotate.zip function.py 
```

### Resources

1. [AWS Secrets Manager Lambda Rotation Function](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-lambda-function-overview.html)
2. [Custom Lambda Rotation Function](https://github.com/aws-samples/aws-secrets-manager-ssh-key-rotation)