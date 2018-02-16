freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

install:
	sudo pip install -r requirements.txt
