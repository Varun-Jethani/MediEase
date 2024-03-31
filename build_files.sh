
echo "Build Start"
pip install -r requirements.txt
python3.12 manage.py collectstatic --no-input --clear
echo "Build End"