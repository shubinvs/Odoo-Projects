from xmlrpc import client

url_db1 = "http://cybrosys:8014"
db_1 = 'odoo_14'
username_db_1 = 'admin'
password_db_1 = 'admin'
common_1 = client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()

url_db2 = "http://cybrosys:8015"
db_2 = 'odoo_15_product'
username_db_2 = 'admin'
password_db_2 = 'admin'
common_2 = client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
models_2 = client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

db_1_products = models_1.execute_kw(db_1, uid_db1, password_db_1,
                                    'product.template', 'search_read', [[]],
                                    {'fields': ['name', 'list_price', 'image_1920', 'standard_price', 'default_code']})
                                    # {'fields': ['name', 'list_price', 'image_1920', 'standard_price', 'categ_id', 'default_code']})

search_products = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                      'product.template', 'search_read', [[]],
                                      {'fields': ['name']})
db_2_products = []
for rec in search_products:
    db_2_products.append(rec['name'])

for rec in db_1_products:
    if rec['name'] not in db_2_products:
        new_products = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                           'product.template', 'create', [rec])
