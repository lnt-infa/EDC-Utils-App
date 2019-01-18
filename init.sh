. .env

CMD="docker run -it --rm --name edc-mgmt-app -v ${DATA_DIR}:/usr/src/app/db edc-mgmt-app python manage.py"

echo "============== Creating scripts"
$CMD makemigrations edcmgmt
echo "============== Initializing the database"
$CMD migrate
echo "============== Creating a super user"
$CMD createsuperuser
