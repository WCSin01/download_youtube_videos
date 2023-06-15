# -*- coding: utf-8 -*-

# Sample Python code for youtube.captions.download
# NOTE: This sample code downloads a file and can't be executed via this
#       interface. To test this sample, you must run it locally using your
#       own API credentials.

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import io
import os
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaIoBaseDownload

from dotenv import load_dotenv

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    load_dotenv()

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        os.getenv("GOOGLE_O_AUTH_SECRET"), scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # list = youtube.captions().list(part="id,snippet", videoId="kiSYRbMn67I").execute()
    #
    # for object in list.get("items"):
    #     print(object)
    # sys.exit()

    request = youtube.captions().download(
        id="NDlCRH48cS9w932VhyMUoc-bI89tcLfr"
    )
    # TODO: For this request to work, you must replace "YOUR_FILE"
    #       with the location where the downloaded content should be written.
    fh = io.FileIO("C:/Users/sinwe/Downloads/captions.txt", "wb")

    download = MediaIoBaseDownload(fh, request)
    complete = False
    while not complete:
        status, complete = download.next_chunk()


if __name__ == "__main__":
    main()
