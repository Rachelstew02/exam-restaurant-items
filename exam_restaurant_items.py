from peewee import *
db = SqliteDatabase('menuitem.db')

class MenuItem(Model):
    menu_item_id = AutoField(primary_key = True)
    name = CharField()
    category = CharField()
    price = FloatField()

    class Meta:
        database = db
    
    @classmethod
    def create (cls, **query):
        if query['price'] < 0:
            print("Invalid price! Price must be between $0 and $50")
            return
        elif query['price'] >50:
            print("Invalid price! Price must be between $0 and $50")
            return
        
        categories_list = ["APPETIZER", "SIDE", "ENTREE", "DESSERT"]

        if query['category'] not in categories_list:
            print("Invalid category! Category must be either APPETIZER, SIDE, ENTREE, or DESSERT")
            return
        new_item = super().create(**query)
        print(f"Item '{query['name']} added successfully.")
        return new_item
            
    def get_info(self):
        print(f"ID: {self.menu_item_id} | Name: {self.name} | Category: {self.category} | Price: ${self.price}")
    

db.connect()
db.create_tables([MenuItem])




while True:
    print("Restaurant Menu Manager:",'\n',
          "1. Add a menu item",'\n',
          "2. View all menu items", '\n',
          "3. View the most expensive item in each category", '\n',
          "4. Exit")
    
    menu_selection = input("Choose an option (1-4)")

    while True:
        if menu_selection =="1":
            item_name_input = input("Enter the item name: ")
            category_add_input = input("Enter the category ('APPETIZER', 'SIDE', 'ENTREE', 'DESSERT'): ")
            price_add_input = input("Enter the price: ")
            price_add_input = float(price_add_input)
            category_add_input = category_add_input.upper()
            
            MenuItem.create(name = item_name_input, category = category_add_input, price = price_add_input)
            break

    if menu_selection == "2":
        menu_list= MenuItem.select()
        for item in menu_list:
            item.get_info()

    if menu_selection == "3":
        Appetizer_list= MenuItem.select().where(category ='APPETIZER').order_by(MenuItem.price.desc())
        Entree_list= MenuItem.select().where(category ='ENTREE').order_by(MenuItem.price.desc())
        Side_list= MenuItem.select().where(category ='SIDE').order_by(MenuItem.price.desc())
        Dessert_list= MenuItem.select().where(category ='DESSERT').order_by(MenuItem.price.desc())

        expensive_app = Appetizer_list[0]
        expensive_entree = Entree_list[0]
        expensive_side = Side_list[0]
        expensive_dessert = Dessert_list[0]

        print(f"Most expensive {expensive_app.category}:", '\n',
                "{expensive_app.get_info}")
        print(f"Most expensive {expensive_side.category}:", '\n',
                "{expensive_side.get_info}")
        print(f"Most expensive {expensive_entree.category}:", '\n',
                "{expensive_entree.get_info}")
        print(f"Most expensive {expensive_dessert.category}:", '\n',
                "{expensive_dessert.get_info}")
        
    if menu_selection == "4":
        print('Goodbye')
        break
    else:
        print("Invalid choice. Please try again.")