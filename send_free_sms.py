import subprocess
import os
from datetime import datetime

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

def send_via_carrier_gateway(phone_number, message):
    """Send SMS via carrier email gateway - completely free"""
    carriers = {
        "1": ("Verizon", "vtext.com"),
        "2": ("AT&T", "txt.att.net"), 
        "3": ("T-Mobile", "tmomail.net"),
        "4": ("Sprint", "messaging.sprintpcs.com"),
        "5": ("US Cellular", "email.uscc.net"),
        "6": ("Metro PCS", "mymetropcs.com")
    }
    
    print("\nSelect your carrier:")
    for key, (name, domain) in carriers.items():
        print(f"{key}. {name}")
    
    choice = input("Enter choice (1-6): ")
    
    if choice in carriers:
        carrier_name, domain = carriers[choice]
        email_address = f"{phone_number}@{domain}"
        
        try:
            # Use built-in mail command
            subprocess.run([
                "mail", "-s", "Flight Alert", email_address
            ], input=message, text=True, check=True)
            
            print(f"SMS sent via {carrier_name} gateway")
            return True
            
        except Exception as e:
            print(f"Carrier gateway failed: {e}")
            return False
    else:
        print("Invalid choice")
        return False

def send_notification(message):
    """Send macOS desktop notification - completely free"""
    try:
        subprocess.run([
            "osascript", "-e", 
            f'display notification "{message}" with title "Flight Alert"'
        ], check=True)
        print("Desktop notification sent")
        return True
    except:
        return False

if __name__ == "__main__":
    # Read results
    try:
        with open("extracted_points.txt", "r") as f:
            results = f.read().strip()
        
        message = f"Virgin Atlantic LHR→BLR: {results}"
        
        print("Choose notification method:")
        print("1. iMessage (iPhone/Mac)")
        print("2. SMS via carrier (any phone)")
        print("3. Desktop notification only")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            phone = input("Enter phone number or email: ")
            send_via_imessage(phone, message)
            
        elif choice == "2":
            phone = input("Enter 10-digit phone number: ")
            send_via_carrier_gateway(phone, message)
            
        elif choice == "3":
            send_notification(message)
            
    except FileNotFoundError:
        print("No results found. Run extract_points.py first.")