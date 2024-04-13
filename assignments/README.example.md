Name: Frecus Tudor George  
Group: 334CA

# Homework 1 - Le Stats Sportif
<!-- #### Este recomandat să folosiți diacritice. Se poate opta și pentru realizarea în limba engleză.  -->

Organizare
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

***Obligatoriu:*** 


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

Acest model de README a fost adaptat după [exemplul de README de la SO](https://github.com/systems-cs-pub-ro/so/blob/master/assignments/README.example.md).