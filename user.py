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
        file = open('users.csv', 'r')
        lines = file.readlines()
        lines = lines[1:]
        for line in lines:
            data = line.split(',')
            user = User(str(data[0]), str(data[1]))
            users[str(data[0])] = user
        return users