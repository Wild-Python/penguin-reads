.PHONY: runserver
runserver:
ifeq ($(port),)
	python manage.py runserver
else
	python manage.py runserver $(port)
endif

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: migrations
migrations:
ifeq ($(app),)
	python manage.py makemigrations
else
	python manage.py makemigrations $(app)
endif

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: shell
shell:
	python manage.py shell

.PHONY: dbshell
dbshell:
	python manage.py dbshell


.PHONY: tailstart
tailstart:
	python manage.py tailwind start


