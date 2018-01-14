from flask import Flask, render_template
from MySQLScrap import Database
from MySQLScrapHamar import Database as DBH
import datetime

database = Database()
database_Hamar = DBH()
today_is = datetime.date.today()
database.connect_to_db()
app = Flask(__name__)

@app.route('/volda/')
def volda():

    list_of_prices_per_kvm = []
    list_of_prices = []
    list_of_prices_temp = database.get_prices()
    for prices in list_of_prices_temp:
        list_of_prices.append(prices[0])
    list_of_prices_per_kvm_temp = database.get_prices_per_kvm()
    for price in list_of_prices_per_kvm_temp:
        list_of_prices_per_kvm.append(price[0])
    average_price = int(sum(list_of_prices)/len(list_of_prices))
    average_price_per_kvm = int(sum(list_of_prices_per_kvm)/len(list_of_prices_per_kvm))
    num_of_el = len(list_of_prices)
    return render_template("volda.html", average_price=average_price, average_price_per_kvm=average_price_per_kvm,
                           list_of_prices=list_of_prices, list_of_prices_per_kvm=list_of_prices_per_kvm,
                           today_is=today_is, num_of_el=num_of_el)

@app.route('/hamar/')
def hamar():

    list_of_prices_per_kvm = []
    list_of_prices = []
    list_of_prices_temp = database_Hamar.get_prices()
    for prices in list_of_prices_temp:
        list_of_prices.append(prices[0])
    list_of_prices_per_kvm_temp = database_Hamar.get_prices_per_kvm()
    for price in list_of_prices_per_kvm_temp:
        list_of_prices_per_kvm.append(price[0])
    average_price = int(sum(list_of_prices)/len(list_of_prices))
    average_price_per_kim = int(sum(list_of_prices_per_kvm)/len(list_of_prices_per_kvm))
    num_of_el = len(list_of_prices)
    return render_template("hamar.html", average_price=average_price, average_price_per_kvm=average_price_per_kim,
                           list_of_prices=list_of_prices, list_of_prices_per_kvm=list_of_prices_per_kvm,
                           today_is=today_is, num_of_el=num_of_el)


@app.route('/volda/voldaorsta/')
def voldaorsta():

    list_of_prices_per_kvm = []
    list_of_prices = []
    list_of_prices_temp = database_Hamar.send_commmand("SELECT price FROM estates WHERE location='Volda' "
                                                       "OR location='Ørsta'")
    for prices in list_of_prices_temp:
        list_of_prices.append(prices[0])
    list_of_prices_per_kvm_temp = database_Hamar.send_commmand("SELECT price_per_kvm FROM estates "
                                                               "WHERE location='Volda' OR location='Ørsta'")
    for price in list_of_prices_per_kvm_temp:
        list_of_prices_per_kvm.append(price[0])
    average_price = int(sum(list_of_prices)/len(list_of_prices))
    average_price_per_kim = int(sum(list_of_prices_per_kvm)/len(list_of_prices_per_kvm))
    num_of_el = len(list_of_prices)
    return render_template("voldaorsta.html", average_price=average_price, average_price_per_kvm=average_price_per_kim,
                           list_of_prices=list_of_prices, list_of_prices_per_kvm=list_of_prices_per_kvm,
                           today_is=today_is, num_of_el=num_of_el)


@app.route('/hamar/whamar/')
def whamar():

    list_of_prices_per_kvm = []
    list_of_prices = []
    list_of_prices_temp = database_Hamar.send_commmand("SELECT price FROM estates_Hamar WHERE NOT location='Hamar' "
                                                       "AND NOT location='Ottestad' AND NOT location='Brumunddal'")
    for prices in list_of_prices_temp:
        list_of_prices.append(prices[0])
    list_of_prices_per_kvm_temp = database_Hamar.send_commmand("SELECT price_per_kvm FROM estates_Hamar WHERE "
                                                               "NOT location='Hamar' AND NOT location='Ottestad' "
                                                               "AND NOT location='Brumunddal'")
    for price in list_of_prices_per_kvm_temp:
        list_of_prices_per_kvm.append(price[0])
    average_price = int(sum(list_of_prices)/len(list_of_prices))
    average_price_per_kim = int(sum(list_of_prices_per_kvm)/len(list_of_prices_per_kvm))
    num_of_el = len(list_of_prices)
    return render_template("whamar.html", average_price=average_price, average_price_per_kvm=average_price_per_kim,
                           list_of_prices=list_of_prices, list_of_prices_per_kvm=list_of_prices_per_kvm,
                           today_is=today_is, num_of_el=num_of_el)

@app.route('/')
def home():
    return render_template("home.html", today_is=today_is)

@app.route('/data/')
def data():
    columns_in_db = database.show_columns()
    data1 = list(database.view_db())
    return render_template("data.html", col=columns_in_db, df=data1, today_is=today_is)

@app.route('/data/voldaorsta')
def data_voldaorsta():
    columns_in_db = database.show_columns()
    data1 = list(database.send_commmand("SELECT * FROM estates WHERE location='Volda' OR location='Ørsta'"))
    return render_template("data.html", col=columns_in_db, df=data1, today_is=today_is)

@app.route('/data_hamar/')
def data_hamar():
    columns_in_db = database_Hamar.show_columns()
    data1 = list(database_Hamar.view_db())
    return render_template("data.html", col=columns_in_db, df=data1, today_is=today_is)

@app.route('/data_whamar/')
def data_whamar():
    columns_in_db = database_Hamar.show_columns()
    data1 = list(database_Hamar.send_commmand("SELECT * FROM estates_Hamar WHERE NOT location='Hamar' AND "
                                              "NOT location='Ottestad' AND NOT location='Brumunddal'"))
    return render_template("data.html", col=columns_in_db, df=data1, today_is=today_is)


if __name__ == "__main__":
    app.run(debug=True)