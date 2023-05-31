from google.auth.transport.requests import Request

class Google_credential:
    def __init__(self, token, refresh_token, token_uri,client_id, client_secret, scopes):
        self.token = token
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        
# Function to refresh the credentials if expired
def refresh_credentials(credentials):
    try:        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        return credentials
    except:
        return None