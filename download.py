#!/usr/bin/env python3

import json
import config
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext

def get_context(url):
    # Initialize the client credentials
    user_credentials = UserCredential(config.username, config.password)

    # create client context object
    ctx = ClientContext(url).with_credentials(user_credentials)

    return ctx

def get_query(url):
    """Query API using ClientContext class (recommended)"""
    web = get_context(url).web.get().execute_query()

    return web

def get_data(url):
    """Query API using RequestOptions class"""
    request = RequestOptions(f"{url}/_api/web/")
    response = get_context(url).pending_request().execute_request_direct(request)
    data = json.loads(response.content)

    return data

def get_files(url):
    pass

def main():
    url = f'https://{config.domain}.sharepoint.com/sites/{config.site}'
    print(f"ClientContext query (title): {get_query(url).properties['Title']}")
    print(f"RequestOptions query (title): {get_data(url)['d']['Title']}")

if __name__ == "__main__":
    main()
