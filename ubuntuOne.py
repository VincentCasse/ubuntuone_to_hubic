import json
import oauth2
import requests
from oauth2 import Request as Requ, SignatureMethod_HMAC_SHA1

class BadRequest(Exception):
    """An invalid request was submitted."""

class Unauthorized(Exception):
    """The provided email address and password were incorrect."""

class UbuntuOne:

    def __init__(self, email_address, password, description, otp=None):
        """Aquire an OAuth access token for the given user."""
        # Issue a new access token for the user.
        params = {
            'email': email_address,
            'password': password,
            'token_name': description,
        }
        if otp is not None:
            params['otp'] = otp
        response = requests.post(
            'https://login.ubuntu.com/api/v2/tokens/oauth',
            data=json.dumps(params),
            headers={'content-type': 'application/json',
                     'accept': 'application/json'})

        if response.status_code == 400:
            raise BadRequest(response.content)
        elif not response.ok:
            # Unauthorized
            raise Unauthorized(response.json())

        data = response.json()
        self.consumer = oauth2.Consumer(data['consumer_key'], data['consumer_secret'])
        self.token = oauth2.Token(data['token_key'], data['token_secret'])
        self.client = oauth2.Client(self.consumer, self.token)

    def get_list(self, content_path, folder):
        request_token_url = "https://one.ubuntu.com/api/file_storage/v1/" +  content_path.replace(' ','%20')  + "/" + folder.replace(' ','%20') + "?include_children=true"
        resp,content = self.client.request(request_token_url, "GET")
        return json.loads(content)['children']

    def get_file(self, content_path):
        request_token_url = "https://files.one.ubuntu.com" +  content_path.replace(' ','%20') 
        resp,content = self.client.request(request_token_url, "GET")
        return content

    def get_stream_file(self,content_path):
        url = "https://files.one.ubuntu.com" +  content_path.replace(' ','%20')

        # Get Oauth1 signature
        req = Requ.from_consumer_and_token(self.consumer,
            token=self.token, http_method='GET', http_url=url,
            parameters=None, body='')

        req.sign_request(SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        realm = "https://files.one.ubuntu.com"
        header = req.to_header(realm=realm)

        return requests.get(url, stream=True, headers=header)