if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "Checking and installing dependencies..."
pip cache purge
pip install --upgrade pip --quiet
pip install pygame numpy matplotlib --quiet
python3 chess.py
deactivate