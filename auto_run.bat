@echo off
cd /d "C:\Allergy weather project"
python -m engine.bulletin_generator
python email_sender.py