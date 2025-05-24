import schedule
import time
import subprocess
import os
from datetime import datetime

def run_flight_check():
    """Run the complete flight check and send results"""
    print(f"\n=== Running flight check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    try:
        # Run the extraction script
        result = subprocess.run(
            ["python", "extract_points.py"], 
            capture_output=True, 
            text=True,
            cwd="/Users/sahil/reward-seat-tracker"
        )
        
        if result.returncode == 0:
            print("✓ Flight data extracted successfully")
            
            # Send iMessage with results
            result = subprocess.run(
                ["python", "send_imessage.py", "4129616513"],
                capture_output=True,
                text=True,
                cwd="/Users/sahil/reward-seat-tracker"
            )
            
            if result.returncode == 0:
                print("✓ iMessage sent successfully")
            else:
                print(f"✗ iMessage failed: {result.stderr}")
                
        else:
            print(f"✗ Flight extraction failed: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Error during flight check: {e}")

def main():
    """Schedule flight checks twice daily"""
    print("Starting reward seat tracker scheduler...")
    print("Scheduled checks: 9:00 AM and 8:00 PM daily")
    print("Press Ctrl+C to stop")
    
    # Schedule the checks
    schedule.every().day.at("09:00").do(run_flight_check)
    schedule.every().day.at("20:00").do(run_flight_check)
    
    # Show next run times
    print(f"\nNext runs:")
    for job in schedule.jobs:
        print(f"  {job.next_run}")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")

if __name__ == "__main__":
    main()