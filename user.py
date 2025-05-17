from changer import csv_to_dict


class User:
    def __init__(self, Aword='' , Rword=''):
        self.Aword = Aword
        self.Rword = Rword

    def __str__(self):
        return (f'Aword: {self.Aword}\n'
                f'Rword: {str(self.Rword)}\n'
                )

    def save(self):
        record = f'{self.Aword},{self.Rword}\n'
        file = open("users.csv", "a",encoding="UTF-8")
        file.write(record)
        file.close()

    @staticmethod
    def get_all_users():
        users = {}
        file = csv_to_dict("users.csv")
        # file = open('users.csv', 'r')
        # lines = file.readlines()
        # lines = lines[1:]
        # for line in lines:
        #     data = line.split(',')
        #     user = User(str(data[0]))
        #     users[str(data[0])] = str(user)
        return file









print(User.get_all_users())