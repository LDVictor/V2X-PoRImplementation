import sys
import time
from resources.ran import RAN
from resources.vehicle import Vehicle

vehicle = Vehicle("127.0.0.3", 8003, 3)
issuer_verifier = RAN("127.1.0.1", 8088, 88)

def generate_credential(id):
    return issuer_verifier.generate_credential_offer(10, None, id, None)

def verify_credential(vc, id):
    return issuer_verifier.verifica_credencial(vc, id)
