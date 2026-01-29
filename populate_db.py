import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'savourelle_project.settings')
django.setup()

from delivery.models import Category, MenuItem

def populate():
    categories_data = [
        {'name': 'Fast Food', 'image_url': 'https://t3.ftcdn.net/jpg/06/97/50/64/360_F_697506405_cw8A20AX7Yt0S7IhShHZ7DDgkbMkCNOh.jpg'},
        {'name': 'Breakfast', 'image_url': 'https://www.shutterstock.com/image-photo/side-view-isometric-angle-crispy-600nw-2600398075.jpg'},
        {'name': 'Main Course', 'image_url': 'https://img.freepik.com/premium-photo/chicken-biryani-isolated-white-background_741212-2174.jpg'},
        {'name': 'Appetizers', 'image_url': 'https://img.freepik.com/premium-photo/restaurant-menu-dish-traditional-restaurant-serving-appetizer-white-background-isolated-top-view_96064-1033.jpg'},
        {'name': 'Desserts', 'image_url': 'https://media.istockphoto.com/id/500362775/photo/tiramisu-dessert.jpg?s=612x612&w=0&k=20&c=lWH9PvaN77Oi-aBd5szdOo2hK2RBTbdi_6HY8ExCfjg='},
        {'name': 'Cakes', 'image_url': 'https://thumbs.dreamstime.com/b/black-forest-cake-recipe-against-transparent-background-dried-apricots-sweet-healthy-384251305.jpg'},
        {'name': 'Ice Cream', 'image_url': 'https://img.freepik.com/premium-photo/ice-cream-with-white-background-high-quality-ultra_670382-88894.jpg'},
    ]

    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(name=cat_data['name'])
        category.image = cat_data['image_url']
        category.save()
        
        # Add some items to each category
        if cat_data['name'] == 'Fast Food':
            MenuItem.objects.get_or_create(category=category, name='Cheese Burst Pizza', description='The ultimate cheesy experience.', price=12.99, image='https://images.unsplash.com/photo-1606756790138-8f02d5f5f88c?auto=format&fit=crop&w=800&q=80')
            MenuItem.objects.get_or_create(category=category, name='Classic Chicken Burger', description='Juicy chicken patty with fresh veggies.', price=8.50, image='https://t3.ftcdn.net/jpg/06/97/50/64/360_F_697506405_cw8A20AX7Yt0S7IhShHZ7DDgkbMkCNOh.jpg')
        elif cat_data['name'] == 'Breakfast':
            MenuItem.objects.get_or_create(category=category, name='Pancakes', description='Fluffy pancakes with maple syrup.', price=7.50, image='https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=400&q=80')
        elif cat_data['name'] == 'Main Course':
            MenuItem.objects.get_or_create(category=category, name='Chicken Biryani', description='Fragrant rice cooked with spiced chicken.', price=15.00, image='https://img.freepik.com/premium-photo/chicken-biryani-isolated-white-background_741212-2174.jpg')
        elif cat_data['name'] == 'Appetizers':
            MenuItem.objects.get_or_create(category=category, name='Spring Rolls', description='Crispy rolls filled with vegetables.', price=6.00, image='https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80')
        elif cat_data['name'] == 'Desserts':
            MenuItem.objects.get_or_create(category=category, name='Tiramisu', description='Classic Italian dessert.', price=7.00, image='https://media.istockphoto.com/id/500362775/photo/tiramisu-dessert.jpg?s=612x612&w=0&k=20&c=lWH9PvaN77Oi-aBd5szdOo2hK2RBTbdi_6HY8ExCfjg=')
        elif cat_data['name'] == 'Cakes':
            MenuItem.objects.get_or_create(category=category, name='Black Forest', description='Rich chocolate cake with cherries.', price=25.00, image='https://thumbs.dreamstime.com/b/black-forest-cake-recipe-against-transparent-background-dried-apricots-sweet-healthy-384251305.jpg')
        elif cat_data['name'] == 'Ice Cream':
            MenuItem.objects.get_or_create(category=category, name='Vanilla Scoop', description='Creamy vanilla ice cream.', price=4.00, image='https://img.freepik.com/premium-photo/ice-cream-with-white-background-high-quality-ultra_670382-88894.jpg')

    print("Database populated successfully!")

if __name__ == "__main__":
    populate()
