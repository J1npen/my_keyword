from db import connect_database
from prettytable import PrettyTable

def map_keyword_id_name(p):
    conn = connect_database()
    cursor = conn.cursor()
    choice = 0

    # Determine if p is id or name
    try:
        int(p)
        sql = 'SELECT * FROM keyword WHERE id = %s'
        choice = 1
    except ValueError as e:
        sql = 'SELECT * FROM keyword WHERE keyword_name = %s'
        choice = 2
    
    cursor.execute(sql,p)
    data = cursor.fetchall() 
    row = data[0]

    if choice == 1:
        return row['keyword_name']
    elif choice == 2:
        return row['id']
    else:
        return

def map_site_id_name(p):
    conn = connect_database()
    cursor = conn.cursor()
    choice = 0

    # Determine if p is id or name
    try:
        int(p)
        sql = 'SELECT * FROM site WHERE id = %s'
        choice = 1
    except ValueError as e:
        sql = 'SELECT * FROM site WHERE site_name = %s'
        choice = 2
    
    cursor.execute(sql,p)
    data = cursor.fetchall() # [{'id': 1, 'site_name': 'Telegram', 'url': 'web.telegram.org', 'quick_search': 'none'}]
    row = data[0]

    if choice == 1:
        return row['site_name']
    elif choice == 2:
        return row['id']
    else:
        return

def add_keyword():
    conn = connect_database()
    cursor = conn.cursor()
    
    keyword_name = input('请输入 keyword：').strip()
    if not keyword_name:
        print('未添加数据！')
        return

    # if not site you want to add?
    query_site()
    gap_time = 0
    while True:
        site_id = input('请输入网站对应的 id 或网站名称：').strip()
        if site_id:
            break
        elif gap_time == 3:
            print('未添加数据！')
            return
        else: 
            gap_time += 1
            print('该选项必填！')
    try:
        int(site_id)
    except ValueError as e:
        # create a new site row
        new_site_name = site_id
        site_url = input('请输入网站 url：')
        sql = '''
INSERT site(site_name, url)
VALUE
(%s,%s)
'''
        cursor.execute(sql,(new_site_name, site_url))

        ## get site_id
        sql = 'SELECT id FROM site WHERE site_name = %s'
        cursor.execute(sql, (new_site_name))
        data_id_list = cursor.fetchall() # [{'id': 1}]
        data_id_dir = data_id_list[0] # {'id': 1}
        site_id = data_id_dir['id'] # 1 int
        

    rating = input('请输入您对该 keyword 的喜爱程度（1 - 5）：').strip()
    image_path = input('请输入照片地址：').strip()
    image_path = image_path if image_path else None
    remark = input('请输入您对该 keyword 的备注：')

    sql = '''
INSERT keyword(keyword_name, site_id, rating, image_path, remark)
VALUE
(%s,%s,%s,%s,%s)
'''
    cursor.execute(sql,(keyword_name, site_id, rating, image_path, remark))
    conn.commit()
    print('已成功添加！\n')
    cursor.close()
    conn.close()

def update_keyword():
    with connect_database() as conn:
        cursor = conn.cursor()
        sql = '''
SELECT k.id, k.keyword_name, s.site_name, k.rating
FROM keyword k
JOIN site s ON k.site_id = s.id
'''
        cursor.execute(sql)

        # Make the output look better
        # data: [{'keyword_name': 'Yummy', 'site_name': 'Telegram', 'rating': 5, 'create_at': datetime.datetime(2025, 12, 3, 10, 57, 16)}]
        data = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ['id', 'keyword', '网站', '喜爱程度']
        for row in data:
            table.add_row(row.values())
        print(table)

    choice_keyword = input('请输入你想修改的 keyword：').strip()
    try:
        int(choice_keyword)
    except ValueError as e:
        map_keyword_id_name(choice_keyword)

    print('------请输入修改后的数据------')
    name = input('keyword: ')

    # Determine which site you want to change to.
    query_site()
    site = input('网站：')
    try:
        int(site)
    except ValueError as e:
        site = map_site_id_name(site)
    
    rating = input('喜爱程度：')
    remark = input('备注：')

    sql = '''
UPDATE keyword
SET keyword_name = %s, site_id = %s, rating = %s, remark = %s
WHERE id = %s
'''
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(sql, (name, site, rating, remark, choice_keyword))
    conn.commit()
    print('已成功修改√\n')
    cursor.close()
    conn.close()


def query_keyword():
    conn = connect_database()
    cursor = conn.cursor()
    sql = 'SELECT * FROM view_default'
    cursor.execute(sql)

    # Make the output look better
    # data: [{'keyword_name': 'Yummy', 'site_name': 'Telegram', 'rating': 5, 'create_at': datetime.datetime(2025, 12, 3, 10, 57, 16)}]
    data = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ['keyword', '网站', '喜爱程度', '创建时间']
    for row in data:
        table.add_row(row.values())
    print(table)

    cursor.close()
    conn.close()

def query_site():
    conn = connect_database()
    cursor = conn.cursor()
    sql = 'SELECT * FROM site'
    cursor.execute(sql)

    # Make the output look better
    #data: [{'id': 1, 'site_name': 'Telegram', 'url': 'web.telegram.org', 'quick_search': 'no'}]
    data = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ['id', '网站名称']
    for site in data:
        table.add_row([site['id'], site['site_name']])
    print(table)

    cursor.close()
    conn.close()

def query_by_site():
    query_site()
    by_site = input('请输入你想查看哪个网站下的 keyword：')
    # Determine if it is a number or a name
    try:
        int(by_site)
        sql = '''
SELECT k.keyword_name, s.site_name, k.rating, k.create_at
FROM keyword k
JOIN site s ON k.site_id = s.id
WHERE s.id = %s
'''
    except ValueError as e:
        sql = 'SELECT * FROM view_default WHERE site_name = %s'

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(sql, by_site)
    data = cursor.fetchall() # [{'keyword_name': '紫雨艾尔登法环', 'site_name': 'bilibili', 'rating': 3, 'create_at': datetime.datetime(2025, 12, 3, 12, 0, 1)}, {'keyword_name': '木鱼水心 是大臣', 'site_name': 'bilibili', 'rating': 4, 'create_at': datetime.datetime(2025, 12, 3, 14, 36, 25)}]

    # Determine if input exists
    if data == ():
        print('输入不存在，请检查👀')
        return()

    # Make the output look better
    table = PrettyTable()
    table.field_names = ['keyword', '网站', '喜爱程度', '创建时间']
    for row in data:
        table.add_row(row.values())
    print(table)
    cursor.close()
    conn.close()

def query_by_rating():
    by_rating = input('请输入你想查看喜爱程度几分的 keyword（1-5）：')

    conn = connect_database()
    cursor = conn.cursor()
    sql = 'SELECT * FROM view_default WHERE rating = %s'
    cursor.execute(sql, by_rating)
    data = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ['keyword', '网站', '喜爱程度', '创建时间']
    for row in data:
        table.add_row(row.values())
    print(table)
    cursor.close()
    conn.close()

def fuzzy_search():
    # fuzzy search keyword
    pass

def main():
    name = map_keyword_id_name('4')
    print(name)

if __name__ == '__main__':
    main()