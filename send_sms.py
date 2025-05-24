import os
from datetime import datetime

def send_sms_twilio(results_text, phone_number):
    """Send extracted flight points via SMS using Twilio"""
    try:
        from twilio.rest import Client
    except ImportError:
        print("Twilio not installed. Run: pip install twilio")
        return False
    
    # Twilio credentials from environment
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")  # Your Twilio phone number
    
    if not all([account_sid, auth_token, from_number]):
        print("Error: Missing Twilio credentials")
        print("Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
        return False
    
    # Create message
    message_body = f"Virgin Atlantic LHR→BLR Upper Class:\n{results_text}\n{datetime.now().strftime('%m/%d %H:%M')}"
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=phone_number
        )
        
        print(f"SMS sent successfully! Message SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def send_sms_simple(results_text, phone_number):
    """Simple SMS using system mail command (macOS/Linux)"""
    try:
        import subprocess
        
        # Format message
        message = f"Virgin Atlantic: {results_text}"
        
        # Use carrier email-to-SMS gateway
        carriers = {
            "verizon": "vtext.com",
            "att": "txt.att.net", 
            "tmobile": "tmomail.net",
            "sprint": "messaging.sprintpcs.com"
        }
        
        print("Available carriers:")
        for i, carrier in enumerate(carriers.keys(), 1):
            print(f"{i}. {carrier}")
        
        choice = input("Select carrier (1-4): ")
        carrier_names = list(carriers.keys())
        
        if choice.isdigit() and 1 <= int(choice) <= len(carrier_names):
            carrier = carrier_names[int(choice)-1]
            email_address = f"{phone_number}@{carriers[carrier]}"
            
            # Send via system mail
            subprocess.run([
                "mail", "-s", "Flight Alert", email_address
            ], input=message, text=True)
            
            print(f"SMS sent to {phone_number} via {carrier}")
            return True
        else:
            print("Invalid carrier selection")
            return False
            
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

if __name__ == "__main__":
    # Read extracted results
    try:
        with open("extracted_points.txt", "r") as f:
            results = f.read().strip()
        
        phone = input("Enter phone number (10 digits): ")
        
        # Try Twilio first, fallback to simple method
        if not send_sms_twilio(results, f"+1{phone}"):
            print("\nTrying alternative SMS method...")
            send_sms_simple(results, phone)
        
    except FileNotFoundError:
        print("No results file found. Run extract_points.py first.")