from fastapi import APIRouter
import requests

router = APIRouter()

API_KEY ="c1a2c42facmsh2e1b56ed7463ce2p137ad2jsn5b768e01b3b8"

@router.get("/jobs")
def jobs():
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": "python developer remote",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
