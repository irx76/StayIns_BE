import pymysql
import requests
from random import randint


# Image table structure
image_table = "Image"
image_id_col = "imageID"
image_cols = ["image1", "image2", "image3","image4","image5","image6"]  # Adjust based on actual number of BLOB columns

# Function to fetch random house image URL
def get_random_house_image():
  url = f"https://picsum.photos/seed/{randint(1,1000)}/200/150"  # Adjust dimensions as needed
  response = requests.get(url)
  if response.status_code == 200:
    return response.content
  else:
    print(f"Error fetching image: {response.status_code}")
    return None

# Connect to MySQL database
try:
    connection=pymysql.connect(
                                host="127.0.0.1",
                                database= "stayins",
                                user= "root",
                                password= "",
                                port=8889,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
                                )
    cursor = connection.cursor()
except pymysql.Error as err:
  print("Error connecting to database:", err)
  exit()

# Generate and insert dummy data
for i in range(1, 11):
  image_data = []
  for _ in range(len(image_cols)):
    image_data.append(get_random_house_image())
  if all(data is not None for data in image_data):  # Check if all images downloaded successfully
    insert_query = """INSERT INTO images (image1, image2, image3, image4, image5, image6)
VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, tuple(image_data))
    connection.commit()
  else:
    print(f"Error downloading image(s) for row {i}, skipping...")

# Close connection
cursor.close()
connection.close()

print("10 dummy image data rows inserted (if successful).")