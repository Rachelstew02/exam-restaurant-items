#importing libraries
from peewee import *
db = SqliteDatabase('menuitem.db')

#create class
class MenuItem(Model):
    menu_item_id = AutoField(primary_key = True)
    name = CharField()
    category = CharField()
    price = FloatField()

    class Meta:
        database = db
    
    #overwrite create method
    @classmethod
    def create (cls, **query):
        #ensure price is between $0 and $50
        if query['price'] < 0:
            print("Invalid price! Price must be between $0 and $50")
            return
        elif query['price'] >50:
            print("Invalid price! Price must be between $0 and $50")
            return
        
        categories_list = ["APPETIZER", "SIDE", "ENTREE", "DESSERT"]

        #ensure category is one of the 4 predetermined categories
        category = query.get('category')
        if category:
            category = category.upper()
            query['category'] = category

        if category not in categories_list:
            print("Invalid category! Category must be either APPETIZER, SIDE, ENTREE, or DESSERT")
            return
        new_item = super().create(**query)
        print(f"Item '{query['name']}' added successfully.",'\n')
        return new_item
            
    
    #create the get info method
    def get_info(self):
        return(f"ID: {self.menu_item_id} | Name: {self.name} | Category: {self.category} | Price: ${self.price}")
    
#connect database
db.connect()
db.create_tables([MenuItem])

while True:
    #print menu
    print("Restaurant Menu Manager:",'\n',
          "1. Add a menu item",'\n',
          "2. View all menu items", '\n',
          "3. View the most expensive item in each category", '\n',
          "4. Exit")
    
    menu_selection = input("Choose an option (1-4): ")

    
    #Menu option 1: Adding a menu item
    if menu_selection =="1":
        item_name_input = input("Enter the item name: ")
        category_add_input = input("Enter the category ('APPETIZER', 'SIDE', 'ENTREE', 'DESSERT'): ")
        price_add_input = input("Enter the price: ")
        price_add_input = float(price_add_input)
        
        #creating a new object
        MenuItem.create(name = item_name_input, category = category_add_input, price = price_add_input)
        

    #Menu option 2: Viewing all menu items
    elif menu_selection == "2":
        menu_list= MenuItem.select()
        for item in menu_list:
            item.get_info()
            

    #Menu option 3: Viewing the most expensive item
    elif menu_selection == "3":
        #Appetizer: get list of appetizers
        Appetizer_list= MenuItem.select().where(MenuItem.category =='APPETIZER').order_by(MenuItem.price.desc())
        #create empty prices list
        app_prices = []
        #add the price of each appetizer to the prices list
        for app in Appetizer_list:
            price = app.price
            app_prices.append(price)

        #repeat with entree
        Entree_list= MenuItem.select().where(MenuItem.category =='ENTREE').order_by(MenuItem.price.desc())
        entree_prices = []
        for entree in Entree_list:
           price = entree.price
           entree_prices.append(price)

        #repeat with side
        Side_list= MenuItem.select().where(MenuItem.category =='SIDE').order_by(MenuItem.price.desc())
        side_prices = []
        for side in Side_list:
            price = side.price
            side_prices.append(price)

        #repeat with dessert
        Dessert_list= MenuItem.select().where(MenuItem.category =='DESSERT').order_by(MenuItem.price.desc())
        dessert_prices = []
        for dessert in Dessert_list:
            price = dessert.price
            dessert_prices.append(price)

        #get most expensive object (first item on the list)
        expensive_app = app_prices[0]
        expensive_entree = entree_prices[0]
        expensive_side = side_prices[0]
        expensive_dessert = dessert_prices[0]

        #get the object associated with that most expensive price
        app_obj = MenuItem.get(price = expensive_app)
        entree_obj = MenuItem.get(price = expensive_entree)
        side_obj = MenuItem.get(price = expensive_side)
        dessert_obj = MenuItem.get(price = expensive_dessert)

        #print messages and get infos for each category's most expensive item
        print("Most expensive APPETIZER:")
        print(f"{app_obj.get_info()}")
        print("Most expensive SIDE:")
        print(f"{side_obj.get_info()}")
        print("Most expensive ENTREE:")
        print(f"{entree_obj.get_info()}")
        print("Most expensive DESSERT:")
        print(f"{dessert_obj.get_info()}")
        
        
        
    #Menu option 4: exit database
    elif menu_selection == "4":
        print('Goodbye')
        break

    else:
        #message for invalid option selected
        print("Invalid choice. Please try again.")