# Temporary database for testing.
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])

users_dic = {"Alice": password_context.hash("123"), "Rute": password_context.hash("456")}
