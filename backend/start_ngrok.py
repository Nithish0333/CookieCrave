from pyngrok import ngrok
import time
import sys

def start_tunnel():
    # Set the authtoken provided by user
    ngrok.set_auth_token("3AyYDALzETeAUvdWtnV0HGHxEZb_44S5LygcZtasgyd3XA46K")
    
    print("Starting ngrok tunnel for Backend...")
    try:
        # Backend tunnel (Port 8000)
        backend_url = ngrok.connect(8000).public_url
        print(f"Backend Ngrok URL (Use for Fast2SMS): {backend_url}")
        
        # Save to file for easy retrieval
        with open("ngrok_urls.txt", "w") as f:
            f.write(f"BACKEND_URL={backend_url}\n")
        
        print("\n--- Keep this script running to maintain the tunnel ---")
        
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        with open("ngrok_error.txt", "w") as f:
            f.write(str(e))
        sys.exit(1)

if __name__ == "__main__":
    start_tunnel()
