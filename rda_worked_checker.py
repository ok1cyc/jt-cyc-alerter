import csv

class RDAWorkedChecker:
    def __init__(self, csv_file='worked_rda.csv'):
        self.csv_file = csv_file
        self.worked_rda_set = self.load_worked_rda()

    def load_worked_rda(self):
        """Loads the RDA codes from the CSV file into a set for faster lookup."""
        try:
            worked_rda_set = set()
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if row:
                        worked_rda_set.add(row[0])  # Add RDA code to the set
                        print(f"Loaded RDA Code: {row[0]}")  # Print each RDA code to stdout
            return worked_rda_set
        except FileNotFoundError:
            print(f"Error: The file '{self.csv_file}' does not exist.")
            return set()
        except Exception as e:
            print(f"An error occurred while loading the RDA data: {e}")
            return set()

    def is_worked(self, rda):
        """
        Checks if the given RDA code is included in the loaded RDA set.
        Returns True if RDA is found, otherwise False.
        """
        return rda in self.worked_rda_set

    def dump_worked_rda(self):
        """Prints the contents of the worked RDA set to the terminal."""
        print("Worked RDA Codes:")
        for rda in self.worked_rda_set:
            print(rda)
