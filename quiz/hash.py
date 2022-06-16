from pickletools import read_uint1
from flask_bcrypt import Bcrypt


class Hashing():
    def __init__(self):
        # creating an instance of the Bcrypt
        self.bcrypt = Bcrypt()

    def gen_hash(self,password):
        hashed_pass = self.bcrypt.generate_password_hash(password=password)
        return hashed_pass.decode('utf-8')

    def check_hash(self,hashed_pass,login_pass):
        check_pass = self.bcrypt.check_password_hash(hashed_pass,login_pass)
        return check_pass

# h = Hashing()
# x = h.gen_hash('password')
# y = h.check_hash(x,'password')
# print(x,y)


# h2 = Hashing()
# x2 = h.gen_hash('password')
# y2 = h.check_hash(x2,'password')
# print(x2,y2)


# print(x is x2 )