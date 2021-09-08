import random
import string


if __name__ == "__main__":
    usernames = []
    for i in range(0, 100):
        username = ""
        for ii in range(0, random.randint(4, 40)):
            username += random.choice(string.ascii_letters + string.digits)
        usernames.append(username + "\n")
