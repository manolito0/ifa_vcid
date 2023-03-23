#Methode um Passwörter zu hashen
#Quelle: https://passlib.readthedocs.io/en/stable/

from passlib.hash import pbkdf2_sha256

#Passwörter generieren
def generate_password(password):
    return pbkdf2_sha256.hash(password)

#Passwörter verifizieren
def verify_password(raw_password, encoded_password):
    return pbkdf2_sha256.verify(raw_password, encoded_password)
