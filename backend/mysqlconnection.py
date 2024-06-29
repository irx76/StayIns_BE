from flask import Flask,request,jsonify,make_response
from flask_cors import CORS
import json
import pymysql
import base64

app=Flask(__name__)
CORS(app)

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
        # conn=pymysql.connect(
        #                     host="127.0.0.1",
        #                     database= "stayins",
        #                     user= "root",
        #                     password= "",
        #                     port=8889,
        #                     charset='utf8mb4',
        #                     cursorclass=pymysql.cursors.DictCursor
        #                     )
        
        conn=pymysql.connect(
                            host="mysql-stayins.alwaysdata.net",
                            database= "stayins_database",
                            user= "stayins_irosh",
                            password= "465646564@Iir",
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


@app.route('/listyourproperty', methods=['POST'])
def listYourProperty():
    conn = connect()
    

    city = request.form.get('city')
    boardingType = request.form.get('boardingType')
    boarderType = request.form.get('boarderType')
    monthlyFee = request.form.get('monthlyFee')
    keyMoney = request.form.get('keyMoney')
    description = request.form.get('description')
    size = request.form.get('size')

    if not all([city, boardingType, boarderType, monthlyFee, keyMoney, description, size]):
        return "Missing fields", 400

    files = request.files.getlist('dropzone-file')
    if len(files) < 3:
        return "At least 3 images are required.", 400

    with conn.cursor() as cursor:
        # Prepare the images for insertion, filling in None for missing images
        images = [file.read() if file.filename != '' else None for file in files]
        # Ensure the list has exactly 6 elements, filling in None if necessary
        images += [None] * (6 - len(images))

        # Insert image data into the images table
        cursor.execute("INSERT INTO images (image1, image2, image3, image4, image5, image6) VALUES (%s, %s, %s, %s, %s, %s)", tuple(images))
        conn.commit()

        # Retrieve the last inserted imageId
        cursor.execute("SELECT imageId FROM images ORDER BY imageId DESC LIMIT 1")
        imageId = cursor.fetchone()['imageId']

        # Insert the property data into the boarding table
        cursor.execute("INSERT INTO boarding (city, boardingType, boarderType, monthlyFee, keyMoney, imageId, description, size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (city, boardingType, boarderType, monthlyFee, keyMoney, imageId, description, size))
        conn.commit()

    response_html = """
    <html>
        <body>
            <p>Your submission was successful!</p>
            <a href="http://127.0.0.1:5500/List%20your%20Property/List%20your%20property.html">Back to Form</a>
        </body>
    </html>
    """
    return make_response(response_html),200


if __name__ == '__main__':
    app.run(debug=True)

