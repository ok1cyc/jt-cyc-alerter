import sqlite3
from datetime import datetime, timedelta

class SQLiteChecker:
    def __init__(self, db_filename):
        # Create and store the connection during initialization
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()

    def is_workedB4(self, callsign, days):
        """
        Checks if a callsign has been worked within the past `days` days.

        Parameters:
        - callsign (str): The callsign to search for.
        - days (int): The number of days back from today to include.

        Returns:
        - bool: True if the callsign is found in the date range, False otherwise.
        """
        # Calculate the date threshold
        date_threshold = datetime.now() - timedelta(days=days)

        query = """
        SELECT 1 FROM Log
        WHERE callsign = ? AND qsodate >= ? LIMIT 1;
        """
        
        try:
            # Execute the query with the parameters
            self.cursor.execute(query, (callsign, date_threshold.strftime('%Y-%m-%d')))
            result = self.cursor.fetchone()
            # Return True if a record is found, otherwise False
            return result is not None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def close_connection(self):
        """Method to close the database connection when done"""
        if self.conn:
            self.conn.close()