# Imports
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import sqlalchemy
from Getting_addresses_from_pictures import get_coordinates, get_address, get_addresses
from Getting_zillow_information_from_address import get_zillow_info
from forms import RegistrationForm, LoginForm, AddressForm
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
import os
import time

# For uploading the photo
UPLOAD_FOLDER = '/uploads/user-photos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# For satellite images
SAT_FOLDER = os.path.join('static', 'sat-images')

# Instantiate flask app
app = Flask(__name__)

# Configure the upload  & sat image folders
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAT_FOLDER'] = SAT_FOLDER


# HOME PAGE
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@fema.gov' and form.password.data == 'password':
            flash('You have been successfully logged in!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# WELCOME PAGE
@app.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome')

 # ________________________________ Satellite section ___________________________________

# NEIGHBORHOOD PAGE
@app.route('/neighborhood')
def neighborhood():
    return render_template('neighborhood.html', title='Select Neighborhood')


# SATELLITE IMAGE PAGE
@app.route('/satellite')
def satellite():
    full_filename = os.path.join(app.config['SAT_FOLDER'], 'anacostia.jpg')
    return render_template('satellite.html', title='Satellite Imagery',
    satellite_image=full_filename, neighborhood_name='Anacostia'
    )


 # ___________________________ Damage assessment form section ______________________________


# UPLOAD PAGE
# Function adapted from: https://stackoverflow.com/questions/44926465/upload-image-in-flask
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('upload'))
        file = request.files['file']
        # If user does not select file, submit empty secure_filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload'))
        # If file allowed...
        if file and allowed_file(file.filename):
            # Save to upload folder
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash('Your photo has been uploaded.', 'success')
            # return redirect(url_for('verify'))
    return render_template('upload.html', title='Upload')

# VERIFY PAGE
@app.route('/verify', methods = ['GET', 'POST'])
def verify():
    form = AddressForm()
    if form.validate_on_submit():
        if form.address.data == 'address_1':
            #flash('Valid address. Next page under construction.', 'success')
            return redirect(url_for('report'))
        else:
            flash('Invalid address. Try again.', 'danger')
    return render_template('verify.html', title='Verify Address',form=form,
    address_1 = "3324 Dent Pl NW, Washington, DC 20007, USA",
    address_2 = "3330 Dent Pl NW, Washington, DC 20007, USA",
    address_3 = "3322 Dent Pl NW, Washington, DC 20007, USA",
    address_4 = "3331 Dent Pl NW, Washington, DC 20007, USA")

# REPORT PAGE
@app.route('/report', methods = ['GET', 'POST'])
def report():
   master_results = get_zillow_info('3318 Dent Pl NW', 20007)
   return render_template('report.html', title='Report',
   zillow_id = master_results['zpid'],
   zestimate_amount = master_results['current_value'],
   last_sold_price = master_results['last_sold'],
   last_sold_date = master_results['last_sold_date'],
   home_type = master_results['property_type'],
   year_built = master_results['year_built'],
   bedrooms = master_results['bedrooms'],
   bathrooms = master_results['bathrooms'],
   home_size = master_results['sqft'],
   property_size = master_results['lot_size'],
   address = '3324 Dent Pl NW, Washington, DC 20007',
   filename = 'gtown_house.jpg',
   name = 'gtown_house_goog.jpg')

# SUBMITTED PAGE
@app.route('/submitted', methods= ['GET','POST'])
def submitted():
    return render_template('submitted.html', title='Submitted')

if __name__ == '__main__':
    app.run(debug=True)
