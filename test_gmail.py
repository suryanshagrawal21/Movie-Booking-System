
import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from utils.email_helper import EmailHelper
from utils.config_manager import ConfigManager

def test_gmail_flow():
    print("📧 Gmail Connectivity Test with Attachments")
    print("-" * 30)
    
    config = ConfigManager.load_config()
    
    email_user = input("Enter your Gmail address: ")
    email_pass = input("Enter your Gmail App Password: ")
    recipient = input("Enter recipient email for test: ")
    
    # Save to config for future use
    config["email_user"] = email_user
    config["email_password"] = email_pass
    ConfigManager.save_config(config)
    
    # Create a dummy file for attachment test
    dummy_file = "test_attachment.txt"
    with open(dummy_file, "w") as f:
        f.write("This is a test attachment for the Movie Booking System.")
        
    print("\nSending test email with attachment...")
    success, message = EmailHelper.send_email(
        to_email=recipient,
        subject="Movie Booking System - Attachment Test",
        body="This is a test email with an attachment from your Movie Booking System project.",
        attachment_path=dummy_file
    )
    
    if success:
        print("✅ SUCCESS: Test email with attachment sent.")
    else:
        print(f"❌ FAILED: {message}")
    
    # Cleanup
    if os.path.exists(dummy_file):
        os.remove(dummy_file)

if __name__ == "__main__":
    test_gmail_flow()
