import base64
import requests
from requests.exceptions import HTTPError
import urllib
import json

class BadRequest(Exception):
    """An invalid request was submitted."""


class Unauthorized(Exception):
    """The provided email address and password were incorrect."""

class DestinationAlreadyExist(Exception):
    """Destination folder already exist"""

class Hubic:

    def __init__(self, app_key, app_secret, redirect_uri,refresh_token=None, prefix_destination="/"):
        self.app_key = app_key
        self.app_secret = app_secret
        self.prefix_destination = prefix_destination

        if refresh_token == None:
            url = "https://api.hubic.com/oauth/auth/?client_id=" + app_key + "&redirect_uri=" + urllib.quote_plus(redirect_uri) + "&scope=credentials.r&response_type=code"
            print "Go on " + url
            code = raw_input("And enter your code here : ")
            
            application_token = base64.b64encode(app_key + ":" + app_secret) 
            url = "https://api.hubic.com/oauth/token/" 
            response = requests.post( url, data={ "code": code, "grant_type": "authorization_code", "redirect_uri": redirect_uri},
                 headers={'Authorization': 'Basic ' + application_token })
            
            if response.status_code == 400:
                raise BadRequest(response.content)
            elif not response.ok:
                # Unauthorized
                raise Unauthorized(response.json())

            self.hubic_refresh_token = response.json()["refresh_token"]
            self.hubic_token = response.json()["access_token"]
        else:
            self.hubic_refresh_token = refresh_token
            self.hubic_token = "falsetoken"

        #Get openstacks credentials
        self.openstack_token = self.get_openstack_credentials()

        #Create prefix destination
        try:
            prefix_exist = self._os_call('get','default'+self.prefix_destination)
            if prefix_exist.status_code == 200:
                raise DestinationAlreadyExist()

        except HTTPError as e:
            if e.response.status_code == 404:
                self._os_call('put','default'+self.prefix_destination,None,{'Content-Type':'application/directory'});
                pass
            else:
                raise

    def _renew_token(self, method, uri, data, headers, limit):
        application_token = base64.b64encode(self.app_key + ":" + self.app_secret) 
        url = "https://api.hubic.com/oauth/token/" 
        response = requests.post( url, data={ "grant_type": "refresh_token", "refresh_token": self.hubic_refresh_token},headers={'Authorization': 'Basic ' + application_token })
        self.hubic_token = response.json()["access_token"]

        return self._hubic_call(method, uri, data, headers, limit)

    def _hubic_call(self, method, uri, data=None, headers={}, limit=3):
        req = getattr(requests, method.lower())
        headers['Authorization'] = "Bearer " + self.hubic_token
        url = 'https://api.hubic.com/1.0/' + uri 

        result = req(url, headers=headers, data=data)
        if result.status_code == 401 and result.json()['error'] == 'invalid_token':
            if limit > 0:
                limit = limit - 1
                return self._renew_token(method,uri,data,headers,limit)
        else:
            result.raise_for_status()
        return result

    def _os_renew_token(self, method, uri, data, headers, limit):
        self.get_openstack_credentials()
        return self._os_call(method, uri, data, headers, limit)

    def _os_call(self, method, uri, data=None, headers={}, limit=3):
        req = getattr(requests, method.lower())
        headers['X-Auth-Token'] = self.os_token
        url = self.os_endpoint + '/' + uri 

        result = req(url, headers=headers, data=data)
        if result.status_code == 403:
            if limit > 0:
                limit = limit - 1
                return self._os_renew_token(method,uri,data,headers,limit)
        else:
            result.raise_for_status()
        return result

    def get_openstack_credentials(self):
        openstack_token = self._hubic_call('GET', 'account/credentials').json()
        self.os_endpoint = openstack_token['endpoint']
        self.os_token = openstack_token['token']

    def create_folder(self,name):
        return self._os_call('put','default'+self.prefix_destination +name,None,{'Content-Type':'application/directory'});

    def upload_object(self,name,data):
        return self._os_call('put','default'+self.prefix_destination +name,data);

    def create_manifest_big_file(self,manifest_link,name):
        headers = { 'X-Object-Manifest': 'default_segments/' + manifest_link}
        return self._os_call('put','default'+self.prefix_destination +name,data=None,headers=headers);

    def upload_segment_big_file(self,manifest_link,number,content):
        return self._os_call('put','default_segments/'+manifest_link + '/' + number,data=content);

    def delete_object(self,name):
        return self._os_call('delete','default'+name);

