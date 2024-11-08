with open('documents/utils/icbc.txt', 'r') as f1, open('documents/utils/icbc.sql', 'w') as f2:
    for line in f1:
        name, location = line.strip().split()
        sql = f"INSERT INTO icbc (bank_name, bank_location) VALUES ('{name}', vec_f32('[{location}]'));\n"
        f2.write(sql)
print('OK')