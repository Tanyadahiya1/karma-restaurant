"""Seed data for the Karma Indian Restaurant database."""

from slugify_util import slugify

MENU_ITEMS = [
    # Appetizers
    dict(name="Samosa Chaat", category="Appetizers", price=8.99, is_veg=True, spice_level=1,
         description="Crispy samosas topped with chickpeas, tangy tamarind and mint chutney, yogurt and pomegranate.",
         image="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800&q=80", is_popular=True),
    dict(name="Paneer Tikka", category="Appetizers", price=11.99, is_veg=True, spice_level=2,
         description="Chunks of cottage cheese marinated in yogurt and spices, char-grilled in the tandoor.",
         image="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80", is_popular=True),
    dict(name="Chicken 65", category="Appetizers", price=13.99, is_veg=False, spice_level=3,
         description="Karma's legendary deep-fried chicken bites, tempered with curry leaves and green chillies.",
         image="https://images.unsplash.com/photo-1598515213692-5f252f1e1c1c?w=800&q=80", is_popular=True),
    dict(name="Chili Paneer", category="Appetizers", price=13.99, is_veg=True, spice_level=2,
         description="Indian cheese cubes tossed in chili garlic sauce with onion and bell pepper.",
         image="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80"),
    dict(name="Masala Papad", category="Appetizers", price=5.99, is_veg=True, spice_level=1,
         description="Crisp lentil wafer topped with chopped onion, tomato, cilantro and tangy spices.",
         image="https://images.unsplash.com/photo-1600335895229-6e75511892c8?w=800&q=80"),
    dict(name="Chicken Manchurian", category="Appetizers", price=14.99, is_veg=False, spice_level=2,
         description="Boneless chicken cubes tossed in Karma's signature Indo-Chinese manchurian sauce.",
         image="https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=800&q=80"),
    dict(name="Vegetable Pakora", category="Appetizers", price=7.99, is_veg=True, spice_level=1,
         description="Assorted vegetables dipped in spiced chickpea batter and fried golden, served with chutney.",
         image="https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800&q=80"),

    # Vegetarian
    dict(name="Paneer Butter Masala", category="Vegetarian", price=15.99, is_veg=True, spice_level=1,
         description="Cottage cheese simmered in a velvety tomato and cashew gravy, finished with cream and butter.",
         image="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80", is_popular=True),
    dict(name="Dal Makhani", category="Vegetarian", price=13.99, is_veg=True, spice_level=1,
         description="Black lentils slow-simmered overnight with butter, cream and aromatic spices.",
         image="https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=800&q=80"),
    dict(name="Malai Kofta", category="Vegetarian", price=14.99, is_veg=True, spice_level=1,
         description="Delicate potato and paneer dumplings in a rich, creamy cashew tomato sauce.",
         image="https://images.unsplash.com/photo-1631292784640-2b24be784d5d?w=800&q=80"),
    dict(name="Chana Masala", category="Vegetarian", price=12.99, is_veg=True, spice_level=2,
         description="Chickpeas simmered in a robust onion-tomato masala with cumin and pomegranate seed.",
         image="https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80"),

    # Non Vegetarian
    dict(name="Butter Chicken", category="Non Vegetarian", price=17.99, is_veg=False, spice_level=1,
         description="Tandoor-roasted chicken in a luxurious tomato butter sauce, Karma's signature dish.",
         image="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800&q=80", is_popular=True),
    dict(name="Chicken Tikka Masala", category="Non Vegetarian", price=16.99, is_veg=False, spice_level=2,
         description="Grilled chicken tikka simmered in a spiced, creamy tomato masala sauce.",
         image="https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800&q=80"),
    dict(name="Lamb Rogan Josh", category="Non Vegetarian", price=19.99, is_veg=False, spice_level=3,
         description="Tender lamb slow-cooked in a Kashmiri chilli and yogurt gravy with warming whole spices.",
         image="https://images.unsplash.com/photo-1631292784640-2b24be784d5d?w=800&q=80"),
    dict(name="Goan Fish Curry", category="Non Vegetarian", price=18.99, is_veg=False, spice_level=2,
         description="Fresh fish simmered in a tangy coconut curry with kokum and curry leaves.",
         image="https://images.unsplash.com/photo-1626777553635-be0defb85e0f?w=800&q=80"),

    # Biryani
    dict(name="Chicken Biryani", category="Biryani", price=16.99, is_veg=False, spice_level=2,
         description="Fragrant basmati rice layered and dum-cooked with marinated chicken and saffron.",
         image="https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800&q=80", is_popular=True),
    dict(name="Lamb Biryani", category="Biryani", price=19.99, is_veg=False, spice_level=2,
         description="Slow dum-cooked basmati rice with tender lamb, caramelized onions and warm spices.",
         image="https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=800&q=80"),
    dict(name="Vegetable Biryani", category="Biryani", price=14.99, is_veg=True, spice_level=1,
         description="Basmati rice dum-cooked with garden vegetables, saffron and fried onions.",
         image="https://images.unsplash.com/photo-1596797038530-2c107229654b?w=800&q=80"),

    # South Indian
    dict(name="Masala Dosa", category="South Indian", price=12.99, is_veg=True, spice_level=1,
         description="Crisp fermented rice and lentil crepe filled with spiced potato masala, served with sambar.",
         image="https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=800&q=80", is_popular=True),
    dict(name="Idli Sambar", category="South Indian", price=9.99, is_veg=True, spice_level=1,
         description="Steamed rice cakes served with lentil sambar and coconut chutney.",
         image="https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&q=80"),
    dict(name="Uttapam", category="South Indian", price=11.99, is_veg=True, spice_level=1,
         description="Thick savory rice pancake topped with onions, tomatoes and green chillies.",
         image="https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=800&q=80"),

    # Tandoor
    dict(name="Tandoori Chicken (Half)", category="Tandoor", price=15.99, is_veg=False, spice_level=2,
         description="Chicken marinated in yogurt and spices, roasted in the traditional clay tandoor.",
         image="https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=800&q=80"),
    dict(name="Seekh Kebab", category="Tandoor", price=14.99, is_veg=False, spice_level=2,
         description="Minced lamb skewers spiced with ginger, garlic and garam masala, chargrilled to order.",
         image="https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=800&q=80"),
    dict(name="Tandoori Prawns", category="Tandoor", price=18.99, is_veg=False, spice_level=2,
         description="Jumbo prawns marinated in tandoori spice and yogurt, roasted until smoky.",
         image="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800&q=80"),

    # Bread
    dict(name="Garlic Naan", category="Bread", price=4.49, is_veg=True, spice_level=0,
         description="Soft leavened flatbread brushed with garlic butter, baked fresh in the tandoor.",
         image="https://images.unsplash.com/photo-1596797038530-2c107229654b?w=800&q=80", is_popular=True),
    dict(name="Butter Naan", category="Bread", price=3.99, is_veg=True, spice_level=0,
         description="Classic tandoor-baked flatbread finished with a brush of melted butter.",
         image="https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=800&q=80"),
    dict(name="Tandoori Roti", category="Bread", price=3.49, is_veg=True, spice_level=0,
         description="Whole wheat flatbread baked in the tandoor, light and slightly charred.",
         image="https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=800&q=80"),

    # Desserts
    dict(name="Gulab Jamun", category="Desserts", price=6.99, is_veg=True, spice_level=0,
         description="Warm milk-solid dumplings soaked in rose and cardamom scented sugar syrup.",
         image="https://images.unsplash.com/photo-1601303516361-a5b7b4f0c6d2?w=800&q=80", is_popular=True),
    dict(name="Rasmalai", category="Desserts", price=7.49, is_veg=True, spice_level=0,
         description="Soft cottage cheese dumplings soaked in saffron and cardamom infused sweetened milk.",
         image="https://images.unsplash.com/photo-1606471191009-63994c53433b?w=800&q=80"),
    dict(name="Kheer", category="Desserts", price=6.49, is_veg=True, spice_level=0,
         description="Traditional rice pudding simmered with milk, cardamom, saffron and roasted nuts.",
         image="https://images.unsplash.com/photo-1606471191009-63994c53433b?w=800&q=80"),

    # Drinks
    dict(name="Mango Lassi", category="Drinks", price=5.49, is_veg=True, spice_level=0,
         description="Chilled yogurt drink blended with sweet Alphonso mango pulp.",
         image="https://images.unsplash.com/photo-1626200926749-1633dcbdb3e6?w=800&q=80", is_popular=True),
    dict(name="Masala Chai", category="Drinks", price=3.99, is_veg=True, spice_level=0,
         description="Spiced black tea simmered with milk, cardamom, ginger and cinnamon.",
         image="https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=800&q=80"),
    dict(name="Sweet Lassi", category="Drinks", price=4.99, is_veg=True, spice_level=0,
         description="Classic churned yogurt drink lightly sweetened and topped with a pinch of saffron.",
         image="https://images.unsplash.com/photo-1626200926749-1633dcbdb3e6?w=800&q=80"),
]


def get_menu_items_with_slugs():
    used = set()
    items = []
    for item in MENU_ITEMS:
        base_slug = slugify(item["name"])
        slug = base_slug
        i = 2
        while slug in used:
            slug = f"{base_slug}-{i}"
            i += 1
        used.add(slug)
        item = dict(item)
        item["slug"] = slug
        items.append(item)
    return items
