import csv

def csv_to_list(file_path):
    data_list = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        # Создаем объект reader для чтения данных из CSV
        csv_reader = csv.reader(file)

        # Пропускаем заголовки, если они есть
        next(csv_reader, None)

        # Читаем данные из CSV и добавляем их в список
        for row in csv_reader:
            data_list.append(row)

    return data_list


# Укажите путь к вашему CSV файлу
file_path = 'C:\Users\user\PycharmProjects\EnglishBot/users.csv.'
data = csv_to_list(file_path)

# Печатаем полученный список
print(data)
