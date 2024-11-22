from flask import *
from flask_login import * # implement user login feature
from pymongo import MongoClient # connect to mongodb
from flask_bcrypt import Bcrypt # encrypt user account password
from bson.objectid import ObjectId # 12 bit binary BSON code

app = Flask(__name__)
app.secret_key = "root"

# creating a loginmanager instance
login_manager = LoginManager()
login_manager.init_app(app) # initializing loginmanager with the application
login_manager.login_view = 'login'

# password hashing
bcrypt = Bcrypt(app)

client = MongoClient('mongodb://localhost:27017')
db1 = client['employee_auth'] #name of database is 'employee_auth'
collection1 = db1['employee_user'] # connecting to 'employee_users' collection

# collect data from table via 'business_produce' db and 'produce_details' collection
db2 = client['business_produce']
collection2 = db2['produce_details']

# creating a user class for Flask-login
class User(UserMixin):
    def __init__(self, user):
        self.id = str(user['_id']) # conversion to string since id will always be a string value esp in mongodb1
        self.username = user['username']

    def get_id(self):
        return self.id

# retrieving a user via Flask-login using loader
@login_manager.user_loader
def load_user(user_id):
    user = collection1.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user)
    return None

# route for user registration
@app.route('/user_account_registration', methods=['GET', 'POST'])
def user_account_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']

        # check if username already exists
        if collection1.find_one({'username': username}):
            flash('Username is already in use. '
                  'Please choose a different one.')
        else:
            # credentials sent to database
            collection1.insert_one({'username': username,
                                   'password1': bcrypt.generate_password_hash(password).decode('utf-8')
                                   })

            flash('Account registered successfully. Please proceed to log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']

        # check if username and password match
        user = collection1.find_one({'username': username})
        # also making sure hashed password entry matches with what is in the database
        if user and bcrypt.check_password_hash(user['password1'], password):
            login_user(User(user))
            return redirect("/layout")
        else:
            flash('Invalid username/password. Please try again', 'danger')

    return render_template('login.html')

# user account layout
@app.route('/layout')
@login_required
def layout():
    # number of results/items per page
    items_per_page = 50

    # get current page number from query parameters, set default to = 1
    page = int(request.args.get('page', 1))

    # skip items
    skip_items = (page - 1) * items_per_page

    # search query as the default result is empty to start with (pagination)
    search_query = request.args.get('search', '').strip()

    # mongodb query to filter by product search
    query = {}
    if search_query:
        query = {
            "$or" : [
                {"Product": {"$regex": f"^{search_query}", "$options": "i"}},
                {"Price": {"$regex": search_query, "$options": "i"}},
                {"Currency": {"$regex": f"^{search_query}", "$options": "i"}},
                {"Imported From": {"$regex": search_query, "$options": "i"}},
                {"Country Code": {"$regex": f"^{search_query}", "$options": "i"}},
                {"Import Date": {"$regex": search_query, "$options": "i"}},
                {"Time of Import": {"$regex": f"^{search_query}", "$options": "i"}},
                {"In Stock": {"$regex": search_query, "$options": "i"}}
            ]
        }

    # grab data from mongodb - business database, specifically the product and list in asc order
    data = list(collection2.find(query).sort("Product", 1).skip(skip_items).limit(items_per_page))

    # total count of matching items/produce
    total_items = collection2.count_documents(query)
    total_pages = (total_items + items_per_page - 1) // items_per_page # results/items per page

    # column to check for duplicates = Product
    target_field = "Produce"


    # render the template
    return render_template('layout.html',
                           username=current_user.username,
                           data=data,
                           page=page,
                           total_pages=total_pages,
                           search_query=search_query,
                           )

# logout route
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user() # logout_user method invoked once user logs off
    flash('Logged out successfully.')
    return redirect(url_for("login")) # redirects user to login page


# run the app
if __name__ == '__main__':
    app.run(debug=True)