import os
import json
import csv

# dictionary key - question, value - dictionary of key - state, value - list of rows(data for that question / state)
class DataStore:
    def __init__(self, csv_file):
        self.data, self.header = self.read_csv(csv_file)
        
    def read_csv(self, csv_file):
        data_dict = {}
        with open(csv_file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                question = row[header.index('Question')]
                state = row[header.index('LocationDesc')]
                if question not in data_dict:
                    data_dict[question] = {}
                if state not in data_dict[question]:
                    data_dict[question][state] = []
                data_dict[question][state].append(row)

                
        return data_dict, header

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        self.csv_path = csv_path
        self.data_store = DataStore(self.csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    # returns all the states- data dictionary in for a given question
    def get_data_by_question(self, question):
        return self.data_store.data[question]
    
    # writes a csv file to test if the data is being read correctly
    def test_ingestion(self, question, state):
        rows = self.data_store.data[question][state]
        # write to test.csv to confirm that the data is being read correctly
        with open('test.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.data_store.header)
            writer.writerows(rows)
        print("--- Data ingested successfully ---")

    # weites the whole data to a csv file
    def test_ingestion(self):
        with open('test.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.data_store.header)
            for question in self.data_store.data:
                for state in self.data_store.data[question]:
                    writer.writerows(self.data_store.data[question][state])
        print("--- Data ingested successfully ---")