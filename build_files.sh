
echo "Build Start"
python3.9 -m venv venv
source venv/bin/activate
echo "Venv activated"
pip install -r requirements.txt
echo "Requirements installed"
python3.9 manage.py collectstatic --no-input --clear
echo "Build End"