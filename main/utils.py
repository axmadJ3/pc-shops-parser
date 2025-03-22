from .parsers.asaxiy_parser import parse_asaxiy
from .parsers.glotr_parser import parse_glotr
from .parsers.mediapark_parser import parse_mediapark
from .parsers.zoodmall_parser import parse_zoodmall
from .services.product_service import save_products_to_db


def run_asaxiy_parser():
    print("Запуск парсера Asaxiy")
    products = parse_asaxiy()
    save_products_to_db(products)


def run_glotr_parser():
    print("Запуск парсера Glotr")
    products = parse_glotr()
    save_products_to_db(products)


def run_mediapark_parser():
    print("Запуск парсера Mediapark")
    products = parse_mediapark()
    save_products_to_db(products)


def run_zoodmall_parser():
    print("Запуск парсера Mediapark")
    products = parse_zoodmall()
    save_products_to_db(products)
