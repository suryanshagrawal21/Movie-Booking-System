
import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from utils.email_helper import EmailHelper
from utils.config_manager import ConfigManager

def test_gmail_flow():
    print("📧 Gmail Connectivity Test")
    print("-" * 30)
    
    config = ConfigManager.load_config()
    
    email_user = input("Enter your Gmail address: ")
    email_pass = input("Enter your Gmail App Password (NOT your regular password): ")
    recipient = input("Enter recipient email for test: ")
    
    # Save to config for future use (optional, but convenient for testing)
    config["email_user"] = email_user
    config["email_password"] = email_pass
    ConfigManager.save_config(config)
    
    print("\nSending test email...")
    success, message = EmailHelper.send_email(
        to_email=recipient,
        subject="Movie Booking System - Gmail Test",
        body="This is a test email from your Movie Booking System project. Gmail integration is working!"
    )
    
    if success:
        print("✅ SUCCESS: Test email sent.")
    else:
        print(f"❌ FAILED: {message}")
        print("\nNote: Ensure you are using a Gmail 'App Password'.")
        print("Guide: https://support.google.com/accounts/answer/185833")

if __name__ == "__main__":
    test_gmail_flow()
