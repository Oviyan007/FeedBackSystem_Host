# FeedBackSystem
# How to Run the code 
### clone this repository and open it in vscode 
### To clone the repo 
```
git clone https://github.com/Oviyan007/Feedback_System.git
```
### open the terminal in Vs Code run following command
### To Activate the virtual environment
```
 .venv\Scripts\activate 
```
it may show the error if it shows run below command 
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

 .venv\Scripts\activate
```

To install requirement for this projects 
```
pip install -r requirements.txt

```
## Apply Migrations 
```
python manage.py migrate

```

Type following command to start developement server 

```
python manage.py runserver

```

### Open your browser and go to http://127.0.0.1:8000/Test.


