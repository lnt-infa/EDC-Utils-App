. .env

CMD="docker run -d --rm --name edc-mgmt-app -v ${DATA_DIR}:/usr/src/app/db -p ${LISTEN_PORT}:8000 edc-mgmt-app python manage.py"

$CMD runserver 0:8000
