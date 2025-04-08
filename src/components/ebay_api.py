import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

class EbayAPI:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("EBAY_CLIENT_ID")
        self.client_secret = os.getenv("EBAY_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ValueError("EBAY_CLIENT_ID and EBAY_CLIENT_SECRET must be set in .env file")
        self.auth_url = "https://api.ebay.com/identity/v1/oauth2/token"
        self.search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self._access_token = None

    def _get_access_token(self) -> str:
        """Get or refresh the access token."""
        if self._access_token:
            return self._access_token

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }

        try:
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=data,
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
            return self._access_token
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def search_items(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for items on eBay.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of items to return
            
        Returns:
            List[Dict[str, Any]]: List of items found
        """
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        }
        params = {
            "q": query,
            "limit": limit
        }

        try:
            response = requests.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("itemSummaries", [])
        except Exception as e:
            raise Exception(f"Failed to search items: {str(e)}")

    def format_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format an item for display."""
        return {
            "title": item.get("title", "No title"),
            "price": item.get("price", {}).get("value", "N/A"),
            "image": item.get("image", {}).get("imageUrl", "assets/images/placeholder.png"),
            "condition": item.get("condition", "Unknown"),
            "seller": item.get("seller", {}).get("username", "Unknown"),
            "url": item.get("itemWebUrl", "#")
        } 