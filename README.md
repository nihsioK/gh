git clone https://github.com/nihsioK/gh
cd gh

virtualenv -p pyhton3 venv
source venv/bin/activate
pip install -r requirements.txt

docker build -t django-rest-api .

docker run -d -p 8000:8000 django-rest-api

docker exec -it [container_id] python manage.py migrate


