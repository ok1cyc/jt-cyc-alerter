from pyhamtools import LookupLib, Callinfo
import redis

class DXCCChecker:
    def __init__(self):
        # Initialize the lookup library only once when the instance is created
        r = redis.Redis()
        self.lookuplib = LookupLib(lookuptype="clublogxml", filename="cty.xml")
        self.lookuplib.copy_data_in_redis(redis_prefix="CL", redis_instance=r)
        self.lookuplib = LookupLib(lookuptype="redis", redis_instance=r, redis_prefix="CL")
        self.callinfo = Callinfo(self.lookuplib)

    def get_dxcc_id(self, callsign):
        """
        Returns the DXCC ID (ADIF) for the given callsign.
        If the callsign is not found, returns 0.
        """
        try:
            # Fetch DXCC information for the given callsign
            info = self.callinfo.get_adif_id(callsign)
            return info if info is not None else 0  # Return 0 if not found
        except Exception as e:
            print(f"Error retrieving DXCC ID for {callsign}: {e}")
            return 0  # Return 0 on error
