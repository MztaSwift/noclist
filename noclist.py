#!python3

import hashlib
import json
import requests

# Function to handle server retries when there is a failover
def retry(url, max_tries=3, **kwargs):
    n_tries = 0
    # Loop the total number of tries
    while n_tries < max_tries:
        # Increase the initialized try value after each iteration
        n_tries += 1
        try:
            # perform the failed function again
            response = requests.get(url, **kwargs)
        except requests.exceptions.ConnectionError:
            # If error occurs, run the loop again
            continue
        if response.status_code == requests.codes.ok:
            # If the request goes through, return the response
            return response
    raise requests.exceptions.HTTPError


def get_auth_token(url):
    ''' 
        Authentication function for the url.  
        Returns a token that is appended to a request being made
    '''
    try:
        # Always wrap the request around the retry function so it handles the number of times a 
        # request is retried before finally giving up
        response = retry(url + "/auth")
    except requests.exceptions.HTTPError:
        return 1
    # Get the token from the response headers
    token = response.headers["Badsec-Authentication-Token"]
    # return the token
    return token

# 
def get_auth_checksum(token):
    ''' 
        Checksum function for the token.  
        Returns a checksum
    '''
    encoded = (token + "/users").encode("utf-8")

    # There is an encoding done and saved as checksum. 
    checksum = hashlib.sha256(encoded).hexdigest()
    return checksum


def get_user_ids(url, checksum):
    ''' 
        A function to get user IDs, with the checksum being a combination of encoded token and string (users)  
        Returns a content from the response
    '''
    # make a request, wrapped in the retry function
    response = retry(url + "/users", headers={"X-Request-Checksum": checksum})
    return response.content.decode()

# This function returns actual users
def get_badsec_users(url="http://127.0.0.1:8888"):
    token = get_auth_token(url=url)
    checksum = get_auth_checksum(token=token)
    users = get_user_ids(url=url, checksum=checksum)
    print(json.dumps(users.splitlines()))
    exit(0)

# The driver function for the entire application
if __name__ == '__main__':
    get_badsec_users()