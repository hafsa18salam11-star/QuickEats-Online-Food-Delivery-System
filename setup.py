"""
QuickEats — MongoDB Setup Script
Creates all 6 collections: Users, Restaurant, Menu, Orders, Order_items, Payment
Run ONCE before starting the app.

Usage:  python setup.py
"""
import sys, os

print("="*55)
print("  ⚡ QuickEats — MongoDB Setup")
print("="*55)

# Install packages if missing
for pkg in ['pymongo','flask']:
    try:
        __import__(pkg)
        print(f"  ✅ {pkg} ready")
    except ImportError:
        print(f"  📦 Installing {pkg}...")
        os.system(f"{sys.executable} -m pip install {pkg}")
        print(f"  ✅ {pkg} installed")

from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "quickeats"

print("\n  🔌 Connecting to MongoDB...")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
    client.server_info()
    print("  ✅ Connected!\n")
except Exception as e:
    print(f"\n  ❌ Cannot connect: {e}")
    print("\n  Fix: Open CMD as Administrator and run:")
    print("       net start MongoDB")
    input("\n  Press Enter to exit...")
    sys.exit(1)

db = client[DB_NAME]

# ── Drop existing collections for clean seed ──────────────────
for col in ['Restaurant','Menu','Orders','Order_items','Payment']:
    db[col].drop()
print("  🗑️  Old data cleared")

# ══════════════════════════════════════════════════════════════
# 1. RESTAURANT collection
# ══════════════════════════════════════════════════════════════
print("\n  🏪 Seeding Restaurant collection...")
restaurants = [
    {"restaurant_id":"R001","name":"Pizza Hub","location":"Karachi","cuisine":"Pizza & Italian","rating":4.5,"reviews":842,"delivery_time":"25-35","min_order":500,"emoji":"🍕","gradient":"linear-gradient(135deg,#ff6b6b,#ee0979)","is_popular":True,"is_open":True,"categories":["pizza"]},
    {"restaurant_id":"R002","name":"Burger Town","location":"Lahore","cuisine":"Burgers & Grills","rating":4.3,"reviews":621,"delivery_time":"20-30","min_order":300,"emoji":"🍔","gradient":"linear-gradient(135deg,#f7971e,#ffd200)","is_popular":False,"is_open":True,"categories":["burgers"]},
    {"restaurant_id":"R003","name":"Pizza Town","location":"Sukkur","cuisine":"Pizza & Pasta","rating":4.1,"reviews":389,"delivery_time":"30-40","min_order":500,"emoji":"🍕","gradient":"linear-gradient(135deg,#ff512f,#dd2476)","is_popular":False,"is_open":True,"categories":["pizza"]},
    {"restaurant_id":"R004","name":"Food Street","location":"Karachi","cuisine":"Pakistani & Desi","rating":4.6,"reviews":1204,"delivery_time":"15-25","min_order":200,"emoji":"🍛","gradient":"linear-gradient(135deg,#e65c00,#f9d423)","is_popular":True,"is_open":True,"categories":["desi"]},
    {"restaurant_id":"R005","name":"Tandoori House","location":"Multan","cuisine":"Desi Cuisine","rating":4.4,"reviews":755,"delivery_time":"25-35","min_order":300,"emoji":"🍗","gradient":"linear-gradient(135deg,#d4145a,#fbb03b)","is_popular":False,"is_open":True,"categories":["desi"]},
    {"restaurant_id":"R006","name":"BBQ Nation","location":"Lahore","cuisine":"BBQ & Grills","rating":4.7,"reviews":1580,"delivery_time":"30-45","min_order":800,"emoji":"🔥","gradient":"linear-gradient(135deg,#1a1a2e,#e63946)","is_popular":True,"is_open":True,"categories":["bbq"]},
    {"restaurant_id":"R007","name":"Asian Wok","location":"Islamabad","cuisine":"Chinese & Thai","rating":4.2,"reviews":467,"delivery_time":"25-35","min_order":400,"emoji":"🍜","gradient":"linear-gradient(135deg,#4facfe,#00f2fe)","is_popular":False,"is_open":True,"categories":["chinese"]},
    {"restaurant_id":"R008","name":"Street Bite","location":"Karachi","cuisine":"Fast Food & Snacks","rating":4.0,"reviews":312,"delivery_time":"15-25","min_order":200,"emoji":"🥪","gradient":"linear-gradient(135deg,#43e97b,#38f9d7)","is_popular":False,"is_open":True,"categories":["snacks"]},
    {"restaurant_id":"R009","name":"Desi Grill","location":"Khairpur","cuisine":"Desi & BBQ","rating":4.3,"reviews":544,"delivery_time":"20-30","min_order":300,"emoji":"🍖","gradient":"linear-gradient(135deg,#f093fb,#f5576c)","is_popular":False,"is_open":True,"categories":["desi","bbq"]},
    {"restaurant_id":"R010","name":"Royal Kitchen","location":"Peshawar","cuisine":"Peshawari Cuisine","rating":4.5,"reviews":933,"delivery_time":"25-40","min_order":400,"emoji":"👑","gradient":"linear-gradient(135deg,#667eea,#764ba2)","is_popular":True,"is_open":True,"categories":["desi"]},
    {"restaurant_id":"R011","name":"Noodle House","location":"Karachi","cuisine":"Chinese & Noodles","rating":4.1,"reviews":290,"delivery_time":"20-30","min_order":350,"emoji":"🍜","gradient":"linear-gradient(135deg,#f8574b,#ffb03a)","is_popular":False,"is_open":True,"categories":["chinese"]},
    {"restaurant_id":"R012","name":"Sweet Cravings","location":"Lahore","cuisine":"Desserts & Beverages","rating":4.6,"reviews":728,"delivery_time":"15-25","min_order":150,"emoji":"🧁","gradient":"linear-gradient(135deg,#ff9a9e,#fad0c4)","is_popular":True,"is_open":True,"categories":["desserts"]},
]
db.Restaurant.insert_many(restaurants)
db.Restaurant.create_index("restaurant_id", unique=True)
db.Restaurant.create_index("is_popular")
print(f"  ✅ {len(restaurants)} restaurants inserted")

