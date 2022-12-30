from random import randint
import psycopg2
global man_name
global girl_name
global last_name_man
global last_name_girl
global products
global email_index
global staffs
global con
global cur


con = psycopg2.connect(
    database="mini_shop",
    user=f"postgres",
    password=f"pass",
    host="127.0.0.1",
    port="5432"
)
cur = con.cursor()

man_name = ['Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей', 'Алексей', 'Артём', 'Илья', 'Кирилл', 'Михаил', 'Никита', 'Матвей', 'Роман', 'Егор', 'Арсений', 'Иван', 'Денис', 'Евгений', 'Даниил', 'Тимофей']
girl_name = ['Анастасия', 'Мария', 'Елена', 'Дарья', 'Алина', 'Ирина', 'Екатерина', 'Арина', 'Полина', 'Ольга', 'Юлия', 'Татьяна', 'Наталья', 'Виктория', 'Елизавета', 'Ксения', 'Милана', 'Вероника', 'Алиса', 'Валерия']
last_name_man = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Федоров', 'Морозов', 'Волков', 'Алексеев', 'Лебедев', 'Семенов', 'Егоров', 'Павлов', 'Козлов', 'Степанов', 'Николаев', 'Орлов', 'Андреев', 'Никитин', 'Захаров', 'Зайцев', 'Соловьев', 'Борисов', 'Яковлев', 'Григорьев', 'Романов', 'Воробьев', 'Сергеев', 'Кузьмин', 'Фролов', 'Александров', 'Дмитриев', 'Королев', 'Гусев', 'Киселев']
last_name_girl = ['Иванова', 'Смирнова', 'Кузнецова', 'Попова', 'Васильева', 'Петрова', 'Соколова', 'Михайлова', 'Новикова', 'Федорова', 'Морозова', 'Волкова', 'Алексеева', 'Лебедева', 'Семенова', 'Егорова', 'Павлова', 'Козлова', 'Степанова', 'Николаева', 'Орлова', 'Андреева', 'Никитина', 'Захарова', 'Зайцева', 'Соловьева', 'Борисова', 'Яковлева', 'Григорьева', 'Романова', 'Воробьева', 'Сергеева', 'Кузьмина', 'Фролова', 'Александрова', 'Дмитриева', 'Королева', 'Гусева', 'Киселева']
products = ['Спаржи', 'Сладкого перца', 'Брокколи', 'Моркови', 'Цветная капусты', 'Огурцов', 'Чеснока', 'Имбиря', 'Лука', 'Томатов', 'Бататов', 'Стручковой фасоли', 'Яблок', 'Авокадо', 'Бананов', 'Черника', 'Апельсинов', 'Клубники', 'Чечевицы', 'Фасоли', 'Коричневого риса', 'Овёса', 'Киноа', 'Миндаля', 'Семян чиа', 'Кокоса', 'Макадами', 'Грецкого ореха', 'Арахиса', 'Тёмного шоколада', 'Многозернового хлеба', 'Оливковкого масла', 'Кокосового масла', 'Сыра', 'Йогурта', 'Сливочного масла', 'Молока', 'Яйц', 'Курятины', 'Ягнятины', 'Говядины', 'Лосося', 'Сардин', 'Моллюсков', 'Креветок', 'Форели', 'Тунеца']
email_index = ['gmail.com', 'mail.ru', 'list.ru', 'bk.ru', 'yandex.ru', 'hotmail.com']
staffs = [['vadimKrasnov', 'Krasnov!_20','Вадим','Краснов','manager'],
         ['zaxarKabanov', 'Kaban2000_u!tra','Захар','Кабанов','clerk']]








#генерация клиентов
def visitor_generation(count):
    for i in range(count):
        a = randint(0, 19)
        b = randint(0, 19)
        c = randint(0, 5)
        name = man_name[a]
        last_name = last_name_man[b]
        number = randint(1000000, 9999999)
        date = f'2022-{randint(10, 12)}-0{randint(1, 9)}'
        cur.execute(
            f"INSERT INTO buyer (email, phone_number,first_name_buyer,last_name_buyer,total_amount_of_purchases, date_of_registration) "
            f"VALUES ('{name}_{last_name}{randint(1, 199)}@{email_index[c]}','7910{number}', '{name}', '{last_name}', {randint(1000, 100000)}, '{date}');"
        )
        con.commit()
# #генерация асортимета и его характеристик
def arotimet_generation():
    count_id = 0
    for product in products:
        count_id+=1
        b = randint(1,4)
        t = True
        quantities_in_stock = randint(1, 1000)
        purchase_price_product = randint(100, 1500)
        cost_product = purchase_price_product * float(f'1.{randint(1,99)}')
        if b == 1:
            t = False
            quantities_in_stock = 0
        cur.execute(
            f"INSERT INTO assortment (id_product, name_product, cost_product, availability) "
            f"VALUES ({count_id}, 'Пачка {product.lower()}', {randint(100, 1500)}, {t});"
        )
        con.commit()
        cur.execute(
            f"INSERT INTO additional_product_information (id_product, quantities_in_stock, purchase_price_product,dimensions_product, postavshik) "
            f"VALUES ({count_id},{quantities_in_stock},{purchase_price_product},'{randint(5,40)}x{randint(5,40)}x{randint(5,40)}', 'ИП {last_name_man[randint(0,len(last_name_man)-1)]}');")
        con.commit()
#генерация работников
def employee_generation():
    for staff in staffs:
        cur.execute(
            f"call add_staff('{staff[0]}', '{staff[1]}','{staff[2]}','{staff[3]}','{staff[4]}');")
        con.commit()

arotimet_generation()
employee_generation()
visitor_generation(1000)
# cur.execute(
#             f"select name_product, quantity, cost_product, (cost_product*quantity)  from (select name_product, id_check, quantity, cost_product from assortment inner join purchase on assortment.id_product = purchase.id_product)as food where id_check =  (select MAX(""id_check"") from ""purchase"");")
# print(cur.fetchall())