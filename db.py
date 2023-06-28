import sqlite3

db = sqlite3.connect('new.db')
cur = db.cursor()
async def get_all_products():
    data = cur.execute("SELECT * from dictionary").fetchall()
    db.commit()



async def create_new_product(word,translation):
    data = cur.execute("INSERT INTO dictionary VALUES (?,?)",(word,translation))
    db.commit()





