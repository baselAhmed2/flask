from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

current_time = datetime.now()
shope = Flask(__name__)

@shope.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        item_name = request.form.get("item_name")
        item_price = request.form.get("item_price")
        product_number = int(request.form.get("product_number"))
        user_name = request.form.get("user_name")

        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (user_name TEXT, name TEXT, price INTEGER, product_number INTEGER, time TEXT)")
        
        cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
        existing_item = cursor.fetchone()

        if existing_item: 
            new_product_number = existing_item[3] + product_number
            cursor.execute("UPDATE items SET product_number=? WHERE name=?", (new_product_number, item_name))
        else:
            cursor.execute("INSERT INTO items (user_name, name, price, product_number, time) VALUES (?, ?, ?, ?, ?)", (user_name, item_name, item_price, product_number, current_time))

        db.commit()
        db.close()

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    db.close()

    return render_template("index.html", pagetitle="Cart Items", items=items)

@shope.route("/edit_item", methods=["POST"])
def edit_item():
    if request.method == "POST":
        item_name = request.form.get("item_name")
        new_quantity = int(request.form.get("new_quantity"))

        db = sqlite3.connect('database.db')
        cursor = db.cursor()

        if new_quantity == 0:
            cursor.execute("DELETE FROM items WHERE name=?", (item_name,))
        else:
            cursor.execute("UPDATE items SET product_number=? WHERE name=?", (new_quantity, item_name))
            
        db.commit()
        db.close()

        return redirect(url_for('homepage'))

if __name__ == '__main__':
    shope.run(debug=True)
