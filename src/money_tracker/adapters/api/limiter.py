from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize Limiter
# key_func: How to identify the client (IP address)
# default_limits: Global limit applied to all endpoints (unless overridden)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
