import csv
import random
import sys
import timeit
from BTrees.OOBTree import OOBTree

CSV_FILE = "generated_items_data.csv"

def generate_csv_file(file_path, num_items=1000):
    """
    Створює (або перезаписує) CSV‑файл із даними про товари.
    Кожен рядок містить: ID, Name, Category, Price.
    """
    fieldnames = ["ID", "Name", "Category", "Price"]
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]

    with open(file_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, num_items + 1):
            item = {
                "ID": i,
                "Name": f"Product {i}",
                "Category": random.choice(categories),
                "Price": round(random.uniform(10.0, 200.0), 2)
            }
            writer.writerow(item)

def load_data(file_path):
    """
    Завантажує дані про товари з CSV‑файлу.
    """
    items = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append(row)
    return items

def add_item_to_tree(tree, item):
    """
    Додає товар до OOBTree, використовуючи кортеж (Price, ID) як ключ.
    """
    key = (float(item['Price']), int(item['ID']))
    tree[key] = item

def add_item_to_dict(dict_structure, item):
    """
    Додає товар до словника, використовуючи ID як ключ.
    """
    key = int(item['ID'])
    dict_structure[key] = item

def range_query_tree(tree, min_price, max_price):
    """
    Повертає список пар (ключ, товар) із OOBTree,
    де ціна товару знаходиться у межах [min_price, max_price].
    Використовуємо метод items(lower, upper) для швидкого доступу.
    """
    lower_key = (min_price, -sys.maxsize)
    upper_key = (max_price, sys.maxsize)
    return list(tree.items(lower_key, upper_key))

def range_query_dict(dict_structure, min_price, max_price):
    """
    Повертає список товарів із словника, де ціна знаходиться
    у заданому діапазоні. Реалізовано лінійним перебором.
    """
    return [
        item
        for item in dict_structure.values()
        if min_price <= float(item['Price']) <= max_price
    ]

def main():
    # Генеруємо CSV‑файл (перезаписуючи існуючий)
    generate_csv_file(CSV_FILE, num_items=1000)

    # Завантаження даних із CSV‑файлу
    data = load_data(CSV_FILE)

    # Ініціалізація структур даних
    tree = OOBTree()
    dict_structure = {}

    # Додавання товарів до обох структур
    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dict_structure, item)

    # Визначаємо діапазон для запиту за ціною (наприклад, від 50 до 150)
    min_query_price = 50.0
    max_query_price = 150.0

    # Вимірювання часу виконання 100 діапазонних запитів для OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_query_price, max_query_price),
        number=100
    )

    # Вимірювання часу виконання 100 діапазонних запитів для Dict (лінійний пошук)
    dict_time = timeit.timeit(
        lambda: range_query_dict(dict_structure, min_query_price, max_query_price),
        number=100
    )

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()