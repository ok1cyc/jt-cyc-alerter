from callsign_knowledge_checker import CallsignKnowledgeChecker

test_callsigns = ["OK1DMP", "DEF456", "OK1AUP", "LMN012", "UNKNOWN"]

# Run the tests
for callsign in test_callsigns:
    checker = CallsignKnowledgeChecker(callsign)
    status = checker.check_status()
    print(f"Callsign '{callsign}' status: {status}")