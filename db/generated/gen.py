from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_sellers = 100
num_accounts = num_users + num_sellers
num_categories = 20
num_carts = 3000

images = [
    "http://placehold.it/120x120&text=image1",
    "http://placehold.it/120x120&text=image2",
    "http://placehold.it/120x120&text=image3",
    "http://placehold.it/120x120&text=image4",
]

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

#Users(uid, email, firstname, lastname, address, password)
def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['residence']
            writer.writerow([uid, email, firstname, lastname, address, password])
        print(f'{num_users} generated')
    return

#Account(uid, balance)
def gen_account(num_accounts):
    with open('Account.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Account...', end=' ', flush=True)
        for uid in range(num_accounts):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            balance = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            writer.writerow([uid, balance])
        print(f'{num_accounts} generated')
    return

#Purchases(oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page)
def gen_purchases(num_purchases):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for oid in range(num_purchases):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            time_purchased = fake.date_time()
            total_amount = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            item_quantity = f'{str(fake.random_int(max=100))}'
            fulfillment_status = fake.random_element(elements=('Ordered', 'In Transit', 'Delivered'))
            order_page = fake.url()
            writer.writerow([oid, uid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page])
        print(f'{num_purchases} generated')
    return

#Product_Categories(category)
def gen_product_categories(num_categories):
    with open('Product_Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Categories...', end=' ', flush=True)
        for categories in range(num_categories):
            if categories % 10 == 0:
                print(f'{categories}', end=' ', flush=True)
            category = fake.sentence(nb_words=2)[:-1]
            writer.writerow([category])
        print(f'{num_categories} generated')
    return

#Products(pid, name, price, available, img)
def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            img = fake.random_element(images)
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available, img])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


# NEED TO FIX GENERATED DATA!!!
#--Cart(uid, pid, p_quantity, unit_price, seller_id)
#Cart(cid)
def gen_cart(num_carts):
    with open('Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 10 == 0:
                print(f'{cid}', end=' ', flush=True)
            writer.writerow([cid])
        print(f'{num_carts} generated')
    return

#InCart(cid, p_quantity, unit_price, total_price, pid, uid)
def gen_in_cart(num_carts):
    with open('InCart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('In Cart...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            total_price = str((int(p_quantity))*float(unit_price))
            writer.writerow([cid, p_quantity, unit_price, total_price, pid, uid])
        print(f'{num_purchases} generated')
    return


#SaveForLater(cid, p_quantity, unit_price, total_price, pid)
def gen_save_for_later(num_carts, num_products):
    with open('SaveForLater.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Save For Later...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            pid = fake.random_int(min=0, max=num_products-1)
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            total_price = str((int(p_quantity))*float(unit_price))
            writer.writerow([cid, p_quantity, unit_price, total_price, pid])
        print(f'{num_purchases} generated')
    return


#Orders(cid, oid, order_totalPrice, fulfilled)
def gen_orders(num_purchases, num_carts):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for cid in range(num_carts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            oid = fake.random_int(min=0, max=num_purchases-1)
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            order_totalPrice = str((int(p_quantity))*float(unit_price))
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([cid, oid, order_totalPrice, fulfilled])
        print(f'{num_purchases} generated')
    return


#Sellers(uid)
def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            writer.writerow([uid])
        print(f'{num_sellers} generated')
    return


#Inventory(seller_id, pid, quantity)
def gen_inventory(num_sellers):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for seller_id in range(num_sellers):
            if seller_id % 10 == 0:
                print(f'{seller_id}', end=' ', flush=True)
            for pid in range(10):
                quantity = f'{str(fake.random_int(max=100))}'
                writer.writerow([seller_id, pid, quantity])
        print(f'{num_sellers} generated')
    return


#SellerOrders(seller_id, order_id, uid)
def gen_seller_orders(num_purchases):
    with open('SellerOrders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Orders...', end=' ', flush=True)
        for order_id in range(num_purchases):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            seller_id = fake.random_int(max=num_sellers)
            uid = fake.random_int(max=num_users)
            writer.writerow([seller_id, order_id, uid])
        print(f'{num_purchases} generated')
    return

#UpdateSubmission(buyer_balance, seller_balance, fulfilled_time, oid, cid, seller_id, total_price)
def gen_update_submission(num_purchases):
    with open('UpdateSubmission.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Update Submission...', end=' ', flush=True)
        for oid in range(num_carts):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            cid = fake.random_int(min=0, max=num_purchases-1)
            seller_id = fake.random_int(min=0, max=num_sellers-1)
            #bid = fake.random_int(min=0, max=num_accounts-1) no table for this
            p_quantity = f'{str(fake.random_int(max=100))}'
            unit_price = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            total_price = str((int(p_quantity))*float(unit_price))
            fulfilled_time = fake.date_time()
            buyer_balance = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            seller_balance = f'{str(fake.random_int(max=5000))}.{fake.random_int(max=99):02}'
            writer.writerow([buyer_balance, seller_balance, fulfilled_time, oid, cid, seller_id, total_price])
        print(f'{num_purchases} generated')
    return


#Product_Reviews(uid, pid, time, rating, comments, votes)
def gen_product_reviews(num_products):
    with open('Product_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            time = fake.date_time()
            rating = fake.random_int(min=0, max=5)
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([uid, pid, time, rating, comments, votes])
        print(f'{num_categories} generated')
    return



#Seller_Reviews(uid, seller_id, time, rating, comments, votes)
def gen_seller_reviews(num_sellers):
    with open('Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            seller_id = fake.random_int(max=num_sellers)
            time = fake.date_time()
            rating = fake.random_int(min=0, max=5)
            comments = fake.sentence(nb_words=20)[:-1]
            votes = fake.random_int(min=0, max=num_users-1)
            writer.writerow([uid, seller_id, time, rating, comments, votes])
        print(f'{num_categories} generated')
    return


#Images_Reviews(uid, pid, img)
def gen_images_reviews(num_products):
    with open('Images_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Images Reviews...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            img = fake.random_element(images)
            writer.writerow([uid, pid, img])
        print(f'{num_categories} generated')
    return


gen_users(num_users)
gen_account(num_accounts)
gen_purchases(num_purchases)

gen_product_categories(num_categories)
available_pids = gen_products(num_products)

gen_cart(num_carts)
gen_in_cart(num_carts)
gen_save_for_later(num_carts, num_products)
gen_orders(num_purchases, num_carts)

gen_sellers(num_sellers)
gen_inventory(num_sellers)
gen_seller_orders(num_purchases)
gen_update_submission(num_purchases)

gen_product_reviews(num_products)
gen_seller_reviews(num_sellers)
gen_images_reviews(num_products)





