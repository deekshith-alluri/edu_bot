import os
from googleapiclient.discovery import build
from config import _YOUTUBE_API_KEY

# Initialize YouTube client using your API key from environment
YOUTUBE_API_KEY = _YOUTUBE_API_KEY

if not YOUTUBE_API_KEY:
    raise ValueError("Please set the YOUTUBE_API_KEY environment variable.")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def recommend_videos(query: str, age: int = None, clazz: str = None, max_results: int = 5) -> list:
    """
    Recommends YouTube videos for a query and student age/class.
    Returns a list of dicts: [{"title": "...", "channel": "...", "url": "..."}, ...]
    """
    # Add context about age/class to the search query
    search_query = query
    if age and clazz:
        search_query += f" for {clazz} class, age {age}"

    try:
        request = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            maxResults=max_results,
            order="relevance"
        )

        response = request.execute()

        recommendations = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            recommendations.append({
                "title": title,
                "channel": channel,
                "url": video_url
            })

        return recommendations

    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return []


# -------- Example Usage --------
if __name__ == "__main__":
    sample_query = "Progressions"
    videos = recommend_videos(sample_query, age=15, clazz="10th grade")
    print("\n--- YouTube Recommendations ---")
    for v in videos:
        print(v)    