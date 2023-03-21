# Meta-Back-end-Capstone
For Coursera Meat backend capstone project
<font color="RED">
PLEASE NOTE TAHT FOR THIS PROJECT I DIDN'T USE THE SAME APP NAME AS REQUIRED IN THE PROJECT, THE APP NAME "LITTLELEMONAPI" IS USED INSTEAD OF "reastaurant" WHICH IS ALSO A TYPO!
</font>

Step One:
Activate the pipenv please follow the below commands,
 ```
pipenv shell
pipenv install
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver
 ```

Alternation if above pipenv not working, then you have to install the below dependency packages
 ```
pipenv --python /usr/bin/python3 #assume using the Ubuntu Linux system.
pipenv install django
pipenv install djangorestframework
pipenv install mysqlclient
pipenv install djoser
 ```
 
Step Two:
Connect to the MySQL follow the below commands to create the root user with 'password' as the password,the create the 
```
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
CREATE DATABASE littlelemon;
exit;
```
Step Three:
Create the superuser for the admin page using command below:
python manage.py createsuperuser
Then you can login the admin page of http://localhost:8000/admin 

Step Four:
For testing the user registration, please test using Insomnia, using link http://127.0.0.1:8000/api-token-auth/
Select POST method and post with username and password then a token will be generated as below, this token is needed in testing the menu APIs, otherwise the access will be denied for any CURD operation.
 ![image](https://user-images.githubusercontent.com/11548466/226509678-0ab425eb-0dca-41c6-8922-f083764dc052.png)


Step Five:
For testing the menu API, please use the token generated above and enable in the auth section in Insomnia, otherwise the authentication will be failed as below, the menu link is http://127.0.0.1:8000/menu/
 ![image](https://user-images.githubusercontent.com/11548466/226509692-0b777035-6991-4835-ae44-4f625209bf4f.png)

Once the Token is enabled, the CRUD operation for the Menu is enabled. Just to remember the add the payload with below information,
  ![image](https://user-images.githubusercontent.com/11548466/226509707-454791dc-a6a9-4afe-a033-01f50d12479d.png)


Step Six:
Testing the Booking APIs with link of http://127.0.0.1:8000/bookings/ can be also tested with Insomnia, in this case the authentication is not implement for differentiation. 
You can do the CURD operation inside Insomnia, the GET need no payload, the POST method would need payload in JSON format as below:
  ![image](https://user-images.githubusercontent.com/11548466/226509715-5debfa1b-f7e1-4d24-bc73-dbee0461b5f7.png)

For the PATCH, PUT operation, you also need to include the id fields as below:
 ![image](https://user-images.githubusercontent.com/11548466/226509729-85b802a8-3f94-4121-b086-06840643dc84.png)

For the Delete operation, you just need to include the id fields but nothing else.

Step Seven:
Unit test file already created inside the test.py file, please run the command below
python manage.py test

Step Eight:
Above already proven that the API can be tested using Insomnia REST client
