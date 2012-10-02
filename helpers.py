def get_user(self, access_token):
    	params = {"access_token": access_token}
    	user = requests.get(settings.GH_API_URL + 'user', params=params, headers=settings.ACCEPT_HEADERS)
    	return user

def get_token(self):
    data = {
        "client_id": settings.GH_CLIENT_ID,
        "client_secret": settings.GH_CLIENT_SECRET,
        "code": code
    }
    response = requests.post(
        settings.GH_ACCESS_TOKEN_URL,
        data=data,
        headers=settings.ACCEPT_HEADERS
    )
    token = json.loads(response.text)['access_token']
    user = get_user(token)