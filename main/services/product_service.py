import logging

from django.db import transaction

from main.models import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_products_to_db(parsed_products):
    if not parsed_products:
        logger.info("Нет данных для сохранения.")
        return

    logger.info(f"Обработка {len(parsed_products)} товаров...")

    existing_products = Product.objects.filter(
        site__in={p.site for p in parsed_products},
        name__in={p.name for p in parsed_products}
    )
    existing_lookup = {(p.site, p.name): p for p in existing_products}

    products_to_create = []
    products_to_update = []

    for pdata in parsed_products:
        key = (pdata.site, pdata.name)
        existing = existing_lookup.get(key)

        if existing:
            updated = False
            if existing.price != pdata.price:
                existing.price = pdata.price
                updated = True
            if existing.url != pdata.url:
                existing.url = pdata.url
                updated = True
            if existing.image_url != pdata.image_url:
                existing.image_url = pdata.image_url
                updated = True

            if updated:
                products_to_update.append(existing)
        else:
            products_to_create.append(Product(
                site=pdata.site,
                name=pdata.name,
                price=pdata.price,
                url=pdata.url,
                image_url=pdata.image_url
            ))

    with transaction.atomic():
        if products_to_create:
            Product.objects.bulk_create(products_to_create, batch_size=1000)
            logger.info(f"Создано товаров: {len(products_to_create)}")

        if products_to_update:
            Product.objects.bulk_update(products_to_update, ['price', 'url', 'image_url'], batch_size=1000)
            logger.info(f"Обновлено товаров: {len(products_to_update)}")

    logger.info("Сохранение в БД завершено.")
