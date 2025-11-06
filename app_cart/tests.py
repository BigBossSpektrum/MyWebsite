from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from app_products.models import Product, Category
from .models import Cart, CartItem
from decimal import Decimal

User = get_user_model()


class CartModelTest(TestCase):
    """Tests para el modelo Cart"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.cart = Cart.objects.create(user=self.user)
        
        # Crear categoría y productos de prueba
        self.category = Category.objects.create(name='Test Category')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Product 1',
            description='Test product 1',
            price=Decimal('10.00'),
            stock=100
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Product 2',
            description='Test product 2',
            price=Decimal('20.00'),
            stock=50
        )
    
    def test_cart_creation(self):
        """Test crear un carrito"""
        self.assertEqual(self.cart.user, self.user)
        self.assertIsNotNone(self.cart.id)
    
    def test_cart_get_total_empty(self):
        """Test obtener total de carrito vacío"""
        self.assertEqual(self.cart.get_total(), 0)
    
    def test_cart_get_total_with_items(self):
        """Test obtener total de carrito con items"""
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        expected_total = (self.product1.price * 2) + (self.product2.price * 1)
        self.assertEqual(self.cart.get_total(), expected_total)
    
    def test_cart_get_total_items(self):
        """Test obtener cantidad total de items"""
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)
        self.assertEqual(self.cart.get_total_items(), 5)
    
    def test_cart_clear(self):
        """Test limpiar carrito"""
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        self.cart.clear()
        self.assertEqual(self.cart.items.count(), 0)


class CartItemModelTest(TestCase):
    """Tests para el modelo CartItem"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test product',
            price=Decimal('15.00'),
            stock=10
        )
    
    def test_cart_item_creation(self):
        """Test crear un item del carrito"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
    
    def test_cart_item_get_subtotal(self):
        """Test calcular subtotal del item"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3
        )
        expected_subtotal = self.product.price * 3
        self.assertEqual(item.get_subtotal(), expected_subtotal)
    
    def test_cart_item_unique_together(self):
        """Test restricción unique_together"""
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        with self.assertRaises(Exception):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)


class CartViewTest(TestCase):
    """Tests para las vistas del carrito (CRUD)"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test product',
            price=Decimal('25.00'),
            stock=50
        )
    
    def test_cart_view_anonymous(self):
        """Test ver carrito como usuario anónimo"""
        response = self.client.get(reverse('cart:cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.context)
    
    def test_cart_view_authenticated(self):
        """Test ver carrito como usuario autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cart:cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.context)
    
    def test_add_to_cart(self):
        """Test CREATE - agregar producto al carrito"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
    
    def test_update_cart(self):
        """Test UPDATE - actualizar cantidad en el carrito"""
        self.client.login(username='testuser', password='testpass123')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        response = self.client.post(
            reverse('cart:update_cart', kwargs={'product_id': self.product.id}),
            {'quantity': 5}
        )
        self.assertEqual(response.status_code, 302)
        
        item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(item.quantity, 5)
    
    def test_remove_from_cart(self):
        """Test DELETE - eliminar producto del carrito"""
        self.client.login(username='testuser', password='testpass123')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.post(
            reverse('cart:remove_from_cart', kwargs={'product_id': self.product.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)
    
    def test_clear_cart(self):
        """Test DELETE - limpiar todo el carrito"""
        self.client.login(username='testuser', password='testpass123')
        cart = Cart.objects.create(user=self.user)
        
        product2 = Product.objects.create(
            category=self.category,
            name='Product 2',
            description='Test',
            price=Decimal('30.00'),
            stock=20
        )
        
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=cart, product=product2, quantity=2)
        
        response = self.client.post(reverse('cart:clear_cart'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)
    
    def test_add_to_cart_insufficient_stock(self):
        """Test agregar producto con stock insuficiente"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}),
            {'quantity': 100}  # Más que el stock disponible (50)
        )
        # Debe redirigir con mensaje de error
        self.assertEqual(response.status_code, 302)
