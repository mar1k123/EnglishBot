class User:
    def __init__(self, id: int, name='', age=0, sex=''):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Age: {str(self.age)}\n'
                f'Sex: {self.sex}')

    def save(self):
        record = f'{self.id},{self.name},{self.age},{self.sex}\n'
        file = open("users.csv", "a")
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
            user = User(int(data[0]), data[1], int(data[2]), data[3])
            users[int(data[0])] = user
        return users