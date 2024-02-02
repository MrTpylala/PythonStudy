import os
import shutil
from git import Repo

def initialize_repository(repo_path): #Инициализация репозитория Git
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            print("Репозиторий уже существует. Используем существующий.")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        try:
            repo = Repo.init(repo_path)
            print("Репозиторий успешно инициализирован.")
        except Exception as e:
            print(f"Ошибка: {e}")

    return repo

def create_file(repo_path, file_name, content): # Создание файла
    file_path = os.path.join(repo_path, file_name)
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Файл {file_name} успешно создан.")

def delete_file(repo_path, file_name): # Удаляем файл из папки репозитория
    file_path = os.path.join(repo_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_name} успешно удален.")
    else:
        print(f"Файл {file_name} не существует.")

def move_file(repo_path, source_name, dest_folder, dest_name=None): # Перемещаем файл внутри папки репозитория
    source_path = os.path.join(repo_path, source_name)

    # Если dest_name не указан, используем то же имя файла
    if dest_name is None:
        dest_name = os.path.basename(source_name)

    dest_path = os.path.join(repo_path, dest_folder, dest_name)

    # Проверяем существование папки-назначения
    dest_folder_path = os.path.join(repo_path, dest_folder)
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)

    if os.path.exists(source_path):
        shutil.move(source_path, dest_path)
        print(f"Файл перемещен из {source_path} в {dest_path}")
    else:
        print(f"Файл {source_name} не найден")

def copy_file(repo_path, source_name, dest_folder, dest_name=None): # Копируем файл внутри папки репозитория
    source_path = os.path.join(repo_path, source_name)

    # Если destination_name не указан, используем то же имя файла
    if dest_name is None:
        dest_name = os.path.basename(source_name)

    dest_path = os.path.join(repo_path, dest_folder, dest_name)

    if os.path.exists(dest_path):
        print(f"Файл {dest_name} уже существует в {dest_folder}. Выберите другое имя.")
        return
        
    if os.path.exists(source_path):
        shutil.copy2(source_path, dest_path)
        print(f"Файл {source_name} успешно скопирован в {dest_folder}/{dest_name}.")
    else:
        print(f"Файл {source_name} не найден")

if __name__ == "__main__":
    # Инициализизация репозиторий
    while True:
        repo_path = input("Введите путь до репозитория: ")

        if os.path.exists(repo_path):
            repo = initialize_repository(repo_path)
            break
        else:
            print("Указанный путь не существует. Пожалуйста, введите существующий путь.")

    while True:
        print("\nМеню:")
        print("1. Создать файл")
        print("2. Удалить файл")
        print("3. Переместить файл")
        print("4. Скопировать файл")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            file_name = input("Введите имя файла: ")
            content = input("Введите содержимое файла (по умолчанию - пусто): ")
            create_file(repo_path, file_name, content)
        elif choice == "2":
            file_name = input("Введите имя файла для удаления: ")
            delete_file(repo_path, file_name)
        elif choice == "3":
            source = input("Введите имя файла для перемещения: ")
            dest_folder = input("Введите путь, куда переместить файл: ")
            dest_name = input("Введите имя файла, которое будет после перемещения (при пустом значении будет оригинальное имя): ")
            move_file(repo_path, source, dest_folder, dest_name)
        elif choice == "4":
            source = input("Введите имя файла для копирования: ")
            dest_folder = input("Введите путь, куда скопировать файл: ")
            dest_name = input("Введите имя файла, которое будет после перемещения (при пустом значении будет оригинальное имя): ")
            copy_file(repo_path, source, dest_folder, dest_name)
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите действие из меню.")
