from passlib.context import CryptContext

#hashing password
pwdcontext=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash(password: str):
    return pwdcontext.hash(password)

