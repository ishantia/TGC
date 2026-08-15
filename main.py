"""
💫 TGC – Telegram Group Checker 💫
Author: @ishantia
Main Entry Point.
"""
import sys
import os

# Ensure current working directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tgc.gui.app import TGCApp

def main():
    app = TGCApp()
    app.run()

if __name__ == "__main__":
    main()
