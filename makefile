clean:
	rm -rf venv

venv/bin/activate: requirements.txt
	python -m venv venv
	pip install -r requirements.txt

run: venv/bin/activate
	clear
	python wyrdle.py