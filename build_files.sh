
echo "Build Start"
python -m pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
echo "Build End"