#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
"""
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_config = {
    "installed": {
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
        "client_id": "685360807414-t5e24rltavr5pdsoot6dcu9d6tuuu9nt.apps.googleusercontent.com",
        "client_secret": "7e7-hHmrgFmCnnB_veMTE4-b"
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
credentials = flow.run_console()

youtube = build('youtube', 'v3', credentials=credentials)
request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q="surfing"
    )
response = request.execute()
print("First Try")
print(response)

access_token = credentials.token
refresh_token = credentials.refresh_token

f = open('refresh_token.txt', "w")
f.write(refresh_token)
f.close()
"""
from google.oauth2.credentials import Credentials
from apiclient.discovery import build
import webbrowser

def find_video(query):
    f = open('refresh_token.txt', "r")
    credentials = Credentials(
        None,
        refresh_token=f.read(),
        token_uri="https://accounts.google.com/o/oauth2/token",
        client_id="685360807414-t5e24rltavr5pdsoot6dcu9d6tuuu9nt.apps.googleusercontent.com",
        client_secret="7e7-hHmrgFmCnnB_veMTE4-b"
    )
    
    youtube = build('youtube', 'v3', credentials=credentials)
    request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=query
        )
    response = request.execute()
    response = str(response)
    video_id_idx = response.find('videoId')
    end_idx = response.find('}', video_id_idx)
    url = "https://www.youtube.com/watch?v=" + response[video_id_idx+11:end_idx-1]
    webbrowser.open(url)

if __name__ == '__main__':
    find_video("surfing")
