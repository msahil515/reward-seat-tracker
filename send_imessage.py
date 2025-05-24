import subprocess
import sys

def send_via_imessage(phone_number, message):
    """Send SMS via iMessage (macOS only) - completely free"""
    try:
        script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{phone_number}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''
        
        subprocess.run(["osascript", "-e", script], check=True)
        print(f"iMessage sent to {phone_number}")
        return True
        
    except Exception as e:
        print(f"iMessage failed: {e}")
        return False

if __name__ == "__main__":
    # Read results
    try:
        with open("extracted_points.txt", "r") as f:
            results = f.read().strip()
        
        # Get phone number from command line or prompt
        if len(sys.argv) > 1:
            phone = sys.argv[1]
        else:
            phone = input("Enter your phone number or email: ")
        
        message = f"Virgin Atlantic LHR→BLR: {results}"
        send_via_imessage(phone, message)
        
    except FileNotFoundError:
        print("No results found. Run extract_points.py first.")
    except KeyboardInterrupt:
        print("\nCancelled")