from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class UploadService:
    def __init__(self, client_secrets_file: str = "./client_secrets.json", scopes: list = ['https://www.googleapis.com/auth/youtube.upload']):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = None
        self.authenticate()

    def authenticate(self):
        """Performs OAuth authentication and builds the YouTube service."""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
            credentials = flow.run_local_server(port=0)
            self.youtube = build("youtube", "v3", credentials=credentials)
        except Exception as e:
            print(f"Authentication error: {e}")
            raise

    def upload_video(self, video_path: str, title: str, description: str, category_id: str = "10", privacy_status: str = "public") -> str:
        """Uploads the video to YouTube and returns the video URL."""
        try:
            body = {
                "snippet": {
                    "title": title,
                    "categoryId": category_id,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            print(f"\nStarting upload for: {title}")
            request = self.youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            response = request.execute()

            video_id = response.get('id')
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print("\n" + "="*15 + "VIDEO INFO" + "="*15)
            print(f"Title: {title}")
            print(f"Link: {video_url}")
            print(f"Description: {description}")
            print("="*40 + "\n")

            return video_url

        except Exception as e:
            print(f"\n[ERROR] The upload failed: {e}")
            raise
