from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# Use flask_pymongo to set up mongo connection
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

# db = client.mars_db
db = mongo.db

# db.team.insert_many(mars_dictionary)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_dictionary = mongo.db.mars_dictionary.find_one()
    return render_template("index.html", mars_dictionary=mars_dictionary)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_route():

    # Run the scrape function and save the results to a variable
    mars_dictionary = mongo.db.mars_dictionary
    mars_data = scrape_mars.scrape()
    mars_dictionary.replace_one({}, mars_data, upsert=True)
    return redirect("/", code=302)

    # Update the Mongo database using update and upsert=True
    # @TODO: YOUR CODE HERE!

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)