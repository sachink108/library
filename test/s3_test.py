import boto3
import os
import time

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAIE3SYMVMFVA7HT5A'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'

# Create an S3 client
#s3 = boto3.client('s3')
#current_milli_time = lambda: int(round(time.time() * 1000))
#curTime = current_milli_time()

#bucketname = "my-library_%s" % str(curTime)
#print ("Creating bucket %s" % bucketname)
#s3.create_bucket(Bucket=bucketname)

# Call S3 to list current buckets
#response = s3.list_buckets()

# Get a list of all bucket names from the response
#buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list
#print("Bucket List: %s" % buckets)

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print (bucket.name)

database_dir = "C:\\databases"
imgfilename = 'f866bc97-3068-488d-b48f-22cf6007a203.jpg'
image_file = os.path.join(database_dir, imgfilename)
imgdata = open(image_file, 'rb')

#print (imgdata.readlines())

s3.Bucket('my-library_1508745849196').put_object(Key=imgfilename, Body=imgdata)
