import os
import requests
from fastapi import FastAPI, Header, HTTPException
from typing import Union
from pydantic import BaseModel
from atproto import Client, client_utils

app = FastAPI()


class SkeetRequest(BaseModel):
    content: str
    authorization: str = Header(None)


class TootRequest(BaseModel):
    content: str


@app.get("/")
def health_check():
    return {}


@app.post("/skeet")
def new_skeet(skeet_request: SkeetRequest):
    authorization = skeet_request.authorization
    if authorization:
        return HTTPException(status_code=401, detail="Unauthorized.")
    client = Client()
    client.login(os.getenv('BSKY_USERNAME', 'Bluesky username not found'),
                 os.getenv('BSKY_PASSWORD', 'Bluesky password not found'))
    skeetResponse = client.send_post(skeet_request.content)
    return skeetResponse


@app.post("/toot")
def new_skeet(status_request: TootRequest):
    tootResponse = requests.post(f"https://{os.getenv('MASTODON_BASE_URL')}/api/v1/statuses", data={
        'status': status_request.content}, headers={"Authorization": f"Bearer {os.getenv('MASTODON_TOKEN')}"})
    return tootResponse
