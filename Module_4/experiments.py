
# from PIL import Image, ImageOps
# import os

# # Пути к папкам
# input_folder = 'dataset_kubiki'  # Папка с исходными изображениями
# output_folder = 'inverted_kubiki'  # Папка для инвертированных изображений

# # Создаем папку для результатов, если её нет
# os.makedirs(output_folder, exist_ok=True)

# # Ограничиваем обработку 50 изображениями
# max_images = 50
# processed = 0

# # Перебираем файлы в папке
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith('.jpg'):
#         # Открываем изображение
#         img_path = os.path.join(input_folder, filename)
#         with Image.open(img_path) as img:
#             # Инвертируем цвета
#             inverted_img = ImageOps.invert(img.convert('RGB'))
            
#             # Сохраняем в новую папку
#             output_path = os.path.join(output_folder, filename)
#             inverted_img.save(output_path, 'JPEG')
            
#             processed += 1
#             print(f"Обработано: {filename}")
            
#             # Прекращаем после 50 изображений
#             if processed >= max_images:
#                 break

# print(f"Готово! Обработано {processed} изображений.")




# from PIL import Image, ImageEnhance, ImageOps
# import os
# import random

# input_folder = 'inverted_kubiki'
# output_folder = 'modified_kubiki'

# os.makedirs(output_folder, exist_ok=True)

# def modify_image(img):
#     """Применяет случайные модификации к изображению"""
#     if img is None:
#         return None

#     # Поворот
#     if random.choice([True, False]):
#         angle = random.choice([0, 90, 180, 270])
#         img = img.rotate(angle, expand=True)
    
#     # Зеркальное отражение
#     if random.choice([True, False]):
#         if random.choice([True, False]):
#             img = ImageOps.mirror(img)
#         else:
#             img = ImageOps.flip(img)
    
#     # Яркость
#     if random.choice([True, False]):
#         enhancer = ImageEnhance.Brightness(img)
#         factor = random.uniform(0.7, 1.3)
#         img = enhancer.enhance(factor)
    
#     return img

# for filename in os.listdir(input_folder):
#     if filename.lower().endswith('.jpg'):
#         img_path = os.path.join(input_folder, filename)
#         try:
#             with Image.open(img_path) as img:
#                 modified_img = modify_image(img)
#                 if modified_img is not None:
#                     output_path = os.path.join(output_folder, filename)
#                     modified_img.save(output_path, 'JPEG', quality=95)
#                     print(f"Успешно: {filename}")
#                 else:
#                     print(f"Ошибка: {filename} (не удалось обработать)")
#         except Exception as e:
#             print(f"Ошибка при обработке {filename}: {e}")

# print("Готово! Проверьте папку", output_folder)



import os
import random

def shuffle_with_prefix(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    random.shuffle(files)
    
    # Добавляем временный префикс
    for filename in files:
        old_path = os.path.join(directory, filename)
        temp_path = os.path.join(directory, f"_temp_{filename}")
        os.rename(old_path, temp_path)
    
    # Убираем префикс и даем новые имена
    temp_files = [f for f in os.listdir(directory) if f.startswith('_temp_')]
    for index, filename in enumerate(temp_files, start=1):
        new_name = f"{index:03d}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
    
    print("Файлы перемешаны!")

folder_path = "dataset_kubiki"
shuffle_with_prefix(folder_path)