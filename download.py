#!/usr/bin/env python3

import os
import re
import json
import config

from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

def get_context(url):
    """Login to sharepoint site using configured credentials"""
    creds = UserCredential(config.username, config.password) # Initialize client credentials
    ctx = ClientContext(url).with_credentials(creds) # create client context object

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
    """Get a list of folders and files in a sharepoint site"""
    folders, files = ([] for i in range(2))
    doc_lib = get_context(url).web.lists.get_by_title("Documents")
    items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get().execute_query()
    for item in items:
        if item.file_system_object_type == 1:
            folders.append(item.folder.serverRelativeUrl)
        else:
            files.append(item.file.serverRelativeUrl)

    return folders,files

def get_folders(url):
    folders = list_files(url)[0]
    for folder in folders:
        folder_name = re.split("/", folder)[-1]
        files = get_context(url).web.get_folder_by_server_relative_url(folder).files
        get_context(url).load(files).execute_query()
        for file in files:
            print(f"{file.name}")

def get_files(url):
    """Download files from a sharepoint site"""
    files = list_files(url)[1]
    for file in files:
        file_name = re.split("/", file)[-1]
        print(f"Downloading {filename}")
        with open(file_name, 'wb') as output:
            contents = File.open_binary(get_context(url), file)
            output.write(contents.content)

def examples(url):
    """Some usage examples"""
    #print(f"ClientContext query (title): {get_query(url).properties['Title']}")
    #print(f"RequestOptions query (title): {get_data(url)['d']['Title']}")
    #print(f"Query properties: {get_query(url).properties}")
    #print(f"Folders: {list_files(url)[0]}, Files: {list_files(url)[1]}")

def main():
    """Main program"""
    url = f'https://{config.domain}.sharepoint.com/sites/{config.site}'
    #examples(url)
    #get_folders(url)
    #list_files(url)
    get_files(url)

if __name__ == "__main__":
    main()
