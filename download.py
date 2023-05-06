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

def list_files(url):
    folders, files = ([] for i in range(2))
    doc_lib = get_context(url).web.lists.get_by_title("Documents")
    items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get().execute_query()
    for item in items:
        if item.file_system_object_type == 1:
            folders.append(item.folder.serverRelativeUrl)
        else:
            files.append(item.file.serverRelativeUrl)
    return folders,files

def get_files(url):
    conn = get_context(url)
    relative_url = f"{get_query(url).properties['ServerRelativeUrl']}/Shared Documents/General/admin.jpg"
    print(f"{relative_url}")
    file = conn.web.get_file_by_server_relative_url(relative_url).execute_query()
    return file

def main():
    url = f'https://{config.domain}.sharepoint.com/sites/{config.site}'
    #print(f"ClientContext query (title): {get_query(url).properties['Title']}")
    #print(f"RequestOptions query (title): {get_data(url)['d']['Title']}")
    #print(f"{get_query(url).properties}")
    #print(get_files(url).name)
    print(f"Folders: {list_files(url)[0]}, Files: {list_files(url)[1]}")

if __name__ == "__main__":
    main()
