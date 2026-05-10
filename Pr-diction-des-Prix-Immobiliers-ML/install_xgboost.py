#!/usr/bin/env python
"""
Script to install XGBoost in the current environment
"""
import subprocess
import sys

def install_xgboost():
    try:
        print("Installing XGBoost...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])
        print("✅ XGBoost installed successfully!")
        
        # Verify installation
        import xgboost
        print(f"📦 XGBoost version: {xgboost.__version__}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing XGBoost: {e}")
        return False
    except ImportError as e:
        print(f"❌ Error importing XGBoost after installation: {e}")
        return False
    
    return True

if __name__ == "__main__":
    install_xgboost()
