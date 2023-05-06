#!/usr/bin/env python3

import os
import json
import config
import tempfile
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
    files = list_files(url)[1]
    for filename in files:
        download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(filename))
        with open(download_path, 'wb') as local_file:
            file = get_context(url).web.get_file_by_server_relative_url(filename).execute_query()
    print(f"{filename} file has been downloaded into: {download_path}")

def main():
    url = f'https://{config.domain}.sharepoint.com/sites/{config.site}'
    #print(f"ClientContext query (title): {get_query(url).properties['Title']}")
    #print(f"RequestOptions query (title): {get_data(url)['d']['Title']}")
    #print(f"{get_query(url).properties}")
    #print(get_files(url).name)
    #print(f"Folders: {list_files(url)[0]}, Files: {list_files(url)[1]}")
    get_files(url)

if __name__ == "__main__":
    main()