# ══════════════════════════════════════════════════════════════
# 2. MENU collection
# ══════════════════════════════════════════════════════════════
print("\n  🍽️  Seeding Menu collection...")
menu_items = [
    # Pizza Hub R001
    {"restaurant_id":"R001","item_id":"M001","item_name":"Pepperoni Pizza","description":"Double pepperoni on classic tomato sauce with mozzarella","price":1200,"category":"Pizza","emoji":"🍕","is_available":True},
    {"restaurant_id":"R001","item_id":"M002","item_name":"Cheese Pizza","description":"Three-cheese blend: mozzarella, cheddar and parmesan","price":1000,"category":"Pizza","emoji":"🧀","is_available":True},
    {"restaurant_id":"R001","item_id":"M003","item_name":"BBQ Chicken Pizza","description":"Smoky BBQ sauce with grilled chicken and caramelized onions","price":1300,"category":"Pizza","emoji":"🍕","is_available":True},
    {"restaurant_id":"R001","item_id":"M004","item_name":"Garlic Bread","description":"Toasted ciabatta with garlic butter and fresh herbs","price":320,"category":"Sides","emoji":"🍞","is_available":True},
    {"restaurant_id":"R001","item_id":"M005","item_name":"Chicken Wings","description":"Crispy wings in buffalo or BBQ sauce — 8 pieces","price":750,"category":"Starters","emoji":"🍗","is_available":True},
    {"restaurant_id":"R001","item_id":"M006","item_name":"Coleslaw","description":"Creamy house-made coleslaw with fresh herbs","price":180,"category":"Sides","emoji":"🥗","is_available":True},
    # Burger Town R002
    {"restaurant_id":"R002","item_id":"M007","item_name":"Zinger Burger","description":"Crispy spiced chicken fillet with special sauce and lettuce","price":450,"category":"Burgers","emoji":"🍔","is_available":True},
    {"restaurant_id":"R002","item_id":"M008","item_name":"Beef Burger","description":"100% beef patty with lettuce, tomato and pickles","price":500,"category":"Burgers","emoji":"🍔","is_available":True},
    {"restaurant_id":"R002","item_id":"M009","item_name":"Double Smash Burger","description":"Two smashed beef patties with cheese and special sauce","price":750,"category":"Burgers","emoji":"🍔","is_available":True},
    {"restaurant_id":"R002","item_id":"M010","item_name":"Crispy Chicken Burger","description":"Golden crispy chicken with creamy mayo and coleslaw","price":520,"category":"Burgers","emoji":"🍔","is_available":True},
    {"restaurant_id":"R002","item_id":"M011","item_name":"Loaded Fries","description":"Fries topped with cheese sauce, jalapenos and crispy chicken","price":350,"category":"Sides","emoji":"🍟","is_available":True},
    {"restaurant_id":"R002","item_id":"M012","item_name":"Chocolate Shake","description":"Thick creamy chocolate milkshake","price":280,"category":"Drinks","emoji":"🥤","is_available":True},
    # Pizza Town R003
    {"restaurant_id":"R003","item_id":"M013","item_name":"Chicken Karahi","description":"Tender chicken in spiced tomato gravy — serves 2","price":900,"category":"Main","emoji":"🍛","is_available":True},
    {"restaurant_id":"R003","item_id":"M014","item_name":"Mutton Karahi","description":"Slow-cooked mutton in bold spices — serves 2","price":1500,"category":"Main","emoji":"🍛","is_available":True},
    {"restaurant_id":"R003","item_id":"M015","item_name":"Chicken Tikka Masala","description":"Marinated grilled chicken in rich creamy masala sauce","price":950,"category":"Main","emoji":"🍛","is_available":True},
    {"restaurant_id":"R003","item_id":"M016","item_name":"Garlic Naan","description":"Soft buttery naan with roasted garlic from the clay oven","price":100,"category":"Bread","emoji":"🫓","is_available":True},
    {"restaurant_id":"R003","item_id":"M017","item_name":"Raita","description":"Cool yogurt with cucumber and fresh mint","price":120,"category":"Sides","emoji":"🥛","is_available":True},
    # Food Street R004
    {"restaurant_id":"R004","item_id":"M018","item_name":"Chicken Biryani","description":"Fragrant basmati rice with spiced chicken and golden fried onions","price":350,"category":"Rice","emoji":"🍚","is_available":True},
    {"restaurant_id":"R004","item_id":"M019","item_name":"Mutton Biryani","description":"Slow-cooked mutton biryani — rich, aromatic and filling","price":450,"category":"Rice","emoji":"🍚","is_available":True},
    {"restaurant_id":"R004","item_id":"M020","item_name":"Beef Qorma","description":"Slow-braised beef in rich yogurt-based gravy","price":420,"category":"Main","emoji":"🍛","is_available":True},
    {"restaurant_id":"R004","item_id":"M021","item_name":"Daal Makhni","description":"Creamy black lentil dal slow-cooked with butter","price":300,"category":"Main","emoji":"🥣","is_available":True},
    {"restaurant_id":"R004","item_id":"M022","item_name":"Garden Salad","description":"Fresh garden salad with chaat masala and lemon dressing","price":150,"category":"Sides","emoji":"🥗","is_available":True},
    {"restaurant_id":"R004","item_id":"M023","item_name":"Lassi","description":"Chilled sweet or salty yogurt drink","price":180,"category":"Drinks","emoji":"🥛","is_available":True},
    # Tandoori House R005
    {"restaurant_id":"R005","item_id":"M024","item_name":"Nihari","description":"Slow-cooked beef stew spiced to perfection — a Lahori classic","price":380,"category":"Main","emoji":"🍲","is_available":True},
    {"restaurant_id":"R005","item_id":"M025","item_name":"Haleem","description":"Lentils and wheat slow-cooked with mutton — hearty and thick","price":320,"category":"Main","emoji":"🥣","is_available":True},
    {"restaurant_id":"R005","item_id":"M026","item_name":"Paye","description":"Traditional trotters curry cooked overnight with spices","price":420,"category":"Main","emoji":"🍲","is_available":True},
    {"restaurant_id":"R005","item_id":"M027","item_name":"Tandoori Naan","description":"Freshly baked naan from the clay tandoor","price":90,"category":"Bread","emoji":"🫓","is_available":True},
    {"restaurant_id":"R005","item_id":"M028","item_name":"Kheer","description":"Classic rice pudding with saffron and cardamom","price":200,"category":"Dessert","emoji":"🍮","is_available":True},
    # BBQ Nation R006
    {"restaurant_id":"R006","item_id":"M029","item_name":"BBQ Platter","description":"Mixed grill for 2: boti, seekh kabab, tikka and wings","price":1800,"category":"BBQ","emoji":"🔥","is_available":True},
    {"restaurant_id":"R006","item_id":"M030","item_name":"Chicken Tikka","description":"Marinated grilled chicken tikka on the bone — 6 pieces","price":650,"category":"BBQ","emoji":"🍗","is_available":True},
    {"restaurant_id":"R006","item_id":"M031","item_name":"Mutton Boti","description":"Juicy mutton boti skewers charcoal-grilled to perfection","price":850,"category":"BBQ","emoji":"🍢","is_available":True},
    {"restaurant_id":"R006","item_id":"M032","item_name":"Seekh Kabab","description":"Minced spiced beef kabab rolls — 6 pieces with naan","price":550,"category":"BBQ","emoji":"🍢","is_available":True},
    {"restaurant_id":"R006","item_id":"M033","item_name":"Roasted Corn","description":"BBQ corn on the cob with spice butter","price":120,"category":"Sides","emoji":"🌽","is_available":True},
    {"restaurant_id":"R006","item_id":"M034","item_name":"Cold Drink","description":"Chilled Pepsi, 7Up or Mirinda","price":100,"category":"Drinks","emoji":"🥤","is_available":True},
    # Asian Wok R007
    {"restaurant_id":"R007","item_id":"M035","item_name":"Chicken Chowmein","description":"Wok-fried noodles with vegetables and chicken in soy sauce","price":520,"category":"Noodles","emoji":"🍜","is_available":True},
    {"restaurant_id":"R007","item_id":"M036","item_name":"Beef Noodles","description":"Rich beef broth noodles with soft-boiled egg","price":580,"category":"Noodles","emoji":"🍜","is_available":True},
    {"restaurant_id":"R007","item_id":"M037","item_name":"Egg Fried Rice","description":"Wok-tossed egg fried rice with fresh vegetables","price":450,"category":"Rice","emoji":"🍳","is_available":True},
    {"restaurant_id":"R007","item_id":"M038","item_name":"Spring Rolls","description":"Crispy vegetable spring rolls — 4 pcs with sweet chili dip","price":320,"category":"Starters","emoji":"🥟","is_available":True},
    {"restaurant_id":"R007","item_id":"M039","item_name":"Dim Sum","description":"Steamed pork and shrimp dumplings — 6 pieces","price":380,"category":"Starters","emoji":"🥟","is_available":True},
    {"restaurant_id":"R007","item_id":"M040","item_name":"Hot & Sour Soup","description":"Classic spicy tangy soup with tofu and mushrooms","price":280,"category":"Soup","emoji":"🍲","is_available":True},
    # Street Bite R008
    {"restaurant_id":"R008","item_id":"M041","item_name":"Classic Fries","description":"Golden crispy salted fries with ketchup","price":200,"category":"Snacks","emoji":"🍟","is_available":True},
    {"restaurant_id":"R008","item_id":"M042","item_name":"Club Sandwich","description":"Triple-layer chicken club with lettuce and tomato","price":380,"category":"Sandwiches","emoji":"🥪","is_available":True},
    {"restaurant_id":"R008","item_id":"M043","item_name":"Chicken Shawarma","description":"Juicy chicken wrap with garlic sauce and pickles","price":420,"category":"Wraps","emoji":"🌯","is_available":True},
    {"restaurant_id":"R008","item_id":"M044","item_name":"Samosa (4 pcs)","description":"Crispy potato-filled fried samosas with mint chutney","price":160,"category":"Snacks","emoji":"🥟","is_available":True},
    {"restaurant_id":"R008","item_id":"M045","item_name":"Pakora Platter","description":"Mixed vegetable and chicken pakoras with mint chutney","price":250,"category":"Snacks","emoji":"🍘","is_available":True},
    {"restaurant_id":"R008","item_id":"M046","item_name":"Mango Shake","description":"Fresh thick mango milkshake","price":220,"category":"Drinks","emoji":"🥭","is_available":True},
    # Desi Grill R009
    {"restaurant_id":"R009","item_id":"M047","item_name":"Chicken Handi","description":"Creamy chicken cooked in traditional clay pot with spices","price":800,"category":"Main","emoji":"🍲","is_available":True},
    {"restaurant_id":"R009","item_id":"M048","item_name":"Daal Chawal","description":"Yellow lentil dal with steamed basmati rice","price":260,"category":"Rice","emoji":"🍚","is_available":True},
    {"restaurant_id":"R009","item_id":"M049","item_name":"Aloo Gosht","description":"Potato and slow-cooked mutton curry","price":520,"category":"Main","emoji":"🥔","is_available":True},
    {"restaurant_id":"R009","item_id":"M050","item_name":"Chicken Boti BBQ","description":"Marinated chicken boti skewers charcoal-grilled","price":680,"category":"BBQ","emoji":"🍢","is_available":True},
    {"restaurant_id":"R009","item_id":"M051","item_name":"Fresh Roti","description":"Freshly made whole-wheat roti","price":50,"category":"Bread","emoji":"🫓","is_available":True},
    # Royal Kitchen R010
    {"restaurant_id":"R010","item_id":"M052","item_name":"Peshawari Pulao","description":"Fragrant rice cooked in rich meat broth with whole spices","price":420,"category":"Rice","emoji":"🍚","is_available":True},
    {"restaurant_id":"R010","item_id":"M053","item_name":"Chapli Kabab","description":"Signature flat beef kabab with herbs — 2 pcs with naan","price":650,"category":"BBQ","emoji":"🍔","is_available":True},
    {"restaurant_id":"R010","item_id":"M054","item_name":"Peshawari Karahi","description":"Bold charcoal-flavored karahi unique to Peshawar","price":950,"category":"Main","emoji":"🍛","is_available":True},
    {"restaurant_id":"R010","item_id":"M055","item_name":"Lamb Chops","description":"Grilled lamb chops marinated in yogurt and spices — 4 pcs","price":1200,"category":"BBQ","emoji":"🍖","is_available":True},
    {"restaurant_id":"R010","item_id":"M056","item_name":"Kabab Platter","description":"Mixed kabab selection: seekh, chapli and boti","price":1400,"category":"BBQ","emoji":"🔥","is_available":True},
    {"restaurant_id":"R010","item_id":"M057","item_name":"Kahwa","description":"Traditional green tea with cardamom and almonds","price":180,"category":"Drinks","emoji":"🫖","is_available":True},
    # Noodle House R011
    {"restaurant_id":"R011","item_id":"M058","item_name":"Dragon Noodles","description":"Spicy Szechuan noodles with chili oil and crispy garlic","price":550,"category":"Noodles","emoji":"🍜","is_available":True},
    {"restaurant_id":"R011","item_id":"M059","item_name":"Lo Mein","description":"Soft noodles stir-fried with vegetables and oyster sauce","price":500,"category":"Noodles","emoji":"🍜","is_available":True},
    {"restaurant_id":"R011","item_id":"M060","item_name":"Chicken Fried Rice","description":"Classic egg fried rice with tender chicken chunks","price":480,"category":"Rice","emoji":"🍳","is_available":True},
    {"restaurant_id":"R011","item_id":"M061","item_name":"Honey Chili Chicken","description":"Crispy chicken tossed in sweet honey chili sauce","price":620,"category":"Chicken","emoji":"🍗","is_available":True},
    {"restaurant_id":"R011","item_id":"M062","item_name":"Wonton Soup","description":"Delicate wontons in clear broth with spring onions","price":300,"category":"Soup","emoji":"🥣","is_available":True},
    # Sweet Cravings R012
    {"restaurant_id":"R012","item_id":"M063","item_name":"Chocolate Lava Cake","description":"Warm chocolate cake with molten center and vanilla ice cream","price":350,"category":"Cakes","emoji":"🍫","is_available":True},
    {"restaurant_id":"R012","item_id":"M064","item_name":"Nutella Waffle","description":"Belgian waffle with Nutella, banana and whipped cream","price":380,"category":"Waffles","emoji":"🧇","is_available":True},
    {"restaurant_id":"R012","item_id":"M065","item_name":"Oreo Shake","description":"Thick blended Oreo milkshake with whipped cream","price":290,"category":"Shakes","emoji":"🥤","is_available":True},
    {"restaurant_id":"R012","item_id":"M066","item_name":"Cheesecake Slice","description":"New York-style baked cheesecake with berry compote","price":400,"category":"Cakes","emoji":"🍰","is_available":True},
    {"restaurant_id":"R012","item_id":"M067","item_name":"Gulab Jamun","description":"Warm soft gulab jamun in sugar syrup — 4 pieces","price":180,"category":"Desi Sweets","emoji":"🍡","is_available":True},
    {"restaurant_id":"R012","item_id":"M068","item_name":"Falooda","description":"Classic falooda with rose syrup, basil seeds and vermicelli","price":260,"category":"Desi Sweets","emoji":"🥤","is_available":True},
]
db.Menu.insert_many(menu_items)
db.Menu.create_index("restaurant_id")
db.Menu.create_index("item_id", unique=True)
print(f"  ✅ {len(menu_items)} menu items inserted")

# ══════════════════════════════════════════════════════════════
# 3. Create empty Orders, Order_items, Payment with indexes
# ══════════════════════════════════════════════════════════════
print("\n  📦 Setting up Orders, Order_items, Payment collections...")
# Orders
db.Orders.create_index("user_id")
db.Orders.create_index("order_code", unique=True, sparse=True)
db.Orders.create_index("order_date")
# Order_items
db.Order_items.create_index("order_id")
db.Order_items.create_index("item_id")
# Payment
db.Payment.create_index("order_id")
db.Payment.create_index("user_id")
# Users
db.Users.create_index("email", unique=True)
print("  ✅ All indexes created")

print("\n  📊 Collections in database:")
for col in sorted(db.list_collection_names()):
    count = db[col].count_documents({})
    print(f"     • {col}: {count} documents")

client.close()
print()
print("="*55)
print("  🎉 Setup complete! Now run:")
print()
print("      python app.py")
print()
print("  Then open: http://localhost:5000")
print("="*55)
