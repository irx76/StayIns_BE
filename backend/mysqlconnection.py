from flask import Flask,request,jsonify
import json
import pymysql
import base64

app=Flask(__name__)

def connect():
    conn=None
    try:
        # conn=pymysql.connect(
        #                     host="sql12.freesqldatabase.com",
        #                     database= "sql12714571",
        #                     user= "sql12714571",
        #                     password= "qQ2DzVIv3i",
        #                     port=3306,
        #                     charset='utf8mb4',
        #                     cursorclass=pymysql.cursors.DictCursor
        #                     )
        conn=pymysql.connect(
                            host="127.0.0.1",
                            database= "stayins",
                            user= "root",
                            password= "",
                            port=8889,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                            )
        # conn=pymysql.connect(
        #                     host="http://mysql-stay-ins.alwaysdata.net",
        #                     database= "stay-ins_website",
        #                     user= "Stay-ins_home",
        #                     password= "Stayins@7",
        #                     port=3306,
        #                     charset='utf8mb4',
        #                     cursorclass=pymysql.cursors.DictCursor
                            # )
    except pymysql.Error as e:
        print(e)
    return conn

@app.route('/', methods=['GET'])
def get_jobs():
    conn=connect()
    cursor=conn.cursor()

    param=request.args.get('param')

    
    # if param == 'locations_list':
    #     cursor.execute("SELECT * FROM Location") 
    #     locations = [
    #         dict(Location=row['LOCATION'])
    #         for row in cursor.fetchall()
    #     ]
    #     if locations is not None:
    #         return jsonify(locations)
    #     return "No jobs found", 404
    
    if param == "Cities_call":
        cursor.execute("SELECT name_en FROM cities ORDER BY name_en ASC")
        cities = [dict(name_en=row['name_en']) for row in cursor.fetchall()]
        if cities:
            return jsonify(cities)
        return "No cities found", 404
    
    elif param == "BoardingsAround":
        UserCompoundCode = request.args.get('UserCompoundCode')
        query = "SELECT id,city,boardingType,boarderType,monthlyFee,keyMoney,description,size,image1,image2,image3,image4,image5,image6 from boarding,images WHERE lower(boarding.city) LIKE CONCAT('%%', LOWER(%s),'%%') AND boarding.imageId=images.imageId;"
        cursor.execute(query, (UserCompoundCode,))
        boardings = []
        for row in cursor.fetchall():
            image1_base64 = base64.b64encode(row['image1']).decode('utf-8')
            image2_base64 = base64.b64encode(row['image2']).decode('utf-8')
            image3_base64 = base64.b64encode(row['image3']).decode('utf-8')
            image4_base64 = base64.b64encode(row['image4']).decode('utf-8')
            image5_base64 = base64.b64encode(row['image5']).decode('utf-8')
            image6_base64 = base64.b64encode(row['image6']).decode('utf-8')
            boardings.append(dict(id=row['id'], city=row['city'], boardingType=row['boardingType'], boarderType=row['boarderType'], monthlyFee=row['monthlyFee'], keyMoney=row['keyMoney'], description=row['description'], size=row['size'], image1=image1_base64, image2=image2_base64, image3=image3_base64, image4=image4_base64, image5=image5_base64, image6=image6_base64))
        if boardings:
            return jsonify(boardings)
        return "No boardings found", 404
    

@app.route('/search', methods=['GET'])
def getBoardings():
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("SELECT id,city,boardingType,boarderType,monthlyFee,keyMoney,description,size,image1,image2,image3,image4,image5,image6 from boarding,images WHERE boarding.imageId=images.imageId;")
    boardings = []
    for row in cursor.fetchall():
            image1_base64 = base64.b64encode(row['image1']).decode('utf-8')
            image2_base64 = base64.b64encode(row['image2']).decode('utf-8')
            image3_base64 = base64.b64encode(row['image3']).decode('utf-8')
            image4_base64 = base64.b64encode(row['image4']).decode('utf-8')
            image5_base64 = base64.b64encode(row['image5']).decode('utf-8')
            image6_base64 = base64.b64encode(row['image6']).decode('utf-8')
            boardings.append(dict(id=row['id'], city=row['city'], boardingType=row['boardingType'], boarderType=row['boarderType'], monthlyFee=row['monthlyFee'], keyMoney=row['keyMoney'], description=row['description'], size=row['size'], image1=image1_base64, image2=image2_base64, image3=image3_base64, image4=image4_base64, image5=image5_base64, image6=image6_base64))
    if boardings:
        return jsonify(boardings)
    return "No boardings found", 404

if __name__ == '__main__':
    app.run(debug=True)