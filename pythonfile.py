str_ = """   
id bigint NOT NULL,
myuser_id bigint NOT NULL,
group_id integer NOT NULL"""

for i in str_.split('\n'):
    k = i.split(' ')
    print(k[0])