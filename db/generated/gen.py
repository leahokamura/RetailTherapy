from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_accounts = num_users

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


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
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


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
            writer.writerow([uid, oid, time_purchased, total_amount, item_quantity, fulfillment_status, order_page])
        print(f'{num_purchases} generated')
    return


gen_users(num_users)
gen_account(num_accounts)
available_pids = gen_products(num_products)
gen_purchases(num_purchases)

