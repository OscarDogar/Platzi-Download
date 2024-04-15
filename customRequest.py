import requests
from utils import get_random_user_agent


def request_with_random_user_agent(url, max_retries=5):
    """
    Sends a GET request to the specified URL with a random User-Agent.

    Args:
        url (str): The URL to send the request to.
        max_retries (int, optional): The maximum number of retries in case of failure. Defaults to 5.

    Returns:
        requests.Response or None: The response object if the request was successful, None otherwise.
    """

    # Initialize retries counter
    retries = 0
    while retries < max_retries:
        # Generate a random User-Agent
        headers = {
            "Referer": "https://platzi.com/",
            "User-Agent": get_random_user_agent(),
        }
        try:
            # Make the request
            response = requests.get(url, headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                return response
            else:
                print(f"Failed! Status Code: {response.status_code}")
                retries += 1
        except Exception as e:
            print(f"Failed to connect: {e}")
            retries += 1
        # If we reached max retries, print a message
        if retries == max_retries:
            print("Max retries reached. Failed to get a successful response.")
            return None
