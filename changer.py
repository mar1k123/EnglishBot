import csv

def csv_to_dict(file_path):
    # Инициализируем пустой словарь для хранения данных
    data_dict = {}

    # Открываем csv файл для чтения
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        # Читаем данные из csv и добавляем их в словарь
        for row in csv_reader:
            # Используем значение первого столбца как ключ
            key = row[next(iter(row))]
            data_dict[key] = row

    return data_dict

file_path = str(r'C:\Users\user\PycharmProjects\EnglishBot\users.csv')
data = csv_to_dict(file_path)

print(data)