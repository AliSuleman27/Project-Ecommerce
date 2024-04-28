from .models import Product
from category.models import Category
import os
import pandas as pd
def feed_categories():
    # Get the base directory of your Django project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the absolute file path to the CSV file
    csv_file_path = os.path.join(base_dir, 'data', 'category.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Print the category names
    print(df['category_name'])

    category_name = df['category_name']
    category_description = df['category_description']

    for i in range(len(category_name)):
        object = Category.objects.create(category_name=category_name[i],description=category_description[i])
        object.save()

def feed_products():
    # Get the base directory of your Django project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the absolute file path to the CSV file
    csv_file_path = os.path.join(base_dir, 'data', 'product_book.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(df['name'])
    # sno,name,description,price,stock,is_available,Category ID,GPU,IPS,OS,processor,ram,storage,touchscreen,company,resolution,weight

    name = df['name']
    description = df['description']
    price = df['price']
    stock = df['stock']
    is_available = df['is_available']
    category_id = df['Category ID']
    GPU = df['GPU']
    IPS = df['IPS']
    OS = df['OS']
    processor = df['processor']
    ram = df['ram']
    storage = df['storage']
    touchscreen = df['touchscreen']
    resolution = df['resolution']
    company = df['company']
    weight = df['weight']

    for i in range(len(name)):
        object = Product.objects.create(
        product_name=name[i],        
        description=description[i],
        company=company[i],
        ram=int(ram[i]),
        storage=storage[i],
        resolution=resolution[i],
        processer=processor[i],
        GPU=GPU[i],
        OS=OS[i],
        weight=float(weight[i]),
        touchscreen= bool(touchscreen[i]),
        IPS = bool(IPS[i]),
        price=price[i],
        stock=stock[i],
        is_available=bool(is_available[i]),
        category=Category.objects.get(id=category_id[i]-1),
        )
        object.save()
        print(f"Added {name[i]} successfully ")





