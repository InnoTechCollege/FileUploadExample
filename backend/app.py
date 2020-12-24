from flask import Flask, request, Response
from flask_cors import CORS
import json
import mariadb
import dbcreds
import string
import random
import os


def generateRandomFileName():
    letters_and_digits = string.ascii_letters + string.digits
    return "".join((random.choice(letters_and_digits) for i in range(75)))


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./userImages"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


@app.route("/api/products", methods=["GET", "POST"])
def products_endpoint():
    if request.method == "POST":
        if "image" not in request.files:
            return Response(
                json.dumps("You need to send an image!", default=str),
                mimetype="application/json",
                status=400,
            )
        product_image = request.files["image"]
        if product_image.filename == "":
            return Response(
                json.dumps("You need to send an image!", default=str),
                mimetype="application/json",
                status=400,
            )
        image_filetype = product_image.filename.rsplit(".", 1)[1].lower()
        if image_filetype not in ALLOWED_EXTENSIONS:
            return Response(
                json.dumps("You need to send a valid image type!", default=str),
                mimetype="application/json",
                status=400,
            )
        cursor = None
        conn = None
        product_id = -1
        errored = False
        product_name = request.form.get("name")
        product_description = request.form.get("description")
        product_image_filename = generateRandomFileName() + "." + image_filetype
        # Finally we are ready to actually store the information in the DB and the image in the folder
        try:
            conn = mariadb.connect(
                user=dbcreds.user,
                password=dbcreds.password,
                host=dbcreds.host,
                port=dbcreds.port,
                database=dbcreds.database,
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (image, name, description) VALUES (?,?,?)",
                [product_image_filename, product_name, product_description],
            )
            conn.commit()
            product_id = cursor.lastrowid
            if product_id != -1:
                product_image.save(os.path.join(UPLOAD_FOLDER, product_image_filename))
        except Exception as err:
            print("Error selecting products")
            print(err)
            errored = True
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.close()
            if errored:
                return Response(
                    json.dumps("Something has gone wrong!", default=str),
                    mimetype="application/json",
                    status=500,
                )
            if product_id != -1:
                return Response(
                    json.dumps(
                        [
                            product_id,
                            product_name,
                            product_description,
                            product_image_filename,
                        ],
                        default=str,
                    ),
                    mimetype="application/json",
                    status=200,
                )
            else:
                return Response(
                    json.dumps("Something has gone wrong!", default=str),
                    mimetype="application/json",
                    status=500,
                )
    elif request.method == "GET":
        cursor = None
        conn = None
        products = None
        errored = False
        try:
            conn = mariadb.connect(
                user=dbcreds.user,
                password=dbcreds.password,
                host=dbcreds.host,
                port=dbcreds.port,
                database=dbcreds.database,
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
        except Exception as err:
            print("Error selecting products")
            print(err)
            errored = True
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.close()
            if errored:
                return Response(
                    json.dumps("Something has gone wrong!", default=str),
                    mimetype="application/json",
                    status=500,
                )
            if len(products) > 0:
                return Response(
                    json.dumps(products, default=str),
                    mimetype="application/json",
                    status=200,
                )
            else:
                return Response(
                    json.dumps("Something has gone wrong!", default=str),
                    mimetype="application/json",
                    status=500,
                )