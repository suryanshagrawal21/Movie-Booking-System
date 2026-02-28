import requests
import os
from ..utils.config_manager import ConfigManager

class TMDBService:
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.api_key = self.config.get("tmdb_api_key", "YOUR_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def get_now_playing(self):
        """Fetch now playing movies from TMDB"""
        if self.api_key == "YOUR_KEY":
            print("WARNING: TMDB API Key not set.")
            return []
            
        url = f"{self.base_url}/movie/now_playing?api_key={self.api_key}&language=en-US&page=1"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            print(f"TMDB API Error: {response.status_code}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"TMDB Request Failed: {e}")
            return []

    def get_popular(self):
        """Fetch popular movies from TMDB"""
        if self.api_key == "YOUR_KEY":
            return []
            
        url = f"{self.base_url}/movie/popular?api_key={self.api_key}&language=en-US&page=1"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            return []
        except requests.exceptions.RequestException:
            return []

    def get_poster_url(self, poster_path, size="w500"):
        """Convert poster path to full image URL"""
        if not poster_path:
            return None
        return f"https://image.tmdb.org/t/p/{size}{poster_path}"

    def download_poster(self, poster_path, save_dir="src/assets/posters"):
        """Downloads and caches a poster image locally."""
        if not poster_path:
            return None
            
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        filename = poster_path.lstrip("/")
        filepath = os.path.join(save_dir, filename)
        
        if os.path.exists(filepath):
            return filepath # Already cached
            
        url = self.get_poster_url(poster_path)
        if not url:
            return None
            
        try:
            response = requests.get(url, stream=True, timeout=5)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filepath
        except Exception as e:
            print(f"Error downloading poster: {e}")
        return None

# Global instance
tmdb_service = TMDBService()
