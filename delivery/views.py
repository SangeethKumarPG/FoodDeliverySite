from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem, Review
from .forms import UserRegistrationForm, LoginForm, OrderForm, ReviewForm

def home(request):
    return render(request, 'home.html')

def menu(request):
    categories = Category.objects.all()
    return render(request, 'menu.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = category.items.all()
    return render(request, 'category_detail.html', {'category': category, 'items': items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def help_view(request):
    return render(request, 'help.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{item.name} added to cart.")
    return redirect('cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('menu')
    
    total_amount = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=item.item,
                    quantity=item.quantity,
                    price=item.item.price
                )
            cart.items.all().delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_success')
    else:
        form = OrderForm()
    
    return render(request, 'checkout.html', {'form': form, 'total_amount': total_amount})

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    return render(request, 'reviews.html', {'reviews': reviews, 'form': form})

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted successfully!")
    return redirect('reviews')
