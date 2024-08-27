import json
from django.core.management.base import BaseCommand
from myproject.catalog.models import Category, Product

class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('your_app_name/fixtures/your_app_name_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('categories', [])

    @staticmethod
    def json_read_products():
        with open('your_app_name/fixtures/your_app_name_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('products', [])

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    name=category['fields']['name'],
                    description=category['fields']['description']
                )
            )

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    image=product['fields']['image'],
                    category=Category.objects.get(pk=product['fields']['category']),
                    price=product['fields']['price'],
                    created_at=product['fields']['created_at'],
                    updated_at=product['fields']['updated_at'],
                    manufactured_at=product['fields']['manufactured_at']
                )
            )

        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
