# https://accounts.google.com/o/oauth2/auth?client_id=623191355592-m31r1l98oi7r60ur695vjn2crrbl9do9.apps.googleusercontent.com&redirect_uri=https://accounts.google.com&scope=https://www.googleapis.com/auth/userinfo.email&response_type=code
# https://myaccount.google.com/u/1/?pli=1
import requests

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
CLIENT_ID = '623191355592-m31r1l98oi7r60ur695vjn2crrbl9do9.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REFRESH_TOKEN = "1//0d12S8CyPZKbRCgYIARAAGA0SNwF-L9IrsBVuxrC_AHO8Mr0i6U4aiezzOIT87QkauyyUuVUbQ3ZxwZ3Ji4Uk2ZtxEWXQvsoUAI4"
REDIRECT_URI = 'https://accounts.google.com'
AUTHORIZATION_CODE = "4%2F0AfJohXn6kgQhXeAspHZx_FuFR_u0Pb1gNbsOZJsnx9oT6CsFknnco7qx7dgN3GiAzFWuqw"


token_url = 'https://accounts.google.com/o/oauth2/token'
data = {
    'code': AUTHORIZATION_CODE,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=data)
response_data = response.json()

print(response_data)
