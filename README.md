
![](other/assets/about.gif)

# LabBook
A web system to book access to your lab while staying safe during the pandemic.

## Problem
Many researchers, among them PhD students, need to access their laboratories. Now that the campus is closed for everyone, none of them can run experiments etc. At some point though, we will need to find a way for the scientific research to safely continue by allowing a limited number of people to work on campus at a time, while taking into account where they need to work and making sure it is safe for them.

## Goal
Make a smart room/lab booking system for performing research safely during the pandemic. We imagine the system to handle researchers' requests to access rooms inside buildings on campus to do experiments, while taking into consideration how many people would be present in each room/section/floor/building at each time and checking this against set safety limits to determine whether to grant them access.

## Setup
```
git clone https://github.com/roesel/book/
cd book
python -m venv venv
venv\Scripts\activate
(venv) pip install -r requirements.txt
```
## Run webserver
```
python reset_db.py
flask run
```
