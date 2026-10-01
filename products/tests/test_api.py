from itertools import product

import pytest
from rest_framework.test import APIClient
from products.models import Category, Product 
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_get_products() :
    category = Category.objects.create(
        name="Electronics"
    )

    Product.objects.create(
        category=category,
        name="Laptop",
        description="Gaming laptop",
        price=1000,
        stock=5
    )

    client = APIClient() 

    response = client.get("/api/products/products")

    assert response.status_code == 200 
    print(response.data)

@pytest.mark.django_db
def test_anonymous_user_cannot_create_product() :
    category = Category.objects.create(
        name="Electronics"
    )

    client = APIClient() 
    data = {
        "category": category.id,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": "1000.00",
        "stock": 5
    } 

    response = client.post("/api/products/products",data,format="json")
    assert response.status_code in [401,403]
    assert Product.objects.count() == 0

@pytest.mark.django_db
def test_normal_user_cannot_create_product():
    category = Category.objects.create(
        name="Electronics"
    )

    user = User.objects.create_user(
        username="testuser",
        password="testpassword"
    )

    client = APIClient()
    client.force_authenticate(user=user) 

    data = {
        "category": category.id,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": "1000.00",
        "stock": 5
    }

    response = client.post("/api/products/products",data,format="json")

    assert response.status_code == 403
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_admin_can_create_product():
    category = Category.objects.create(
        name="Electronics"
    )

    user = User.objects.create_user(
        username="testuser",
        password="testpassword",
        is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=user) 

    data = {
        "category": category.id,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": "1000.00",
        "stock": 5
    }

    response = client.post("/api/products/products",data,format="json")

    assert response.status_code == 201 
    assert Product.objects.count() == 1 

    product = Product.objects.get()

    assert product.name == "Laptop"
    assert product.category == category
    assert product.price == 1000
    assert product.stock == 5

@pytest.mark.django_db
def test_admin_cannot_create_product_with_invalid_data():
    admin = User.objects.create_user(
        username="admin",
        password="testpassword",
        is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": "1000.00",
        "stock": 5
    }

    response = client.post("/api/products/products",data,format="json")
    assert response.status_code == 400
    assert "category" in response.data
    assert Product.objects.count() == 0

@pytest.mark.django_db
def test_get_product_detail():
    category = Category.objects.create(
        name="Electronics"
    )

    product = Product.objects.create(
        category=category,
        name="Laptop",
        description="Gaming laptop",
        price=1000,
        stock=5
    )

    client = APIClient()

    response = client.get(f"/api/products/products/{product.id}")

    assert response.status_code == 200
    assert response.data["name"] == "Laptop"

@pytest.mark.django_db
def test_get_non_existing_product_returns_404():
    client = APIClient()

    response = client.get(
        "/api/products/products/99999/"
    )

    assert response.status_code == 404

@pytest.mark.django_db
def test_normal_user_cannot_update_product():
    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Laptop",
        price=1000,
        stock=5
    )

    user = User.objects.create_user(
        username="testuser",
        password="testpassword"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch(
        f"/api/products/{product.id}/",
        {"price": "800.00"},
        format="json"
    )
    assert response.status_code == 404
#لأن product كائن موجود أصلاً في ذاكرة Python. نحن نريد إعادة تحميل حالته الفعلية من PostgreSQL بعد الـ request.
    product.refresh_from_db()

    assert product.price == 1000


@pytest.mark.django_db
def test_admin_can_update_product():
    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Laptop",
        price=1000,
        stock=5
    )

    admin = User.objects.create_user(
            username="admin",
            password="testpassword",
            is_staff=True
        )


    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.patch(
        f"/api/products/products/{product.id}",
        {
            "price": "800.00",
            "stock": 10
        },
        format="json"
    )

    assert response.status_code == 200

    product.refresh_from_db()

    assert product.price == 800
    assert product.stock == 10

@pytest.mark.django_db
def test_normal_user_cannot_delete_product():
    category = Category.objects.create(
        name="Electronics"
    )

    product = Product.objects.create(
        category=category,
        name="Laptop",
        price=1000,
        stock=5
    )

    user = User.objects.create_user(
        username="testuser",
        password="testpassword"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(
        f"/api/products/products/{product.id}")

    assert response.status_code == 403 
    assert Product.objects.filter(id=product.id).exists() is True 


@pytest.mark.django_db
def test_admin_can_delete_product():
    category = Category.objects.create(
        name="Electronics"
    )

    product = Product.objects.create(
        category=category,
        name="Laptop",
        price=1000,
        stock=5
    )

    admin = User.objects.create_user(
        username="admin",
        password="testpassword",
        is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.delete(
        f"/api/products/products/{product.id}"
    )

    assert response.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()