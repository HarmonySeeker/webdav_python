# WebDav python service

This README assumes that you've installed:
- django(vers. 2.1.7)
- django rest framework(https://www.django-rest-framework.org/)
- python 3.5 or higher


## Test

After starting server through terminal command "python3 manage.py runserver" or "python manage.py runserver" there will be a set of links available for testing:

### File uploading

Go to 127.0.0.1:8000/init_app/upload/ (or to your own custom address). The file uploaded through this web page will be downloaded at the root media folder.

### List contains of given folder

Go to 127.0.0.1:8000/init_app/source/ there you will see a root folder with its contains. You can walk down the folders to view or delete them(notice that you can delete ONLY EMPTY folders). Also you can delete or download all files which are listed there.

### List all folders

Go to 127.0.0.1:8000/init_app/full_source to view every folder and file which are contained within the root directory. 


---- 
(All of the commands are for linux terminal)
