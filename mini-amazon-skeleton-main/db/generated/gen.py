from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_sellers = 50
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('db/generated/Users.csv', 'w') as f:
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
            balance = fake.random_int(min=0)
            writer.writerow([uid, email, password, firstname, lastname, address, balance])
        print(f'{num_users} generated')
    return

def gen_sellers(num_sellers):
    sellers = []
    with open('db/generated/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for uid in fake.random_elements(list(range(num_users)), length=num_sellers, unique=True):
            sellers.append(uid)
            writer.writerow([uid])
        print(f'{num_sellers} generated')
    return sellers

# determines which products are available
def get_available_products(num_products):
    available_pids = []
    for pid in range(num_products):
        if pid % 100 == 0:
            print(f'{pid}', end=' ', flush=True)
        available = fake.random_element(elements=('true', 'false'))
        if available == 'true':
            available_pids.append(pid)
    return available_pids

def gen_products(num_products, seller_pid, available_pids):
    #available_pids = []
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        unavailable_pids = list(set(range(num_products)) - set(available_pids))
        unique_pid_available = {} # key: id, value: (pid, sid)
        unique_pid_unavailable = {} # key: id, value: (pid, sid)
        id = 0
        for pid in available_pids:
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            for sid in seller_pid[pid]: # for each seller that sells current pid
                name = fake.sentence(nb_words=4)[:-1]
                category = fake.random_element(elements=('toys', 'electronic', 'clothes', 'tools', 'food', 'beauty'))
                description = fake.sentence(nb_words=15)[:-1]
                price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
                # available = fake.random_element(elements=('true', 'false'))
                # if available == 'true':
                #     available_pids.append(pid)
                available = 'true'
                unique_pid_available[id] = (pid, sid)
                writer.writerow([id, pid, sid, name, category, description, price, available])
                id += 1 # id is unique, pid is not unique (multiple sellers can have same pid)
        for pid in unavailable_pids:
            name = fake.sentence(nb_words=4)[:-1]
            category = fake.random_element(elements=('toys', 'electronic', 'clothes', 'tools', 'food', 'beauty'))
            description = fake.sentence(nb_words=15)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            unique_pid_unavailable[id] = (pid, sid)
            available = 'false'
            writer.writerow([id, pid, sid, name, category, description, price, available])
            id += 1 # id is unique, pid is not unique (multiple sellers can have same pid)
        print(f'{id} product listings generated; {len(available_pids)} products available; {len(unavailable_pids)} products unavailable')
    return unique_pid_available, unique_pid_unavailable


def gen_purchases(num_purchases, available_pids):
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            # pid = fake.random_element(elements=available_pids, unique = True)
            # time_purchased = fake.date_time()
            # writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_cart(available_pids):
    with open('db/generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            for pid in fake.random_elements(available_pids, length=fake.random_int(min=1, max=30), unique=True):
                qty = fake.random_int(min=1, max=20)
                writer.writerow([uid, pid, qty])
    return

def gen_reviews(num_products, available_pids):
    # available_pids = []
    with open('db/generated/Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            review_text = fake.sentence(nb_words=15)[:-1]
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            rating = fake.random_int(min=1,max=5)
            writer.writerow([id, uid, pid, time_purchased, rating, review_text])
        # print(f'{num_products} generated; {len(available_pids)} available')
    return

def gen_sellerReviews(num_users):
    # available_pids = []
    with open('db/generated/SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_users):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_users-1)
            review_text = fake.sentence(nb_words=15)[:-1]
            time_posted = fake.date_time()
            rating = fake.random_int(min=1,max=5)
            writer.writerow([id, uid, sid, time_posted, rating, review_text])
        # print(f'{num_products} generated; {len(available_pids)} available')
    return    

# function that assigns sellers to available pids
def get_seller_to_pid(available_pids, sellers): #### use all pids, not just available_pids
    for pid in available_pids:
        seller_pid[pid] = [] # all sellers who have this pid in inventory
        num_sellers = random.randint(1,9)  # number of sellers who have this same pid in inventory
        #seller_pid = [] # all sellers who have this pid in inventory
        for i in range(num_sellers):
            if id % 50 == 0:
                print(f'{id}', end=' ', flush=True)
            sid = random.choice(sellers)
            if sid not in seller_pid[pid]: # prevents duplicate sid/pid pairing
                seller_pid[pid].append(sid)
    return seller_pid

# inventory needs products to set unavailable pids to qty = 0
def gen_inventory(sellers, unique_pid_available, unique_pid_unavailable):
    #sellers = [] #contains sid/uid of sellers
    seller_pid = {} # dictionary with key:pid and value:list of sids that sell pid
    with open('db/generated/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True) 
        id = 0
        for unique_pid in unique_pid_available:
            sid = unique_pid_available[unique_pid][1]
            qty = random.choice([1,1,1,10,10,10,20,20,30,50,70,100]) + random.randint(1,9)
            writer.writerow([id, sid, unique_pid, qty])
            id += 1
                
        for unique_pid in unique_pid_unavailable:
            sid = unique_pid_available[unique_pid][1]
            qty = 0
            writer.writerow([id, sid, unique_pid, qty])
            id += 1
        print(f'{id} entries generated')
    return

gen_users(num_users)
sellers = gen_sellers(num_sellers)
available_pids = get_available_products(num_products)
seller_pid = get_seller_to_pid(available_pids, sellers)
unique_pid_available, unique_pid_unavailable = gen_products(num_products, seller_pid, available_pids)
gen_inventory(sellers, unique_pid_available, unique_pid_unavailable)

gen_purchases(num_purchases, available_pids)
gen_cart(available_pids)
gen_inventory(sellers, available_pids)
gen_reviews(num_products, available_pids)
gen_sellerReviews(num_users)
