#!/usr/bin/env python3

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import config

def get_context():
    # Get sharepoint credentials
    sharepoint_url = 'https://codeacademylt.sharepoint.com/sites/PHPmokymaiPHPU1'

    # Initialize the client credentials
    user_credentials = UserCredential(config.username, config.password)

    # create client context object
    ctx = ClientContext(sharepoint_url).with_credentials(user_credentials)
    web = ctx.web.get().execute_query()

    return web

def main():
    print(f"{get_context().properties['Title']}")

if __name__ == "__main__":
    main()
