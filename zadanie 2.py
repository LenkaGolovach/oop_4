#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import logging
from datetime import datetime

# Настройка логгирования
logging.basicConfig(
    filename='program.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_shop(shops, name, product, price):
    shops.append({
        'name': name,
        'product': product,
        'price': price,
    })
    logging.info(f"Добавлен магазин: {name}, товар: {product}, цена: {price}")
    return shops

def display_shops(shops):
    if shops:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 8,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Название магазина",
                "Товар",
                "Цена"
            )
        )
        print(line)
        for idx, shop in enumerate(sorted(shops, key=lambda x: x['name']), 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    shop.get('name', ''),
                    shop.get('product', ''),
                    shop.get('price', 0)
                )
            )
            print(line)
    else:
        print("Список магазинов пуст.")

def select_shops(shops, name):
    found = False
    for shop in shops:
        if shop.get('name') == name:
            found = True
            print(
                'Товар: {:<20} Цена: {:<8}'.format(
                    shop.get('product', ''),
                    shop.get('price', 0),
                )
            )
    if not found:
        print("Такого магазина нет.")

def save_shops(file_name, shops):
    try:
        with open(file_name, "w", encoding="utf-8") as fout:
            json.dump(shops, fout, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в файл {file_name}.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных: {e}")

def load_shops(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    except FileNotFoundError:
        logging.error(f"Файл {file_name} не найден. Будет создан новый файл.")
        return []
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных из файла {file_name}: {e}")
        return []

def main(command_line=None):
    parser = argparse.ArgumentParser("shops")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="The data file name")

    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new product")
    add.add_argument("-n", "--name", action="store", required=True, help="The shop's name")
    add.add_argument("-p", "--product", action="store", required=True, help="The shop's product")
    add.add_argument("-pr", "--price", action="store", type=float, required=True, help="The price of product")

    display = subparsers.add_parser("display", parents=[file_parser], help="Display all shops")

    select = subparsers.add_parser("select", parents=[file_parser], help="Select the shops")
    select.add_argument("-s", "--shop", required=True, help="The selected shop")

    args = parser.parse_args(command_line)

    is_dirty = False
    shops = load_shops(args.filename) if os.path.exists(args.filename) else []

    if args.command == "add":
        get_shop(shops, args.name, args.product, args.price)
        is_dirty = True
    elif args.command == "display":
        display_shops(shops)
    elif args.command == "select":
        select_shops(shops, args.shop)

    if is_dirty:
        save_shops(args.filename, shops)

if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    logging.info(f"Выполнение команды завершено. Время выполнения: {end_time - start_time}")
