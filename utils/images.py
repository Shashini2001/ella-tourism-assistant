import os
import requests
import streamlit as st

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24) 
def fetch_image_url(query: str, api_key: str | None = None) -> dict | None:
    
    key = api_key or os.environ.get("PEXELS_API_KEY")
    if not key:
        return None

    try:
        response = requests.get(
            PEXELS_SEARCH_URL,
            headers={"Authorization": key},
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])
        if not photos:
            return None

        photo = photos[0]
        return {
            "url": photo["src"]["medium"],
            "photographer": photo.get("photographer", "Unknown"),
            "pexels_url": photo.get("url", "https://www.pexels.com"),
        }
    except (requests.RequestException, KeyError, ValueError):
        return None
