import sqlite3
import re

# Connect to the SQLite database
db_path = "database.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Provided meal data
meal_data = """
🥗 <b>Appetizers & Light Bites</b>
🍞 Bread - ₦1,500
🍛 Akara(10) - ₦1000
🍛 Moi-moi - ₦700
🥣 Pap (corn) - ₦500
🥣 Pap (millet) - ₦500
🍢🫖 Small Chops (Puffs, Samosas, Spring Rolls, and Chicken) - ₦2,500

🍛<b>Rice, Pasta and noodles</b>
🔥 Jollof Rice - ₦1,500
🥕 Fried Rice - ₦1,500
🍚 White Rice - ₦3,000
🍚 Ofada Rice - ₦4,000
🍚 Spaghetti(Plain white) - ₦4,000
🍲 Spaghetti meal - ₦4,000
🍚 indomie noodles (1 Plain white superpacks) - ₦1000    
🍲 indomie noodles meal (1 superpacks) - ₦1000    
🥚 Egg (boiled) - ₦500

🐟 <b>Fish Meat</b>
🍲🐠 Cooked Tilapia Fish - ₦3,000
🍳🐟 Fried Titus Fish - ₦3,000
🔥🐠 Roasted Tilapia Fish - ₦3,000
🍛🐟 Stewed Cota Fish - ₦3,000
🔥🐟 Dried Fish - ₦3,000
🌶️🐟 Peppered Panla Fish - ₦3,000
🔥🐟 Smoked Fish - ₦3,000

🥩 <b>Cow Meat</b>
🍳🥩 Fried Cow meat - ₦3,000
🍲🥩 Boiled Cow meat- ₦3,000
🌶️🥩 Peppered Cow meat - ₦3,000
🔥🥩 Roasted Cow meat- ₦3,000

🥩 <b>Goat Meat</b>
🍳🥩 Fried Goat meat - ₦3,000
🍲🥩 Boiled Goat meat- ₦3,000
🌶️🥩 Peppered Goat meat - ₦3,000
🔥🥩 Roasted Goat meat- ₦3,000

🥩 <b>Ram Meat</b>
🍳🥩 Fried Ram meat - ₦3,000
🍲🥩 Boiled Ram meat- ₦3,000
🌶️🥩 Peppered Ram meat - ₦3,000
🔥🥩 Roasted Ram meat- ₦3,000

🐔 <b>Local Chicken</b>
🍗 Fried Chicken - N3,000
🍗 Boiled Chicken - ₦3,000
🌶️ Peppered Chicken - ₦3,000
🔥 Roasted Chicken - ₦3,000

🐔 <b>Agric Chicken</b>
🍗 Fried Chicken (Agric) - ₦3,000
🍗 Boiled Chicken (Agric) - ₦3,000
🌶️ Peppered Chicken (Agric) - ₦3,000
🔥 Roasted Chicken (Agric) - ₦3,000

🍽️ <b>Swallow</b>
🍲 Eba - ₦700
🍲 Fufu - ₦900 
🍲 Semovita - ₦900 
🍲 Semolina - ₦900
🍲 Amala - ₦700 - ₦900
🥔 Pounded Yam - ₦900

🥘 <b>Soups and sauce</b>
🥜 Egusi Soup - ₦1,000
🍲 Ogbono Soup - ₦1,000
🥬 Efo Riro - ₦1,600
🍅 Stew - ₦700 - ₦1,300
🌿 Oha Soup - ₦700 - ₦1,200
🍃 Edikang Ikong Soup - ₦1000
🍛 Egg Sauce - ₦1,500
🐠 fish sauce - ₦1000
🌶️ Ayamase Sauce - ₦4,000

🍲 <b>Porridges & Yam, Plantain and Potato Dishes</b>
🍛 Beans- ₦3,000
🍳 Boiled Yam - ₦3,000
🍟 Fried Yam - ₦1,500
🔥 Yam Porridge (Asaro) - ₦3,500
🍠 Boiled sweet Potato - ₦3,500
🍟 Fried sweet Potato - ₦3,500
🍠 Boiled Irish Potato - ₦3,500
🍟 Fried Irish Potato - ₦3,500    
🍳 Boiled Plantain - ₦3,000
🍟 Fried Plantain - ₦3,000    

🌯 <b>Grilled & Roasted</b>
🌯🔥 Shawarma (Nigerian Style) - ₦3,500
🍗 Grilled Chicken with Fried Yam - ₦5,000
🍌🐠 Bole (Roasted Plantain) & Fish Sauce - ₦3,500

🍜 <b>Extras</b>
🍲🐐 Peppersoup Goat Meat - ₦4,200
🍲🐔 Peppersoup Chicken - ₦4,200
🥩🔥 Nkwobi (Spicy Cow Leg Dish) - ₦4,500
🍢🔥 Suya with Onions & Pepper - ₦3,000

💧🥤 <b>Water and Juice Drinks</b>
💧 Bottled Water - ₦300
🍹 Orange juice - ₦700
🍹 Mango juice - ₦700
🍹 Punch - ₦300
"""

