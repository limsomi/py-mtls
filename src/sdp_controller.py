from utils.crypto_utils import *
import json,time

class SDP_Controll:
    # def __init__(self):

    def spa_auth(self,data):
        try:
            decrypted = decrypt(data)
            payload = json.loads(decrypted.decode())

            if abs(time.time() - payload["timestamp"]) > 30:
                print("Rejected: Expired packet")
                return 
            if payload['request_port']==1234:
                print("Rejected: Expired packet")
                return 
            return payload

        except Exception as e:
            print("Invalid packet:", e)

        