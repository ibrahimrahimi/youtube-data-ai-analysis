from googleapiclient.discovery import build
import pandas as pd

# Initialize YouTube API
API_KEY = ""  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Fetch channel stats
def get_channel_stats(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    return response

# Fetch videos from a playlist (uploads)
def get_videos_from_playlist(playlist_id):
    videos = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        videos += response['items']
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return videos

# Fetch video statistics
def get_video_stats(video_ids):
    stats = []
    for video_id in video_ids:
        request = youtube.videos().list(
            part="statistics,snippet",
            id=video_id
        )
        response = request.execute()
        stats += response['items']
    return stats

# Example Usage
channel_id = "YOUR_CHANNEL_ID"  # Replace with your channel ID
channel_data = get_channel_stats(channel_id)

playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
videos = get_videos_from_playlist(playlist_id)

video_ids = [video['snippet']['resourceId']['videoId'] for video in videos]
video_stats = get_video_stats(video_ids)

# Save to DataFrame
video_data = []
for video in video_stats:
    video_data.append({
        "Video ID": video['id'],
        "Title": video['snippet']['title'],
        "Views": int(video['statistics'].get('viewCount', 0)),
        "Likes": int(video['statistics'].get('likeCount', 0)),
        "Comments": int(video['statistics'].get('commentCount', 0))
    })

df = pd.DataFrame(video_data)
df.to_csv('youtube_data.csv', index=False)
print("Data saved to youtube_data.csv")
