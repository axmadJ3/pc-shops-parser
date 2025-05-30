from project.celery import shared_task

from .parsers.asaxiy_parser import parse_asaxiy
from .parsers.glotr_parser import parse_glotr
from .parsers.mediapark_parser import parse_mediapark
from .parsers.noutuz_parser import parse_noutuz
from .parsers.zoodmall_parser import parse_zoodmall
from .services.product_service import save_products_to_db


@shared_task
def run_asaxiy_parser():
    print("Запуск парсера Asaxiy")
    products = parse_asaxiy()
    save_products_to_db(products)

@shared_task
def run_glotr_parser():
    print("Запуск парсера Glotr")
    products = parse_glotr()
    save_products_to_db(products)


@shared_task
def run_mediapark_parser():
    print("Запуск парсера Mediapark")
    products = parse_mediapark()
    save_products_to_db(products)


@shared_task
def run_zoodmall_parser():
    print("Запуск парсера Mediapark")
    products = parse_zoodmall()
    save_products_to_db(products)


@shared_task
def run_noutuz_parser():
    print("Запуск парсера Mediapark")
    products = parse_noutuz()
    save_products_to_db(products)
