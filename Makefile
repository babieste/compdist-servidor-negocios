setup-dev-environment:
	python3 -m venv venv

install-deps:
	pip3 install -r requirements.txt

run-dev:
	flask run -p 5001

run-prd:
	gunicorn wsgi:app -b 0.0.0.0:5001
