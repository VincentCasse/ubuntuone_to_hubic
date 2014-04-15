from ubuntuOne import UbuntuOne
from hubic import Hubic

def for_each_current_folder(content_path,name):
	for item in ubuntu.get_list(content_path,name):
		if item['kind'] == 'directory':
			print "Create directory : " + item['path']
			hubic.create_folder(item['path'])

			print "Discover directory : " + item['path']
			for_each_current_folder(content_path,item['path'])

		elif item['kind'] == 'file':
			print "Copy file : " + item['path']
			content = ubuntu.get_file(item['content_path'])
			hubic.upload_object(item['path'],content)

#ubuntu one informations
uo_login = "xxx"
uo_pass = "xxx"
content_path = '~/Ubuntu One'

#hubic informations
AK = 'xxxx'
AS = 'xxxx'
redirect = 'https://beveloper.fr/showHubicCode/'
#refresh_token = 'xxxx'
destination_folder = '/ubuntu_one'

#Open connections
ubuntu = UbuntuOne(uo_login,uo_pass,'Ubuntu One @ python [migrate-to-hubic]')
print "Connection to Ubuntu One : ok"
hubic = Hubic(AK,AS, redirect, refresh_token=None, prefix_destination=destination_folder)
print "Connection to Hubic : ok"

# foreach element in ubuntu one
for_each_current_folder(content_path,'')


