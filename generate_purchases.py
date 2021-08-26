import sqlite3
import random
from faker import Faker


fake = Faker()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS "wasite_purchases" (
                                                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                "card" varchar(11) NOT NULL,
                                                "date_create" datetime NOT NULL,
                                                "summ" real NOT NULL,
                                                "goods" varchar(10000) NOT NULL,
                                                "card_id_id" bigint NOT NULL REFERENCES "wasite_card" ("id") DEFERRABLE INITIALLY DEFERRED,
                                                "shop" integer(10) NOT NULL, 
                                                "emploeye" integer(10) NOT NULL)""")

card_id_range = [str(i) for i in range(1, 101)]
#card_id_range = [str(i) for i in range(101, 201)]

prod = ['mussels', 'sausages', 'walnuts', 'pistachios', 'banana', 'tuna', 'almonds', 'lamb', 'cheese', 'crab', 
         'shampoo', 'feta', 'beer', 'garlic', 'beans', 'carp', ' potato', 'chicken', 'chicken wings', 'pumpkin', 
         'broccoli', 'apple', ' shrimp', 'bacon', ' avocado', 'corn', 'grapes', 'beef', 'pork', 'meat', ' milk', 
         'oysters', ' peanuts', 'parmesan ', 'salmon', 'ox tongue', 'spinach', 'lobster', 'cola', 'tomato', 
         'mushrooms', 'mozzarella ', 'sardines', 'blackberry', ' beer', 'artichoke', 'drumsticks', 'vine', 'spaghetti', 
         'onion', 'ricotta', 'cashew', 'rice', 'yam', 'gelato', 'orange', 'octopus', ' pork', 'lemon', 'butter', 'zucchini', 
         'yoghurt', 'kivi', 'plum', 'turkey', 'chestnuts', 'cherry']

shop_id = [i for i in range(1,21)]
emploeye_id = [i for i in range(1,51)]

for i in range(1, 5000):
    card_id_id = random.choice(card_id_range)
    card = "AA" + f"0000{card_id_id}"[-5:]
    #card = "BB" + f"0000{int(card_id_id) - 100}"[-5:]
    date_create = fake.date_time_between(start_date="-1y", end_date="now")#.strftime('%d.%m.%Y %H:%M')
    goods = {random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)],
             random.choice(prod):[round(random.uniform(1.0, 5.0), 2), round(random.uniform(1.0, 100.0), 2)]}
    summ = round(sum(i[1] for i in goods.values()), 2)
    shop = random.choice(shop_id)
    emploeye = random.choice(emploeye_id)

    cur.execute("""INSERT INTO wasite_purchases 
                (card, date_create, summ, goods, card_id_id, shop, emploeye) VALUES (?,?,?,?,?,?,?)""", 
                [card, date_create, summ, str(goods), card_id_id, shop, emploeye])

con.commit()
con.close()
