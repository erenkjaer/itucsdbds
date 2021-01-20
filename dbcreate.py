import psycopg2 as dbapi2

URL="postgres://mscrlztk:j9PwWtS-g7dCBt9DxTsnO1GSRGDjgSJ-@kandula.db.elephantsql.com:5432/mscrlztk"

restaurant_list=[
{'restaurantname':"GORDON BIERSCH RESTAURANT & BREWERY"	,
'address':"100 M ST SE WASHINGTON, DC 20003",
'phonenumber':	"12025096995"},
{'restaurantname':"PAUL BAKERY"	,
'address':"1000 CONNECTICUT AVE NW WASHINGTON, DC 20006",
'phonenumber':	"12024885741"
},
{'restaurantname':"PIZZA AUTHENTICA",
'address':"1015 15TH ST NW WASHINGTON, DC 20005",
'phonenumber':"12026944851"},
{'restaurantname':"MCDONALD'S",
'address':"1000 O ST SE Washington, DC 20003",
'phonenumber':"12025448751"
},
{'restaurantname':"COPYCAT CO.",
'address':"1110 H ST NE WASHINGTON, DC 20002",
'phonenumber':"12026194201"},
{'restaurantname':"ASCOT RESTAURANT",
'address':"1050 17TH ST NW Washington, DC 20036",
'phonenumber':"12024207865"},
{'restaurantname':"STAN'S RESTAURANT",
'address':"1029 VERMONT AVE NW Washington, DC 20005",
'phonenumber':"12025046262"},
{'restaurantname':"STARBUCKS",
'address':"1001 CONNECTICUT AVE NW Washington, DC 20036",
'phonenumber':"12025091396"}
]
feature_list=[
{'feature': "Delivery",'restaurantid':1},
{'feature':"Takeout",'restaurantid':1},
{'feature':"Outdoor Seating",'restaurantid':1},
{'feature':"Delivery",'restaurantid':2},
{'feature':"Takeout",'restaurantid':2},
{'feature':"Delivery",'restaurantid':3},
{'feature':"Takeout",'restaurantid':3},
{'feature':"Accepts Cryptocurrency",'restaurantid':3},
{'feature':"Delivery",'restaurantid':4},
{'feature':"Takeout",'restaurantid':4},
{'feature':"Good for Kids",'restaurantid':4},
{'feature':"Takeout",'restaurantid':5},
{'feature':"Dogs Allowed",'restaurantid':6},
{'feature':"Liked by Vegetarians",'restaurantid':6},
{'feature':"Valet",'restaurantid':6},
{'feature':"Wheelchair Accessible",'restaurantid':6},
{'feature':"Delivery",'restaurantid':7},
{'feature':"Takeout",'restaurantid':7},
{'feature':"Takeout",'restaurantid':8},
{'feature':"Accepts Apple Pay",'restaurantid':8},
]


def createtables():
    with dbapi2.connect(URL) as connection:
        cursor = connection.cursor()
        statement = """
        CREATE TABLE IF NOT EXISTS users(
	    id SERIAL NOT NULL,
    	username VARCHAR(255) NOT NULL UNIQUE,
	    password VARCHAR(255) NOT NULL,
	    email VARCHAR(255)  UNIQUE,
	    PRIMARY KEY (id)
	    );"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()

    with dbapi2.connect(URL) as connection:
        cursor = connection.cursor()
        statement = """CREATE TABLE IF NOT EXISTS restaurants(
        id SERIAL NOT NULL,
        restaurantname VARCHAR(255) NOT NULL UNIQUE,
        phonenumber VARCHAR(255) NOT NULL UNIQUE,
        address VARCHAR(255) NOT NULL UNIQUE,
        PRIMARY KEY(id)
        );"""
        cursor.execute(statement)
        cursor.close()


    with dbapi2.connect(URL) as connection:
        cursor = connection.cursor()
        statement = """CREATE TABLE IF NOT EXISTS comments(
        id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255)  NOT NULL,
        restaurantname VARCHAR(255) NOT NULL,
        point INT NOT NULL,
        explanation text NOT NULL,
        FOREIGN KEY(username) REFERENCES users(username),
        FOREIGN KEY(restaurantname) REFERENCES restaurants(restaurantname)
        );"""
        cursor.execute(statement)
        cursor.close()


    with dbapi2.connect(URL) as connection:
        cursor = connection.cursor()
        statement = """   CREATE TABLE IF NOT EXISTS menus(
        id SERIAL NOT NULL,
        restaurantid INT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
        items VARCHAR(255) NOT NULL,
        PRIMARY KEY(id)
        );"""
        cursor.execute(statement)
        cursor.close()
    with dbapi2.connect(URL) as connection:
        cursor = connection.cursor()
        statement = """CREATE TABLE IF NOT EXISTS features(
        id SERIAL NOT NULL PRIMARY KEY,
        feature VARCHAR(255) NOT NULL,
        restaurantid INT NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE	
        );"""
        cursor.execute(statement)
        cursor.close()
    #with dbapi2.connect(URL) as connection:
    #    cursor = connection.cursor()
    #    statement = """CREATE TABLE IF NOT EXISTS orders(
    #    id SERIAL NOT NULL PRIMARY KEY,
    #    address VARCHAR(255) NOT NULL,
    #    restaurantname VARCHAR(255) NOT NULL ,
    #    price INT NOT NULL,	
    #    FOREIGN KEY(restaurantname) REFERENCES restaurants(restaurantname)
    #    );"""
    #    cursor.execute(statement)
    #    cursor.close()
    #with dbapi2.connect(URL) as connection:
    #    cursor = connection.cursor()
    #    statement = """CREATE TABLE IF NOT EXISTS ordereditem(
    #   id SERIAL NOT NULL,
    #   item VARCHAR(255) NOT NULL,
    #   orderid INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    #   PRIMARY KEY(id)
    #   );"""
    #   cursor.execute(statement)
    #   cursor.close()
    with dbapi2.connect(URL) as connection:
        cursor=connection.cursor()        
        for item in restaurant_list:
            statement="""SELECT * FROM restaurants WHERE restaurantname=%s """
            cursor.execute(statement,(item['restaurantname'],))
            if not cursor.fetchone()[0]:
                statement= """INSERT INTO restaurants(restaurantname,phonenumber,address) VALUES (%s,%s,%s);"""
                cursor.execute(statement,(item['restaurantname'],item['phonenumber'],item['address']))
        cursor.close()
    with dbapi2.connect(URL) as connection:
        cursor=connection.cursor()
        for x in feature_list:
            statement="""INSERT INTO features(feature,restaurantid) VALUES (%s,%s)"""
            cursor.execute(statement,(x['feature'],x['restaurantid']))      
    
    return

