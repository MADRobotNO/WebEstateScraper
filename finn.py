import requests
from bs4 import BeautifulSoup
from MySQLScrap import Database
import datetime

date = datetime.date.today()

database = Database()
database.connect_to_db()

base_url = "https://www.finn.no/realestate/homes/search.html?location=0.20015&location=1.20015.20287&" \
           "location=1.20015.20285&location=1.20015.20284&location=1.20015.20286&location=1.20015.20283&" \
           "location=1.20015.20288&location=1.20015.20289&page="
            #Volda

request = requests.get(base_url)
content = request.content
soup = BeautifulSoup(content, "html.parser")
page_nr = soup.find_all("a", {"class": "phs valign-middle"})[-1].text
page_nr = int(page_nr)
print("Analysing page. Please wait.")
counter = 0
for page in range(1, page_nr):
    print(page)
    request = requests.get(base_url+str(page))
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    all_items = soup.find_all("div", {"class": "unit flex align-items-stretch result-item"})
    if not all_items:
        break
    else:
        for item in all_items:
            m = []

            #location m[0]
            location = item.find("div",{"class":"licorice valign-middle"}).text
            if "," in location:
                coma_position = (location.rfind(","))+2
                m.append(location[coma_position:])
            else:
                m.append(location)
                
            #estate type m[1]
            estate_type = item.find("ul", {"class":"d1 licorice man fleft"}).text
            types = ["Enebolig", "Tomannsbolig", "Leilighet", "Rekkehus", "Andre", "Hyttetomt", "Gårdsbruk/Småbruk"]
            matches = [x for x in types if x in estate_type]
            if not matches:
                estate_type = None
                m.append(estate_type)
            else:
                estate_type = matches[0]
                m.append(estate_type)
                
            #size and price m[2]=size, m[3]=price
            size_and_price = item.find("p", {"class", "t5 word-break mhn"}).text.replace(",-", "").replace(" ", "")\
                .replace("m²", "").replace(u'\xa0', "").split('\n')
            if len(size_and_price) == 3:
                size_and_price = None
                m.append(size_and_price)
                m.append(size_and_price)   # twice, one for price and one for size
            elif len(size_and_price) == 4:
                del size_and_price[0], size_and_price[-1]
                both_sizes = size_and_price[0]
                both_prices = size_and_price[1]
                find_coma_in_sizes = both_sizes.find("-")
                find_coma_in_price = both_prices.find("-")
                if size_and_price[0].find("-") > 0 and size_and_price[1].find("-") > 0:
                    size_and_price[0] = both_sizes[0:find_coma_in_sizes]
                    size_and_price[1] = both_prices[0:find_coma_in_price]
                    m.append(size_and_price[1])   #price
                    m.append(size_and_price[0])   #size
                elif size_and_price[0].find("-") > 0:
                    size_and_price[0]=both_sizes[0:find_coma_in_sizes]
                    m.append(size_and_price[1])
                    m.append(size_and_price[0])
                elif size_and_price[1].find("-") > 0:
                    size_and_price[1]=both_prices[0:find_coma_in_price]
                    m.append(size_and_price[1])
                    m.append(size_and_price[0])
                else:
                    if size_and_price[1] == "Solgt":
                        size_and_price = None
                        m.append(size_and_price)
                        m.append(size_and_price)
                    else:
                        m.append(size_and_price[1])  #price
                        m.append(size_and_price[0])  #size
            else:
                size_and_price = None
                m.append(size_and_price)
                m.append(size_and_price)
            #price = size_and_price[1]
            #size = size_and_price[0]

            #price per kvm m[4]
            if size_and_price is None:
                price_per_kvm = None
                m.append(price_per_kvm)

            elif size_and_price[0] == 0 or size_and_price[1] == 0:
                price_per_kvm = None
                m.append(price_per_kvm)

            else:
                price_per_kvm = int(size_and_price[1])/int(size_and_price[0])
                price_per_kvm = int(price_per_kvm)
                m.append(price_per_kvm)

            #bedroom m[5]
            if item.find("li", {"data-automation-id": "bottomRow2"}) is not None:

                bedroom = item.find("li", {"data-automation-id": "bottomRow2"}).text
                bedroom_in_text = bedroom.find("soverom")

                if bedroom_in_text == -1:
                    bedroom = None
                    m.append(bedroom)
                else:
                    bedroom = bedroom[-9:-8]
                    m.append(bedroom)

                
            #date m[6]
            m.append(date)

            #description m[7]
            description = item.find("h3").text.replace("  ", " ").replace(u'\xa0', "")
            m.append(description)

            #save to database
            list_of_values_to_check = [m[1], m[2], m[3], m[4]]
            a = None
            check_if_none = a in list_of_values_to_check
            #print(check_if_none)
            if check_if_none:
                #print("Item has no value and is being dropped:", m)
                pass
            else:
                if (database.check_if_exists(m[7])) is None:
                    print("Item has been added:", m)
                    database.insert_to_db(m[0], m[1], m[2], m[3], m[4], m[5], m[6],m[7])
                    counter += 1
                else:
                    #print("Item exists")
                    pass
if counter:
    print("Items added: ", counter)
else:
    print("Items added:", None)
database.close_db()
print("Analyse done!")
