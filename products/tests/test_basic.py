import pytest
from products.models import Product, Category


@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(
        name="Electronics",
        description="Electronics items"
    )

    product = Product.objects.create(
        category=category,
        name="Laptop",
        description="Laptop",
        price=1000,
        stock=5,
        is_active=True
    )

    assert Product.objects.count() == 1
    assert product.name == "Laptop"
    assert product.price == 1000
    assert product.stock == 5
    assert product.category == category