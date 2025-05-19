import requests
import json
from dotenv import load_dotenv

load_dotenv()
import os

# Endpoint from your Apollo GraphQL server
url = 'https://api.thinkific.com/stable/graphql'
YOUR_API_TOKEN = os.getenv('THINKIFIC_ACCESS_TOKEN')

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

# Your variables
variables = {
    "courseId": "3095634",
    "chaptersFirst": 10,
    "chaptersAfter": None,
    "lessonsFirst": 10,
    "lessonsAfter": None
}

# Make the request
response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

# Print the JSON response
print(json.dumps(response.json(), indent=2))
