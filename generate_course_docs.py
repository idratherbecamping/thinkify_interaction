from thinkific_client import ThinkificClient
from datetime import datetime

def generate_course_docs():
    client = ThinkificClient()
    
    # Get all courses
    courses = client.get_courses()
    
    # Create markdown content
    markdown_content = f"""# Thinkific Courses
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    # Add each course and its chapters
    for course in courses:
        markdown_content += f"""## {course['name']}

"""
        
        # Get chapters for this course
        chapters = client.get_course_chapters(course['id'])
        
        if not chapters:
            markdown_content += "*No content available*\n\n"
        else:
            for chapter in chapters:
                markdown_content += f"""### {chapter['name']}

"""
                # Get content for each content ID in the chapter
                for content_id in chapter['content_ids']:
                    content = client.get_contents(content_id)
                    markdown_content += f"""#### {content['name']}

{content.get('description', '')}

"""
        
        markdown_content += "---\n\n"
    
    # Write to file
    with open('thinkific_courses.md', 'w') as f:
        f.write(markdown_content)
    
    print(f"Documentation generated successfully in 'thinkific_courses.md'")

if __name__ == "__main__":
    generate_course_docs() 