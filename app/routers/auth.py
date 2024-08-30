import requests
from fastapi import APIRouter, Request, HTTPException, Response
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse
import os

router = APIRouter()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
CLIENT_SECRETS_FILE = "app/client_secret_37544745732-puoc20jif076bgr2r1qm1gs1chhp5beg.apps.googleusercontent.com.json"  # Path to your downloaded JSON file
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.readonly'
]

@router.get("/login")
async def login(request: Request):

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = request.url_for("callback")

    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def callback(request: Request):
    state = request.query_params.get('state')

    if state != request.session.get('state'):
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = request.url_for("callback")

    try:
        flow.fetch_token(authorization_response=request.url._url)

        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)
        return RedirectResponse(url="/drive/list-files")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/logout")
async def logout(request: Request, response: Response):
    credentials = request.session.get('credentials')
    if credentials:
        token = credentials.get('token')
        if token:
            revoke_google_token(token)


    # Clear the session
    request.session.clear()
    response.delete_cookie(key="session")
    return RedirectResponse(url="/auth/login")


def revoke_google_token(token):
    revoke_url = "https://oauth2.googleapis.com/revoke"
    response = requests.post(revoke_url, params={"token": token})
    return response.status_code == 200


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
