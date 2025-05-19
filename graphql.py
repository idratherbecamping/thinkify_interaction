import os
from typing import Optional, Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

class ThinkificGraphQLClient:
    def __init__(self):
        self.api_key = os.getenv("THINKIFIC_ACCESS_TOKEN")
        self.domain = os.getenv("thinkific_site_subdomain")
        if not self.api_key or not self.domain:
            raise ValueError("THINKIFIC_API_KEY and THINKIFIC_DOMAIN must be set in .env file")
        
        self.base_url = f"https://{self.domain}/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def execute_query(
        self,
        course_id: str,
        chapters_first: Optional[int] = None,
        chapters_after: Optional[str] = None,
        lessons_first: Optional[int] = None,
        lessons_after: Optional[str] = None
    ) -> Dict[str, Any]:
        query = """
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
        """

        variables = {
            "courseId": course_id,
            "chaptersFirst": chapters_first,
            "chaptersAfter": chapters_after,
            "lessonsFirst": lessons_first,
            "lessonsAfter": lessons_after
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

# Example usage:
async def main():
    client = ThinkificGraphQLClient()
    try:
        result = await client.execute_query(
            course_id="3095634",
            chapters_first=10,
            lessons_first=10
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
