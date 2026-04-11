@echo off
echo 🚀 Initializing CrewAI Blog Team UI...
echo ---
py -m pip install -r requirements.txt
echo ---
echo ✨ Installation complete. Launching the Web Dashboard...
py -m streamlit run ui.py
pause
