from utils.crypto_utils import *
import json,time

class SDP_Controll:
    # def __init__(self):

    def spa_auth(self,data,addr):
        try:
            decrypted = decrypt(data)
            payload = json.loads(decrypted.decode())

            if abs(time.time() - payload["timestamp"]) > 30:
                print("Rejected: Expired packet")
                return 
            if addr[0]=='192.168.10.2':
                print("Rejected: Expired packet")
                return 
            print(f"source_ip {addr[0]} pass")
            return payload

        except Exception as e:
            print("Invalid packet:", e)

        