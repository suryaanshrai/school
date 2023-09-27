# school
Video presentation with voice over: https://youtu.be/06H9vf2SrDc?si=0lPtWYGmP0leXSZY

Video presentation for CS50 submission: https://youtu.be/XZ5SIozA9gQ?si=ai5HH2aahAWorQp0

This document contains the following sections: 
- [Overview](#overview)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Project structure](#project-structure)
- [How to run the application](#how-to-run-the-application)
    - [Usernames and passwords](#usernames-and-passwords)
- [User verification](#user-verification)
- [User Privileges](#user-privileges)

## Overview
This project was chosen by me as I wanted to build something that can have some possible application in real life even if its not something entirely new. I happen to understand the school in which I used to study well enough to design an application that can help in its functioning. So, I decided to build a school management system with some essential features that I can think of as my final project of the CS50 web course.

## Distinctiveness and Complexity
The project is clearly different from any other project of the course, both in its functionality and purpose. This project aims to assisst in the operation of an educational instute, by providing features that may improve otherwise slower or less efficient traditional methods. Example: Adding something in the schedule of a student (such as an assignment) is better than just announcing the assignment in the classroom.

Here is a more detailed explaination of the project's applications and features:

The project's name (given through the django-admin command) is capstone2. It contains three applications, with the following features:

- home
    - Manages the homepage and users who are not registered with the school.
    - Allows logged in students to request addition of a news article or image in the school website.
    - Allows employees to approve or reject such submission requests made by students.
    - Allows the 'master' user to start a new academic session. Starting a new academic session archives all the news articles and images, deallocates everyone from the classrooms and deletes all the notices issued by the teachers.

- student
    - Displays test/assignment scores to student
    - Displays notices published for a classroom
    - Displays the scheduled tasks that are yet due to the user. A user can add anything to their schedule if they wish.
    - An employee can assign tasks to an entire classroom as via adding it to the classroom's schedule
    - An employee can release test score of a classroom by either manually entering it for the entire class or uploading a csv file.
    - An employee can add a notice for a classroom

- library
    - Displays the books issued with their due date of return and penalties accrued (if any) to the user.
    - Allows user to search for a book or author and also see its availibility
    - Librarian can Issue/Return a book to a user or clear their penalties
    - Librarian can add new books to the library, one by one or through a csv file.
    - Librarian can search for a username and see the list of books issued by them


## Project structure
The project contains three applications: home, student and library. In each application there is a `views.py` file that contains various django views and a `urls.py` file which handles the requests from various urls. Each application also contains a `templates` folder to store the django templates and a `static` folder to store static files such as css and js.

In the `home` application, there are two files `emp_ids.txt` and `stud_ids.txt`. These files contains a list of usernames for employees and students. Only these usernames are allowed to be registered on the application (unless registered from the admin site). This is to ensure that only people from that school register there.

All the images that are uploaded in the news and gallery section are stored in `home/static/news` and `home/static/gallery`.

## How to run the application
- Clone the repository on your local system by executing `git clone https://github.com/suryaanshrai/school.git`
- Open this directory and execute `python manage.py runserver` 
- Then open your browser and go to `127.0.0.1:8000`
- You can register as a student, teacher, teacher, librarian or master based on whichever part of the application you want to explore.

#### Usernames and passwords
The following student and teacher accounts contains some default values in them
- S_1003: WordPass@123
- E_101: WordPass@123
- librarian:Qwerty@123
- master: password

If you want to create a new student user, register on the site with a username that starts with `S_` followed by a number between 1000 and 1500, which is assumed here to be there school id.

If you want to create a new employee user, register on the site with a username that starts with `E_` followed by a number between 100 and 150, which is assumed here to be there employee id.

## User verification
Note that the application verifies the username in the backend. Only those students whose username is in the list of students in `student/stud_ids.txt` and only those employees whose username is in the list of employees in `student/emp_ids.txt` are allowed to register in the application.

So, usernames such as `jamespotter81` or `newstudent` or anything other than the names in the files are not allowed. This is to impose the usernames and restrict the application to a certain group of people. 

All student usernames start with S followed by an underscore, followed by a number between 1000 and 1500. Similarly, all employee usernames start with an E followed by an underscore followed by a number between 100 and 150.

`librarian` is a username reserverd for the librarian of the school.

On the frontend, the site also verifies that the email id is valid using an api call to an external site and also ensures that the password is strong enough.

## User Privileges
There are privileges given to certain users. These privileges and restrictions are as follows:

- Non-logged in users: These users can only view the homepage, gallery, and news section.
- Logged in users who are students: These users can make submissions for gallery and news sections, open their classroom or check the library.
- Logged in users who are teachers: These users can review the submission made by the users, access a classroom, issue a notice for them or add anything to their schedule.
- Logged in user who is `librarian`: This user can issue/return books from students, add books to the library, clear penalty if any on a student.
- Logged in user who is `master`: The `master` user can restart the academic session.