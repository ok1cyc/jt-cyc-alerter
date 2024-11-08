class MobileChecker:
    def __init__(self):
        pass

    def is_mobile(self, callsign):
        """
        Checks if the callsign ends with '/P' or '/M'.
        
        Parameters:
        - callsign (str): The callsign to check.
        
        Returns:
        - bool: True if the callsign ends with '/P' or '/M', False otherwise.
        """
        return callsign.endswith('/P') or callsign.endswith('/M')