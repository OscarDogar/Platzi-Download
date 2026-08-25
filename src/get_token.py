"""
Utilities for fetching and caching Platzi authentication tokens for resource access.
"""

import asyncio
import time
import ssl
import certifi
import aiohttp
import config

TOKEN = None  # When the token is created, it is valid for 1 day
TOKEN_EXP = 0
LOCK = asyncio.Lock()

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


async def validate_token(session):
    """
    Validates and retrieves an authentication token, using caching to minimize API calls.

    This function implements a token validation strategy with the following
    features:
    - Returns a cached token if it's still valid (with a 30-second buffer
      before expiration)
    - Uses async locking to prevent race conditions when multiple coroutines
      request tokens simultaneously
    - Performs a double-check pattern after acquiring the lock to ensure
      thread safety
    - Fetches a new token from the Platzi API if the cached token is expired
      or missing

    Args:
        session: An aiohttp ClientSession object for making HTTP requests

    Returns:
        str: The valid access token from the Platzi API

    Raises:
        aiohttp.ClientError: If the HTTP request to fetch credentials fails
        KeyError: If the API response doesn't contain the expected token structure

    Note:
        Updates global variables TOKEN and TOKEN_EXP with the new token and its expiration time.
        The 30-second buffer ensures the token won't expire during use.
    """
    global TOKEN, TOKEN_EXP
    now = int(time.time())
    # Return cached token if still valid
    if TOKEN and now < TOKEN_EXP - 30:
        return TOKEN
    async with LOCK:
        # Double check after acquiring lock
        now = int(time.time())
        if TOKEN and now < TOKEN_EXP - 30:
            return TOKEN
        url = "https://platzi.com/api/v5/users/credentials/"
        async with session.get(url, ssl=SSL_CONTEXT) as res:
            data = await res.json()
            TOKEN = data["token"]["access"]
            TOKEN_EXP = data["token"]["exp"]
            return TOKEN


async def get_token():
    """
    Asynchronously retrieves and validates an authentication token.

    This function establishes an HTTP session with pre-configured cookies and headers,
    removes the Accept header to prevent 406 errors, validates the token, and returns
    the current valid access token.

    Returns:
        str: The valid Platzi access token.

    Raises:
        May raise exceptions from validate_token() if token validation fails.

    Notes:
        - Uses aiohttp.ClientSession for async HTTP operations
        - Modifies a copy of config.headers to avoid side effects
        - Requires config.COOKIES and config.headers to be properly configured
    """
    headers = config.headers.copy()
    # remove accept header to avoid getting a 406 error
    headers.pop("Accept", None)
    connector = aiohttp.TCPConnector(ssl=SSL_CONTEXT)
    async with aiohttp.ClientSession(
        cookies=config.COOKIES, headers=headers, connector=connector
    ) as session:
        return await validate_token(session)


asyncio.run(get_token())
