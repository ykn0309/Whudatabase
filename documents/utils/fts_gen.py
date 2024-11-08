from faker import Faker

fake = Faker()

with open('fts.sql', 'w') as f:
    for i in range (10):
        title = fake.sentence(nb_words=6)
        content = fake.sentence(nb_words=20)
        sql = f"INSERT INTO articles (title, content) VALUES ('{title}', '{content}');\n"
        f.write(sql)
print('OK')