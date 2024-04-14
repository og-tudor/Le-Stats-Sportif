Name: Frecus Tudor George  
Group: 334CA

# Homework 1 - Le Stats Sportif
<!-- #### Este recomandat să folosiți diacritice. Se poate opta și pentru realizarea în limba engleză.  -->

Project Structure
-
<!-- 1. Explicație pentru soluția aleasă: -->
The project is structured in 4 main files: __init__.py, data_ingestor.py, routes.py and task_runner.py. The __init__.py file is used to initialize the Flask app and the database connection. The data_ingestor.py file is used to ingest the data from the csv files into the database. The routes.py file is used to define the routes of the Flask app. The task_runner.py file is used to process the request for the task.

### Data Ingestion :
- This class is used to store and interact with the data from the csv files. 
- The data is stored as an object of the class "DataStore" which contains the data in a dictionary format. The dictionary is structured as follows: 
    - The keys of the dictionary are the questions from the csv files.
    - The values of the dictionary are dictionaries where the keys are the states.
    - The values of the inner dictionaries are lists of dictionaries where each dictionary entry is a row from the csv file.  
``` data_dict[question][state] ```

- The data is ingested from the csv files using the "read_csv" method. The method reads the csv file and stores the data in the "DataStore" object using the imported csv module.

### Routes :
- This file contains the routes of the Flask app.
- The job counter is used to keep track of the total number of jobs that have been processed.  
it is synchronized using a lock to avoid race conditions.
- For a POST_REQUEST, a coresponding task object is created and added to the task queue.   
Jobs_list indicates what the request is, example: jobs_list[0] = states_mean  
``` job = Task(webserver.job_counter, question, jobs_list[i], state)  ```
``` thread_pool.add_task(job) ```
- For a GET_REQUEST, the response is sent back to the client and   
it can either be a error message or the result of the task.

### Task Runner :
- The ThreadPool class is used to create a pool of threads that will process the tasks, it is also used to add tasks to the queue, and manage the threads.
- Each thread from Task Runner class is constantly checking the queue for new tasks and assigns them to the threads in the thread pool.
- The threads are not busy waiting because the queue.get() method is blocking until a new task is added to the queue. 
``` task = self.q_jobs.get(block=True, timeout=None) ```
- When a task is created all information that is needed to process the task is stored in the task object. It sees which type of request it is and it processes the request accordingly.
- When the task is finished, the result is stored in the task object and the task is added to a queue of finished tasks in the ThreadPool class.

## Implementation
- All the tasks from the requirements have been implemented.
- Added a new route ``` http://localhost:5000/api/results ``` which returns the results of all the tasks that have been processed so far and their respective data.
- Unit tests could have checked many more edge cases. /api/num_jobs can't really be tested because as soon as a request is made, one of the threads will process it and the number of jobs will be back to 0. I tested it manually with sleep() function and it worked as expected.

### Mentions :
- I found the project really useful to learn python, before it I had no experience with python.
- Learned that Flask is a really powerful tool for creating web applications.
- I would consider the implementation efficient, the data is stored in a dictionary format which makes it easy to access and process the data. But there are certainly ways to improve the implementation, for example processing the data in a more efficient way.
- I could have modularized the code better, such that in routes I would only call a method from ThreadPool which would create my Task instead of importing Task class in routes.

<!-- ***Obligatoriu:*** 


* De făcut referință la abordarea generală menționată în paragraful de mai sus. Aici se pot băga bucăți de cod/funcții - etc.
* Consideri că tema este utilă?
* Consideri implementarea naivă, eficientă, se putea mai bine?

***Opțional:***


* De menționat cazuri speciale, nespecificate în enunț și cum au fost tratate.


Implementare
-

* De specificat dacă întregul enunț al temei e implementat
* Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor
* De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru
* Dificultăți întâmpinate
* Lucruri interesante descoperite pe parcurs


Resurse utilizate
-

* Resurse utilizate - toate resursele publice de pe internet/cărți/code snippets, chiar dacă sunt laboratoare de ASC

Git
-
[Le-Stats-Sportif](https://github.com/og-tudor/Le-Stats-Sportif)

Ce să **NU**
-
* Detalii de implementare despre fiecare funcție/fișier în parte
* Fraze lungi care să ocolească subiectul în cauză
* Răspunsuri și idei neargumentate
* Comentarii (din cod) și *TODO*-uri

Acest model de README a fost adaptat după [exemplul de README de la SO](https://github.com/systems-cs-pub-ro/so/blob/master/assignments/README.example.md). -->