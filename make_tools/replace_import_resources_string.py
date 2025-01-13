import os


def replace(directory: str):
    # Проверка, существует ли директория
    if not os.path.isdir(directory):
        print(f"Ошибка: Директория {directory} не существует.")
        return

    # Поиск всех .py файлов в директории и поддиректориях
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                # Чтение содержимого файла
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Замена строки
                updated_content = content.replace(
                    "import resources_rc", "import source.view.ui.resources_rc"
                )

                # Проверка, была ли выполнена замена
                if content != updated_content:
                    # Сохранение изменений
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"Обновлено: {file_path}")
                else:
                    print(f"Без изменений: {file_path}")


if __name__ == "__main__":
    # Укажите директорию для обработки
    directory_to_process = "src/ui"
    replace(directory_to_process)
