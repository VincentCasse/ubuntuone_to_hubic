from ubuntuOne import UbuntuOne
from hubic import Hubic
import uuid
import time

def for_each_current_folder(content_path,chunk_size,name):
	for item in ubuntu.get_list(content_path,name):
		# if this is a directory, we create the directory in hubic 
		# and we explore this directory
		if item['kind'] == 'directory':
			print "Create directory : " + item['path']
			hubic.create_folder(item['path'])

			print "Discover directory : " + item['path']
			for_each_current_folder(content_path,item['path'])

		#if this is a file, we verify his size
		# if size > chunk, we had to create a segmented file
		# if not, we get it in memory and upload directly in hubic
		elif item['kind'] == 'file':
			if item['size'] > chunk_size:
				print "Copy file : " + item['path']
				stream = ubuntu.get_stream_file(item['content_path'])
				if stream.status_code == 200: 
					i = 1
					
					# get infos
					the_uuid = str(uuid.uuid4())
					timestamp =  str(time.time())
					size = str(item['size'])
					manifest_link = "/".join([the_uuid,timestamp,size])
					# print manifest_link
					
					for chunk in stream.iter_content(chunk_size):	
						number = str('{:08}'.format(i))
						# print number
						hubic.upload_segment_big_file(manifest_link,number,chunk)
						i=i+1

					#Create manifest
					hubic.create_manifest_big_file(manifest_link,item['path'])
				
				print "End Copy file : " + item['path']
			else:
				print "Copy file : " + item['path']
				content = ubuntu.get_file(item['content_path'])
				hubic.upload_object(item['path'],content)

# ubuntu one informations
uo_login = "xxx"
uo_pass = "xxx"
content_path = '~/Ubuntu One'

# hubic informations
AK = 'xxxx'
AS = 'xxxx'
redirect = 'https://beveloper.fr/showHubicCode/'
#refresh_token = 'xxxx'
destination_folder = '/ubuntu_one'

# general informations
chunk_size=1048576 #1M

#Open connections
ubuntu = UbuntuOne(uo_login,uo_pass,'Ubuntu One @ python [migrate-to-hubic]')
print "Connection to Ubuntu One : ok"
hubic = Hubic(AK,AS, redirect, refresh_token=None, prefix_destination=destination_folder)
print "Connection to Hubic : ok"

# foreach element in ubuntu one
for_each_current_folder(content_path,chunk_size,'')


