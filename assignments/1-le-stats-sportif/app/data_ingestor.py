"""
Module to ingest data from a csv file
"""
import csv

class DataStore:
    """Class to store the data from the csv file in a dictionary"""
    def __init__(self, csv_file):
        self.data, self.header = self.read_csv(csv_file)

    def read_csv(self, csv_file):
        """Reads the csv file and stores the data in a dictionary"""
        data_dict = {}
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
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
    """Class to ingest data from a csv file"""
    def __init__(self, csv_path: str):
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
            ('Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
            'activity (or an equivalent combination)'),
            ('Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
            'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
            'physical activity and engage in muscle-strengthening activities on 2 or more '
            'days a week'),
            ('Percent of adults who achieve at least 300 minutes a week of moderate-intensity '
            'aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic '
            'activity (or an equivalent combination)'),
            ('Percent of adults who engage in muscle-strengthening activities on 2 or more '
            'days a week'),
        ]

    # writes the whole data to a csv file
    def test_ingestion(self):
        """Writes the whole data to a csv file"""
        with open('test.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.data_store.header)
            for question in self.data_store.data:
                for state in self.data_store.data[question]:
                    writer.writerows(self.data_store.data[question][state])
        print("--- Data ingested successfully ---")

    # returns all the states- data dictionary in for a given question
    def get_data_by_question(self, question):
        """Returns all the states- data dictionary in for a given question"""
        return self.data_store.data[question]

    # writes a csv file to test if the data is being read correctly
    def test_ingestion(self, question, state):
        """Writes a csv file to test if the data is being read correctly"""
        rows = self.data_store.data[question][state]
        # write to test.csv to confirm that the data is being read correctly
        with open('test.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.data_store.header)
            writer.writerows(rows)
        print("--- Data ingested successfully ---")
