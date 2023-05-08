import boto3  # pip install boto3

# Let's use Amazon S3
session = boto3.Session(profile_name='test_user')
s3 = session.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)