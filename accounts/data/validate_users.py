from pydantic_core._pydantic_core import ValidationError
from user_models import *

if __name__=="__main__":

    users = [
        {'username': 'joe', 'password': 'schmoe'},
        {'username':'joe'},
        {'username':'joe','password':'schmoe','extra':'ex'}
    ]

    for u_dict in users:
        try:
            u = User(**u_dict)
        except ValidationError as e:
            print(f"--\n{e}\n--")
        else:
            print(u)