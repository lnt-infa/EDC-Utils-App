# EDC-Utils-App
This repository contains an thin client (web UI) application providing utilities for the Informatica Enterprise Data Catalog. 
The utilities available are:
* EDC Environment manager utility: with this utility, manager multiple EDC environment, save/export/deploy resource definition or custom attribute 


This application leverage the REST API provided by with EDC, is written in Python and leverage the DJango framework.
Official REST API documents can be found [here](https://kb.informatica.com/proddocs/Product%20Documentation/6/IN_102_EnterpriseInformationCatalog[REST-API]Reference_en.pdf)

The application is package into a docker image for easier deployment


Getting Started
---------------

* Clone this repository
* build the docker image
```
./buid.sh
```
* Edit the file .env and specify the path for the data as well as the listen port for the webserver
```
DATA_DIR=$PWD/edcUtils/db
LISTEN_PORT=8000
```
* Execute the initialization script
The initialization script will create a new database file in the directory given by DATA_DIR and will create superuser, while creating the superuser, the process will ask for a username and a password to be used.
```
./init.sh
``` 
* Execute the start script
```
./start.sh
```
*Access the application
To use the application, use :
```
http://<hostname>:8000/
```

