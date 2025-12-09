from typing import Dict, Any
from google.oauth2 import id_token
from google.auth.transport import requests
from money_tracker.application.ports.security import IdentityProvider
from money_tracker.core.config import get_settings

settings = get_settings()

class GoogleIdentityProvider(IdentityProvider):
    async def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            return {
                "email": id_info["email"],
                "full_name": id_info.get("name"),
                "picture": id_info.get("picture"),
                "is_verified": id_info.get("email_verified", False)
            }
        except ValueError as e:
            # Invalid token
            raise ValueError(f"Invalid Google Token: {str(e)}")
