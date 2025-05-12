import requests
import json

def test_chat_api():
    # API endpoint
    # url = "http://localhost:8000/chat"
    url = "https://968d-68-5-165-122.ngrok-free.app/chat"
    # Test message
    test_message = "Tell me a joke about programming"
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request body
    data = {
        "message": test_message
    }
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Check if request was successful
        if response.status_code == 200:
            print("✅ API Test Successful!")
            print(f"Request Message: {test_message}")
            print(f"Response: {response.json()['response']}")
        else:
            print(f"❌ API Test Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to API: {e}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

if __name__ == "__main__":
    test_chat_api() 