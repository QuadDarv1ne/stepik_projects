import json
from sqlalchemy.orm import Session
from app.database import engine
from app.models import MediaFile

# Путь к файлу JSON
json_file_path = './zametki/musicians.json'

# Функция для загрузки данных из JSON файла
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для записи данных в базу данных
def save_data_to_db(data):
    # Создаем сессию
    session = Session(bind=engine)

    try:
        # Перебираем данные и создаем объекты MediaFile
        for item in data:
            media_file = MediaFile(
                id=int(item["id"]),
                name_music=item["name_music"],
                description=item["description"],
                file_name=item["file_name"] if item["file_name"] else None,
                file_path=item["file_path"] if item["file_path"] else None,
                cover_image_path=item["cover_image_path"] if item["cover_image_path"] else None,
                category_id=int(item["category_id"]) if item["category_id"] else None,
                genre_id=int(item["genre_id"]) if item["genre_id"] else None,
                youtube_url=item["youtube_url"] if item["youtube_url"] else None,
                rutube_url=item["rutube_url"] if item["rutube_url"] else None,
                plvideo_url=item["plvideo_url"] if item["plvideo_url"] else None
            )
            # Добавляем объект в сессию
            session.add(media_file)
        
        # Сохраняем изменения
        session.commit()
        print("Данные успешно записаны в базу данных.")

    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка при записи данных: {e}")
    
    finally:
        # Закрываем сессию
        session.close()

# Основной блок программы
if __name__ == "__main__":
    # Загружаем данные из файла JSON
    data = load_data_from_json(json_file_path)

    # Сохраняем данные в базу данных
    save_data_to_db(data)



'''
📔 Автор: Дуплей Максим Игоревич | Dupley Maxim Igorevich
📲 Номер телефона: +7-915-048-02-49
📅 Дата: 19.10.2024
'''
