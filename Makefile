setup-dev-environment:
	python3 -m venv venv

install-deps:
	pip3 install -r requirements.txt

run-dev:
	flask run -p 5001

run-prd-serv-1:
	SERVIDOR_ID=1 gunicorn wsgi:app -b 0.0.0.0:5001

run-prd-serv-2:
	SERVIDOR_ID=2 gunicorn wsgi:app -b 0.0.0.0:5002

run-prd-serv-3:
	SERVIDOR_ID=3 gunicorn wsgi:app -b 0.0.0.0:5003
