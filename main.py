import requests
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from atproto import Client, client_utils


app = FastAPI()


class StatusRequest(BaseModel):
    mastodon_base_url: str
    mastodon_token: str
    bsky_username: str
    bsky_password: str
    content: str


@app.post("/skeet")
def new_skeet(status_request: StatusRequest):
    response = requests.post(f"https://{status_request.mastodon_base_url}/api/v1/statuses", data={
                             'status': status_request.content}, headers={"Authorization": f"Bearer {status_request.mastodon_token}"})
    client = Client()
    profile = client.login(status_request.bsky_username,
                           status_request.bsky_password)
    post = client.send_post(status_request.content)
    return "cool"
