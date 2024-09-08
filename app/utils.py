from passlib.context import CryptContext # for hashing password

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pass_context.hash(password)

def verify_password(plain_pwd, hashed_pwd):
    return pass_context.verify(plain_pwd, hashed_pwd)
