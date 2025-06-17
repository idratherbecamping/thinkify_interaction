from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict
import uuid

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read the inclusive classroom content
with open("example_content/navigating_spd_webinar_formatted.md", "r") as file:
    SYSTEM_CONTENT = file.read()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Dependency to manage conversation history
class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}

    def get_or_create_conversation(self, conversation_id: str = None) -> str:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            self.conversations[conversation_id] = [
                {"role": "system", "content": f"You are an AI assistant knowledgeable about Sensory Processing Disorder (SPD) and sensory integration strategies. \
                  Use the following course content to answer questions on how to understand, identify, and support individuals with sensory processing challenges. \
                  Your responses should draw from the material, including definitions, subtypes, behavioral signs, intervention strategies, and researchbacked recommendations.\
                  Content: {SYSTEM_CONTENT} Keep your responses concise and to the point. Use bullets and lists when appropriate. Use markdown formatting."}
            ]


    
        elif conversation_id not in self.conversations:
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        return conversation_id

    def add_message(self, conversation_id: str, role: str, content: str):
        self.conversations[conversation_id].append({"role": role, "content": content})

    def get_messages(self, conversation_id: str) -> List[Dict]:
        return self.conversations[conversation_id]

# Create a single instance of ConversationManager
conversation_manager = ConversationManager()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create conversation
        conversation_id = conversation_manager.get_or_create_conversation(request.conversation_id)
        
        # Add user message to conversation history
        conversation_manager.add_message(conversation_id, "user", request.message)

        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=conversation_manager.get_messages(conversation_id),
            # max_tokens=500
        )
        
        # Add assistant response to conversation history
        assistant_response = response.choices[0].message.content
        conversation_manager.add_message(conversation_id, "assistant", assistant_response)
        
        return ChatResponse(response=assistant_response, conversation_id=conversation_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port) 