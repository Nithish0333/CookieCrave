import requests
import json

def test_sms():
    url = "https://www.fast2sms.com/dev/bulkV2"
    api_key = "JrhlMkeC4yXRijqSBZOsf2xznNwp98L0gKVo7cmdQtGAHuYETaJoLlAntuEaXD4ZiqmH0bGcFO9Vw5TS"
    
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json",
    }
    
    # Try the 'q' route (Quick SMS) which often doesn't require website verification
    payload_q = {
        "route": "q",
        "message": "Your CookieCrave OTP is 1234. Use this to verify your account.",
        "language": "english",
        "numbers": "7639207156",
    }
    
    print(f"\nTesting Fast2SMS 'q' route...")
    try:
        response_q = requests.post(url, json=payload_q, headers=headers)
        print(f"Status Code: {response_q.status_code}")
        print(f"Response: {response_q.text}")
    except Exception as e:
        print(f"Error: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_sms()
