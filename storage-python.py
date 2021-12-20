from google.cloud import storage

bucketName = 'bucket_name'
projectName = 'proyecto'
fileName='/temp/zoneYPF.kml' 
crdl = service_account.Credentials.from_service_account_file('settings/storage-david-vasquez.json')

client = storage.Client(project=projectName,credentials=crdl)

# https://console.cloud.google.com/storage/browser/[bucket-id]/
#https://storage.cloud.google.com/looker-personal-parameter-prod/temp/zoneYPF.kml

bucket = client.get_bucket(bucketName)
# Then do other things...
blob = bucket.get_blob('temp/zoneYPF.kml')
data=blob.download_as_string()

data2=data.decode('UTF-8')

data
