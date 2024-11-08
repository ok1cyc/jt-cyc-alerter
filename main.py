from udp_server import UDPServer
from dxcc_checker import DXCCChecker
from rda_checker import RDAChecker
from qrz_checker import QRZChecker
from rda_worked_checker import RDAWorkedChecker
from mobile_checker import MobileChecker
from sqlite_checker import SQLiteChecker
from local_rda_checker import LocalRDAChecker
from ignore_list_maintainer import IgnoreListMaintainer
from alert_list_maintainer import AlertListMaintainer
from alerter import Alerter
from datetime import datetime

def check_rda_worked_and_process(callsign, rda_code, rda_worked_checker, ignore_list_maintainer, alert_list_maintainer, alerter):
    """Checks if an RDA code has been worked and updates lists accordingly."""
    if rda_worked_checker.is_worked(rda_code):
        print(f"RDA code '{rda_code}' has been worked.")
        ignore_list_maintainer.add_callsign(callsign)
        print(f"Callsign '{callsign}' added to the ignore list because RDA has been worked.")
    else:
        alert_list_maintainer.add_callsign(callsign, f"{callsign} - New RDA: {rda_code}")
        alerter.shoot_alert(callsign, alert_list_maintainer)
        print(f"RDA code '{rda_code}' has not been worked.")

if __name__ == "__main__":
    port = 1100  
    server = UDPServer(port=port)
    ignore_list_maintainer = IgnoreListMaintainer()
    alert_list_maintainer = AlertListMaintainer()
    dxcc_checker = DXCCChecker()
    rda_checker = RDAChecker()
    qrz_checker = QRZChecker()
    rda_worked_checker = RDAWorkedChecker()
    mobile_checker = MobileChecker()
    db_filename = r"G:\Můj disk\Log4OM\ok1cyc_log4om.SQLite" 
    sqlite_checker = SQLiteChecker(db_filename)
    local_rda_checker = LocalRDAChecker('rda.csv')
    alerter = Alerter(url="https://ntfy.ok1cyc.net:8031", topic="ham", silence_period=60)
    
    for callsign in server.start():
        dxcc_id = dxcc_checker.get_dxcc_id(callsign)

        if dxcc_id in [15, 54, 61, 126, 151]:
            mobile = mobile_checker.is_mobile(callsign)
            
            if not mobile and sqlite_checker.is_workedB4(callsign, 365):
                continue
            
            if ignore_list_maintainer.is_ignored(callsign):
                continue
            
            rda_code = None if mobile else local_rda_checker.get_rda_code(callsign)
            
            alert_data = alert_list_maintainer.get_data(callsign)
            
            match (rda_code, alert_data, mobile):
                # Case for non-None RDA code
                case (rda_code, _, _) if rda_code is not None:
                    check_rda_worked_and_process(callsign, rda_code, rda_worked_checker, ignore_list_maintainer, alert_list_maintainer, alerter)

                # Non-mobile not yet alerted callsign with RDA not retrieved locally
                case (None, None, False):
                    rda_code = rda_checker.get_rda(callsign)
                    if rda_code != 0:
                        check_rda_worked_and_process(callsign, rda_code, rda_worked_checker, ignore_list_maintainer, alert_list_maintainer, alerter)
                    else:
                        alert_list_maintainer.add_callsign(callsign, f"{callsign} - Unknown RDA")
                        alerter.shoot_alert(callsign, alert_list_maintainer)
                # Callsign which has unknown RDA and was already alerted due to that unknown RDA

                case (None, alert_data, _) if alert_data is not None:
                    message, timestamp = alert_data
                    if timestamp <= datetime.now():
                        alerter.shoot_alert(callsign, alert_list_maintainer)

                # Mobile callsign (RDA locally not checked => unknown) which has not been alerted yet
                case (None, None, True):
                    alert_list_maintainer.add_callsign(callsign, f"{callsign} - Mobile callsign")
                    alerter.shoot_alert(callsign, alert_list_maintainer)