from faker import Faker
import random

fake = Faker()

table_name = 'user_test'

delete_set = set()
name_set= set()
age_set = set()

insert_count1 = 3000
update_count = 1500
delete_count = 1500
insert_count2 = 4000
select_count = 10000

def gen_id(a, b):
    id = random.randint(a, b)
    while id in delete_set:
        id = random.randint(a, b)
    return id

def random_projection():
    columns = ["name", "age", "city", "email", "name, age", "name, city", "name, email", "name, age, city", "name, age, email", "*"]
    return random.choice(columns)

def random_condition():
    random_num = random.randint(1,3)
    if random_num == 1:
        random_id = gen_id(1, insert_count1 + insert_count2)
        sql = f"id = {random_id}"
    elif random_num == 2:
        random_name = random.choice(name_set)
        sql = f"name = '{random_name}'"
    else:
        random_age = random.choice(age_set)
        sql = f"age = {random_age}"
    return sql

if __name__ == "__main__":
    with open('testdata.sql', 'w') as f:
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, city TEXT, email TEXT);\n"
        f.write(create_table_sql)

        for i in range (insert_count1):
            name = fake.name()
            age = fake.random_int(min=18, max=80)
            city = fake.city()
            address = fake.address()
            email = fake.email()
            sql = f"INSERT INTO {table_name} (name, age, city, email) VALUES ('{name}', {age}, '{city}', '{email}');\n"
            f.write(sql)

        for i in range (update_count):
            random_num = random.randint(1, 4)
            if random_num == 1:
                set_content = f"name = '{fake.name()}'"
            elif random_num == 2:
                set_content = f"age = {fake.random_int(min=18, max=80)}"
            elif random_num ==3:
                set_content = f"city = '{fake.city()}'"
            else:
                set_content = f"email = '{fake.email()}'"
            sql = f"UPDATE {table_name} SET {set_content} WHERE id = {random.randint(1, insert_count1)};\n"
            f.write(sql)

        for i in range (delete_count):
            id = gen_id(1, insert_count1)
            delete_set.add(id)
            sql = f"DELETE FROM {table_name} WHERE id = {id};\n"
            f.write(sql)

        for i in range (insert_count2):
            name = fake.name()
            age = fake.random_int(min=18, max=80)
            city = fake.city()
            address = fake.address()
            email = fake.email()
            name_set.add(name)
            age_set.add(age)
            sql = f"INSERT INTO {table_name} (name, age, city, email) VALUES ('{name}', {age}, '{city}', '{email}');\n"
            f.write(sql)
        
        name_set = list(name_set)
        age_set = list(age_set)

        for i in range (select_count):
            sql = f"SELECT {random_projection()} from {table_name} where {random_condition()};\n"
            f.write(sql)

    print('OK')