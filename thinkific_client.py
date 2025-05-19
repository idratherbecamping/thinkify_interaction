import requests
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup

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

    def get_full_course_via_graphql(self, course_id: int, chapters_first: int = 30, lessons_first: int = 30, chapters_after: Optional[str] = None, lessons_after: Optional[str] = None) -> Dict:
        """
        Get a full course from the Thinkific site using GraphQL.
        
        Args:
            course_id: The ID of the course
        
            Returns:
                Dictionary containing course details
            """

        # Your variables
        variables = {
            "courseId": course_id,
            "chaptersFirst": chapters_first,
            "chaptersAfter": chapters_after,
            "lessonsFirst": lessons_first,
            "lessonsAfter": lessons_after
        }
        # Endpoint from your Apollo GraphQL server
        url = 'https://api.thinkific.com/stable/graphql'
        YOUR_API_TOKEN = self.access_token

        # Replace this with your actual token if authentication is required
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {YOUR_API_TOKEN}'  # optional
        }

        # Your GraphQL query as a string
        query = '''
        query Example_CourseCurriculumQuery(
        $courseId: ID!
        $chaptersFirst: Int
        $chaptersAfter: String
        $lessonsFirst: Int
        $lessonsAfter: String
        ) {
        course(id: $courseId) {
            curriculum {
            chaptersCount
            lessonsCount
            totalVideoContentTime
            chapters(first: $chaptersFirst, after: $chaptersAfter) {
                nodes {
                id
                position
                title
                lessons(first: $lessonsFirst, after: $lessonsAfter) {
                    pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    }
                    nodes {
                    content {
                        id
                        contentType
                        ... on AssignmentContent {
                        confirmationMessage
                        createdAt
                        fileSizeLimit
                        contentType
                        updatedAt
                        }
                        ... on AudioContent {
                        createdAt
                        htmlDescription
                        id
                        contentType
                        updatedAt
                        url
                        }
                        ... on DownloadContent {
                        createdAt
                        htmlDescription
                        id
                        contentType
                        updatedAt
                        }
                        ... on ExamContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on LiveContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on MultimediaContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on PdfContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        url
                        }
                        ... on PresentationContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on QuizContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on SurveyContent {
                        createdAt
                        id
                        contentType
                        updatedAt
                        }
                        ... on TextContent {
                        createdAt
                        htmlDescription
                        id
                        contentType
                        updatedAt
                        }
                        ... on VideoContent {
                        createdAt
                        fileName
                        fileSize
                        fileType
                        htmlDescription
                        id
                        contentType
                        updatedAt
                        videoId
                        thumbnail
                        }
                    }
                    id
                    title
                    lessonType
                    takeUrl
                    }
                }
                }
                pageInfo {
                endCursor
                hasNextPage
                hasPreviousPage
                startCursor
                }
            }
            }
            description
            id
            cardImage {
            url
            }
            instructor {
            fullName
            id
            bio
            email
            }
            name
            slug
            title
        }
        }
        '''

        # Make the request
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        return response.json()

    def process_course_data(self, course_data: Dict) -> Dict:
        """
        Process and clean the course data from GraphQL response into a more readable format.
        
        Args:
            course_data: The raw course data from get_full_course_via_graphql
            
        Returns:
            Dictionary containing cleaned course data
        """
        def clean_html(html_content: str) -> str:
            """Remove HTML tags and clean up whitespace."""
            if not html_content:
                return ""
            # Use BeautifulSoup to parse and get text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        def process_lesson(lesson: Dict) -> Dict:
            """Process a single lesson and its content."""
            content = lesson.get('content', {})
            return {
                'id': lesson.get('id'),
                'title': lesson.get('title'),
                'type': lesson.get('lessonType'),
                'take_url': lesson.get('takeUrl'),
                'content': {
                    'id': content.get('id'),
                    'type': content.get('contentType'),
                    'created_at': content.get('createdAt'),
                    'updated_at': content.get('updatedAt'),
                    'description': clean_html(content.get('htmlDescription', '')),
                    'url': content.get('url')
                }
            }

        def process_chapter(chapter: Dict) -> Dict:
            """Process a single chapter and its lessons."""
            return {
                'id': chapter.get('id'),
                'position': chapter.get('position'),
                'title': chapter.get('title'),
                'lessons': [process_lesson(lesson) for lesson in chapter.get('lessons', {}).get('nodes', [])]
            }

        # Extract the course data
        course = course_data.get('data', {}).get('course', {})
        curriculum = course.get('curriculum', {})
        
        # Build the processed data structure
        processed_data = {
            'course_info': {
                'id': course.get('id'),
                'name': course.get('name'),
                'title': course.get('title'),
                'slug': course.get('slug'),
                'description': course.get('description'),
                'card_image': course.get('cardImage', {}).get('url'),
                'instructor': {
                    'id': course.get('instructor', {}).get('id'),
                    'name': course.get('instructor', {}).get('fullName'),
                    'email': course.get('instructor', {}).get('email'),
                    'bio': course.get('instructor', {}).get('bio')
                }
            },
            'curriculum': {
                'chapters_count': curriculum.get('chaptersCount'),
                'lessons_count': curriculum.get('lessonsCount'),
                'total_video_time': curriculum.get('totalVideoContentTime'),
                'chapters': [process_chapter(chapter) for chapter in curriculum.get('chapters', {}).get('nodes', [])]
            }
        }
        
        return processed_data

if __name__ == "__main__":
    client = ThinkificClient()
    course = client.get_full_course_via_graphql(3090216)
    processed_course = client.process_course_data(course)

    
    # courses = client.get_courses()
    # course_id = courses[0]['id']
    # chapters = client.get_course_chapters(course_id)
    # for chapter in chapters:
    #     print(chapter['name'])
    #     for content_id in chapter['content_ids']:
    #         cont = client.get_contents(content_id)
    #         print(cont)

        
