# testsqlchecker.py
from sqlite_checker import SQLiteChecker

db_filename = r"G:\Můj disk\Log4OM\ok1cyc_log4om.SQLite"  # Use the raw string literal to handle Windows path
checker = SQLiteChecker(db_filename)

# Test callsign and days_back value
test_callsign = "RA9UKO"
days_back = 30

# Call is_workedB4
worked_before = checker.is_workedB4(test_callsign, days_back)
print(f"Has the callsign {test_callsign} been worked before within {days_back} days? {worked_before}")