# Extract meal names and prices
meal_pattern = re.compile(r"[\w\s\(\)-]+ - ₦?([\d,]+)")
meals = meal_pattern.findall(meal_data)

# Prepare meals for insertion
meal_entries = []
for match in meal_pattern.finditer(meal_data):
    meal_name = match.group(0).split(" - ")[0].strip()
    price = match.group(1).replace(",", "")
    
    description = "A combination of " + meal_name
    image = None
    deleted = 0
    
    meal_entries.append((meal_name, description, int(price), image, deleted))

# Insert into the database
# cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", meal_entries)
cursor.executemany("INSERT INTO products (name, description, price, image, deleted) VALUES (?, ?, ?, ?, ?)", meal_entries)

# Commit changes and close connection
conn.commit()
conn.close()

# Return number of inserted items
len(meal_entries)


# from itertools import combinations
# import sqlite3

# # Extract meal items and their prices from the provided meal_type string
# meal_prices = {
#     "Bread": 1500,
#     "Akara(10)": 1000,
#     "Moi-moi": 700,
#     "Pap (corn)": 500,
#     "Pap (millet)": 500,
#     "Small Chops": 2500,
#     "Jollof Rice": 1500,
#     "Fried Rice": 1500,
#     "White Rice": 3000,
#     "Ofada Rice": 4000,
#     "Spaghetti(Plain white)": 4000,
#     "Spaghetti meal": 4000,
#     "Indomie noodles (Plain white superpacks)": 1000,
#     "Indomie noodles meal (1 superpacks)": 1000,
#     "Egg (boiled)": 500,
#     "Cooked Tilapia Fish": 3000,
#     "Fried Titus Fish": 3000,
#     "Roasted Tilapia Fish": 3000,
#     "Stewed Cota Fish": 3000,
#     "Dried Fish": 3000,
#     "Peppered Panla Fish": 3000,
#     "Smoked Fish": 3000,
#     "Fried Cow meat": 3000,
#     "Boiled Cow meat": 3000,
#     "Peppered Cow meat": 3000,
#     "Roasted Cow meat": 3000,
#     "Fried Goat meat": 3000,
#     "Boiled Goat meat": 3000,
#     "Peppered Goat meat": 3000,
#     "Roasted Goat meat": 3000,
#     "Fried Ram meat": 3000,
#     "Boiled Ram meat": 3000,
#     "Peppered Ram meat": 3000,
#     "Roasted Ram meat": 3000,
#     "Fried Chicken": 3000,
#     "Boiled Chicken": 3000,
#     "Peppered Chicken": 3000,
#     "Roasted Chicken": 3000,
#     "Fried Chicken (Agric)": 3000,
#     "Boiled Chicken (Agric)": 3000,
#     "Peppered Chicken (Agric)": 3000,
#     "Roasted Chicken (Agric)": 3000,
#     "Eba": 700,
#     "Fufu": 900,
#     "Semovita": 900,
#     "Semolina": 900,
#     "Amala": 900,
#     "Pounded Yam": 900,
#     "Egusi Soup": 1000,
#     "Ogbono Soup": 1000,
#     "Efo Riro": 1600,
#     "Stew": 1300,
#     "Oha Soup": 1200,
#     "Edikang Ikong Soup": 1000,
#     "Egg Sauce": 1500,
#     "Fish Sauce": 1000,
#     "Ayamase Sauce": 4000,
#     "Beans": 3000,
#     "Boiled Yam": 3000,
#     "Fried Yam": 1500,
#     "Yam Porridge (Asaro)": 3500,
#     "Boiled Sweet Potato": 3500,
#     "Fried Sweet Potato": 3500,
#     "Boiled Irish Potato": 3500,
#     "Fried Irish Potato": 3500,
#     "Boiled Plantain": 3000,
#     "Fried Plantain": 3000,
#     "Shawarma (Nigerian Style)": 3500,
#     "Grilled Chicken with Fried Yam": 5000,
#     "Bole & Fish Sauce": 3500,
#     "Peppersoup Goat Meat": 4200,
#     "Peppersoup Chicken": 4200,
#     "Nkwobi": 4500,
#     "Suya with Onions & Pepper": 3000,
#     "Bottled Water": 300,
#     "Orange Juice": 700,
#     "Mango Juice": 700,
#     "Punch": 300
# }

# db_path = "database.sqlite"

# # Generate all possible meal combinations
# meal_combinations = []
# for r in range(1, 4):  # 1-item, 2-item, and 3-item combinations
#     for combo in combinations(meal_prices.keys(), r):
#         name = " and ".join(combo) if len(combo) == 2 else ", ".join(combo)
#         price = sum(meal_prices[item] for item in combo)
#         description = f"A combination of {name}."
#         deleted = 0
#         image = None
#         meal_combinations.append((name, description, price, image, deleted))
        

# # Insert into the SQLite database
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Insert meal combinations into the products table
# cursor.executemany("INSERT INTO products (name, description, price, image, deleted) VALUES (?, ?, ?, ?, ?)", meal_combinations)

# # Commit changes and close connection
# conn.commit()
# conn.close()

# # Output number of records inserted
# len(meal_combinations)
