import requests
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ThinkificClient:
    """Client for interacting with the Thinkific API using Bearer token authentication."""
    
    BASE_URL = "https://api.thinkific.com/api/public/v1"
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize the Thinkific client.
        
        Args:
            access_token: Your Thinkific access token. If not provided, will try to get from THINKIFIC_ACCESS_TOKEN env var.
        """
        self.access_token = access_token or os.getenv('THINKIFIC_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Access token is required. Provide it directly or set THINKIFIC_ACCESS_TOKEN environment variable.")
    
    def _get_headers(self) -> Dict:
        """Get the headers required for API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_courses(self) -> List[Dict]:
        """
        Get all courses from the Thinkific site.
        
        Returns:
            List of course dictionaries
        """
        response = requests.get(
            f"{self.BASE_URL}/courses",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()['items']
    
    def get_course_chapters(self, course_id: int) -> List[Dict]:
        """
        Get all lessons for a specific course.
        
        Args:
            course_id: The ID of the course
            
        Returns:
            List of lesson dictionaries
        """
        response = requests.get(
            f"{self.BASE_URL}/courses/{course_id}/chapters",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()['items']
    
    def get_contents(self, content_id: int) -> Dict:
        """
        Get detailed information about a specific content.
        
        Args:
            content_id: The ID of the contents
            
        Returns:
            Dictionary containing lesson details
        """
        response = requests.get(
            f"{self.BASE_URL}/contents/{content_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_users(self) -> List[Dict]:
        """
        Get all users from the Thinkific site.
        
        Returns:
            List of user dictionaries
        """
        response = requests.get(
            f"{self.BASE_URL}/users",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()['items']

    def get_site_scripts(self) -> List[Dict]:
        """
        Get all site scripts from the Thinkific site.
        
        Returns:
            List of site script dictionaries
        """
        response = requests.get(
            f"{self.BASE_URL}/site_scripts?page=1&limit=25",
            headers=self._get_headers() 
        )
        response.raise_for_status()
        return response.json()['items']


if __name__ == "__main__":
    client = ThinkificClient()
    courses = client.get_courses()
    course_id = courses[0]['id']
    chapters = client.get_course_chapters(course_id)
    for chapter in chapters:
        print(chapter['name'])
        for content_id in chapter['content_ids']:
            cont = client.get_contents(content_id)
            print(cont)

        
