from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import random


def hasAttribute(obj: dict, attribute: str):
    """Check whether a given dict contains a specific attribute"""

    if obj is None:
        return False

    return attribute in obj


class ValidationHelper:
    def __init__(self, usercontroller: UserController):
        self.usercontroller = usercontroller

    def validateAge(self, userid: str):

        user = self.usercontroller.get(id=userid)

        if user['age'] < 0 or user['age'] > 120:
            return "invalid"

        if user['age'] >= 18:
            return "valid"

        return "underaged"


class ValidationHelper2:
    def __init__(self):
        self.usercontroller = UserController(
            dao=DAO(collection_name='user')
        )

    def validateAge(self, userid: str):

        user = self.usercontroller.get(id=userid)

        if user['age'] < 0 or user['age'] > 120:
            return "invalid"

        if user['age'] >= 18:
            return "valid"

        return "underaged"


def diceroll():

    number = random.randint(1, 6)

    if number >= 5:
        return True

    return False