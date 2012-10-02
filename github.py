import settings
import requests
import json

def get_token(code):
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
    token = json.loads(response.content).get('access_token', None)
    return token

def get_user_data(access_token):
    params = {"access_token": access_token}
    response = requests.get(settings.GH_API_URL + 'user', params=params, headers=settings.ACCEPT_HEADERS)
    user_data = response.json
    user_data['access_token'] = access_token
    return user_data