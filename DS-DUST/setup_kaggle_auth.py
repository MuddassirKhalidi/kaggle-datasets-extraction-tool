#!/usr/bin/env python3
"""
Kaggle API Authentication Setup Script
This script helps set up Kaggle API credentials for the data lake experiments.
"""

import os
import json
from pathlib import Path

def setup_kaggle_auth():
    """Set up Kaggle API authentication."""
    
    print("=" * 60)
    print("KAGGLE API AUTHENTICATION SETUP")
    print("=" * 60)
    
    # Check if credentials already exist
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        print(f"✅ Kaggle credentials already exist at: {kaggle_json}")
        print("You can proceed with running the test script.")
        return True
    
    print("\nTo use the Kaggle API, you need to set up your credentials:")
    print("\n1. Go to https://www.kaggle.com/account")
    print("2. Scroll down to the 'API' section")
    print("3. Click 'Create New API Token'")
    print("4. This will download a file called 'kaggle.json'")
    print("\n5. Move the downloaded 'kaggle.json' file to:")
    print(f"   {kaggle_dir}/")
    
    # Create the .kaggle directory if it doesn't exist
    kaggle_dir.mkdir(exist_ok=True)
    print(f"\n✅ Created directory: {kaggle_dir}")
    
    print("\n6. Set proper permissions:")
    print("   chmod 600 ~/.kaggle/kaggle.json")
    
    print("\n" + "=" * 60)
    print("MANUAL SETUP REQUIRED")
    print("=" * 60)
    print("\nAfter completing the steps above, you can:")
    print("1. Run: python test_kaggle_api.py")
    print("2. Or activate the virtual environment first:")
    print("   source venv/bin/activate")
    print("   python test_kaggle_api.py")
    
    return False

def verify_setup():
    """Verify that Kaggle API setup is complete."""
    
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    
    if not kaggle_json.exists():
        print("❌ Kaggle credentials not found!")
        return False
    
    try:
        with open(kaggle_json, 'r') as f:
            credentials = json.load(f)
        
        required_keys = ['username', 'key']
        if all(key in credentials for key in required_keys):
            print("✅ Kaggle credentials are properly configured!")
            print(f"   Username: {credentials['username']}")
            return True
        else:
            print("❌ Kaggle credentials file is missing required fields!")
            return False
            
    except json.JSONDecodeError:
        print("❌ Kaggle credentials file is not valid JSON!")
        return False
    except Exception as e:
        print(f"❌ Error reading Kaggle credentials: {e}")
        return False

if __name__ == "__main__":
    print("Checking Kaggle API setup...")
    
    if not verify_setup():
        setup_kaggle_auth()
    else:
        print("\n🎉 Ready to run Kaggle API tests!")
        print("Run: python test_kaggle_api.py")
