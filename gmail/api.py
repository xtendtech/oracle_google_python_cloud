import os
from googleapiclient.discovery import build

yt_api_key= os.environ.get("GOOGLE_API")
print(yt_api_key)
youtube_client=build("youtube","v3",developerKey=yt_api_key)
print(youtube_client)
pl='UUCezIgC97PvUuR4_gbFUs5g'
# request=youtube_client.playlistItems().list(part="status", playlistId=pl
request=youtube_client.channels()
print(request.list(part="statistics", forUsername="Coreyms").execute())
# print(request.__doc__)


# resp=request.execute()
# for req in resp['items']:
#     print(req['id'])