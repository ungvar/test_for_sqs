import boto3  # pip install boto3

# Let's use Amazon S3
session = boto3.Session(profile_name='test_user')
s3 = session.client('s3')


s3.upload_file('string.txt', 'test-bucket-for-selivaka', 'hello.txt')

with open('byte.txt', 'rb') as data:
    s3.upload_fileobj(data, 'test-bucket-for-selivaka', 'mykey')


s3.download_file('test-bucket-for-selivaka', 'hello.txt', 'string.txt')

with open('byte.txt', 'wb') as data:
    s3.download_fileobj('test-bucket-for-selivaka', 'mykey', data)