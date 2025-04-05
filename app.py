from flask import Flask, flash, render_template, request, redirect, session, g, jsonify, url_for, send_file, make_response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from datetime import timedelta
from helper_functions import login_required, is_num, valid_extension
from cs50 import SQL
import re
from time import time
from datetime import datetime
import calendar 
import base64
import datetime as dt
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True  # Sessions will last beyond the browser session
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=6)  # Set session lifetime
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




db = SQL("sqlite:///finance_app.db")


app.secret_key = 'supersecretkey'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.before_request
def profile_picture():
    profile = None
    if 'user_id' in session:
        profile_picture = db.execute("SELECT profile_picture FROM users WHERE id = ?", session['user_id'])
        if len(profile_picture) == 1:
            g.profile = profile_picture[0]['profile_picture']
        else:
            g.profile = None

@app.route('/')
@login_required
def index():
    value = db.execute('SELECT * FROM transactions WHERE user_id= ?', session['user_id'])
    current_time = time() 
    income = [{'income_month': 0.0}, {'income_year': 0.0}]
    expense = [{'expense_month': 0.0}, {'expense_year': 0.0}]   
    current_year = datetime.now().year
    balance = 0
    current_month = datetime.today().month
    for val in value:
        db_date = datetime.strptime(val['date'],'%Y-%m-%d').date()
        if db_date.year == current_year:
            if  val['type'] == 'Income':
                if db_date.month == current_month:
                    income[0]['income_month'] += float(val['amount']) 
                income[1]['income_year'] += float(val['amount'])
            if val['type'] == 'Expense':
                if db_date.month == current_month:
                    expense[0]['expense_month'] += float(val['amount'])
                expense[1]['expense_year'] += float(val['amount'])
        balance = income[0]['income_month'] - expense[0]['expense_month']
    pie_chart_img_monthly = pie_chart_img_yearly = salary_chart_img = ''
    if len(value) != 0:
        pie_chart_img_monthly = pie_chart_monthly()
        pie_chart_img_yearly = pie_chart_yearly()
        salary_chart_img = salary_plot()

    return render_template("index.html", income=income, expense=expense, balance = balance, pie_chart_img_monthly=pie_chart_img_monthly, salary_chart_img=salary_chart_img, pie_chart_img_yearly=pie_chart_img_yearly)
def pie_chart_monthly():
    count = 0
    categories = {}
    current = datetime.now()
    values = db.execute('SELECT * FROM transactions WHERE user_id = ?', session['user_id'])
    primary_category_db = db.execute('SELECT DISTINCT primary_category FROM categories')
    primary_category_db = [primary['primary_category'] for primary in primary_category_db]
    for prim in primary_category_db:
        if prim not in categories:
            categories[prim] = 0
    for value in values:
        date = datetime.strptime(value['date'], '%Y-%m-%d').date()
        if value['type'] == 'Expense':
            count += 1
            primary_category = value['primary_category']
            amount = (value['amount'])
            if date.year == current.year and date.month == current.month:
                categories[primary_category] = 0            
                categories[primary_category] += float(amount)
    if count != 0:
        for keyy in list(categories.keys()):
            if categories[keyy] <= 0:
                del categories[keyy]
        pie_chart_name = list(categories.keys())
        pie_chart_values = list(categories.values())
        matplotlib.use('Agg')
        largest_val = pie_chart_values.index(max(pie_chart_values))
        explode = [0.09 if i == largest_val else 0 for i in range(len(pie_chart_values))]

        plt.figure(figsize=(10, 8))
        plt.pie(pie_chart_values, autopct = '%1.1f%%', shadow = True, labeldistance = 1.1, startangle = 90, radius=1.0,  textprops={'fontsize': 8}, explode=explode)
        plt.title('Pie chart of Monthly Expense')
        imgg = BytesIO()
        plt.legend(pie_chart_name, loc='upper left', fontsize='small', bbox_to_anchor=(1, 1)  )
        plt.savefig(imgg, format='png')
        plt.close()
        imgg.seek(0)
        im = base64.b64encode(imgg.read()).decode('utf-8')
        return im
    else:
        plt.figure(figsize=(10, 8))
        val = [1]
        plt.pie(val, autopct = '%1.1f%%', shadow = True, startangle = 90, radius=1.0,  textprops={'fontsize': 8})
        plt.title('Pie chart of Monthly Expense')
        imgg = BytesIO()
        plt.legend(['N\A'], loc='upper left', fontsize='small', bbox_to_anchor=(1, 1)  )
        plt.savefig(imgg, format='png')
        plt.close()
        imgg.seek(0)
        im = base64.b64encode(imgg.read()).decode('utf-8')
        return im

def pie_chart_yearly():
    count = 0
    categories = {}
    current = datetime.now()
    values = db.execute('SELECT * FROM transactions WHERE user_id = ?', session['user_id'])
    primary_category_db = db.execute('SELECT DISTINCT primary_category FROM categories')
    primary_category_db = [primary['primary_category'] for primary in primary_category_db]
    for prim in primary_category_db:
        if prim not in categories:
            categories[prim] = 0
    for value in values:
        date = datetime.strptime(value['date'], '%Y-%m-%d').date()
        if value['type'] == 'Expense':
            count +=1
            primary_category = value['primary_category']
            amount = (value['amount'])
            if date.year == current.year:
                categories[primary_category] = 0            
                categories[primary_category] += float(amount)
    
    if count != 0:    
        for keyy in list(categories.keys()):
            if categories[keyy] <= 0:
                del categories[keyy]
        pie_chart_name = list(categories.keys())
        pie_chart_values = list(categories.values())
        matplotlib.use('Agg')
        largest_val = pie_chart_values.index(max(pie_chart_values))
        explode = [0.09 if i == largest_val else 0 for i in range(len(pie_chart_values))]

        plt.figure(figsize=(10, 8))
        plt.pie(pie_chart_values, autopct = '%1.1f%%', shadow = True, labeldistance = 1.1, startangle = 90, radius=1.0,  textprops={'fontsize': 8}, explode=explode)
        plt.title('Pie chart of Yearly Expense')
        imgg = BytesIO()
        plt.legend(pie_chart_name, loc='upper left', fontsize='small', bbox_to_anchor=(1, 1)  )
        plt.savefig(imgg, format='png')
        plt.close()
        imgg.seek(0)
        im = base64.b64encode(imgg.read()).decode('utf-8')
        return im
    else:
        plt.figure(figsize=(10, 8))
        val = [1]
        plt.pie(val, autopct = '%1.1f%%', shadow = True, startangle = 90, radius=1.0,  textprops={'fontsize': 8})
        plt.title('Pie chart of Monthly Expense')
        imgg = BytesIO()
        plt.legend(['N\A'], loc='upper left', fontsize='small', bbox_to_anchor=(1, 1)  )
        plt.savefig(imgg, format='png')
        plt.close()
        imgg.seek(0)
        im = base64.b64encode(imgg.read()).decode('utf-8')
        return im


def salary_plot():
    current_year = datetime.now().year
    value = db.execute('SELECT * FROM transactions WHERE user_id= ?', session['user_id'])
    monthly_sums =  {}
    for dates in value:
        date = datetime.strptime(dates['date'], '%Y-%m-%d').date()
        if date.year == current_year:
            month_name = (date.strftime('%b'))
            transaction_type = dates['type']
            amount = dates['amount']
            if month_name not in monthly_sums:
                monthly_sums[month_name] = {}

            if transaction_type not in monthly_sums[month_name]:
                monthly_sums[month_name][transaction_type] = 0
            monthly_sums[month_name][transaction_type] += float(amount)
    
    
    months = list(monthly_sums.keys())
    months_sorted = [month[:3] for month in calendar.month_name[1:]]
    months_sortedd = {}
    for i, key in enumerate(months_sorted):
        months_sortedd[key] = i
    months = sorted(months, key=months_sortedd.get)
    graph_value_income = [float(monthly_sums[month].get('Income', 0)) for month in months]
    graph_value_Expense = [float(monthly_sums[month].get('Expense', 0)) for month in months]

    matplotlib.use('Agg')

    plt.plot(months, graph_value_income, label='Income', marker='o')
    plt.plot(months, graph_value_Expense, label='Expense', marker='o')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Monthly Income vs Expense')
    img = BytesIO()
    plt.legend()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    im = base64.b64encode(img.read()).decode('utf-8')
    return im




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password :
            flash("Username and password cannot be empty")
            return redirect('/login')
        

        if len(username) < 6 or len(password) < 6:
            flash("Username or password too short")   
            return redirect('/login')
        
    
        ans = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(ans) != 1 or not check_password_hash(
            ans[0]['password_hash'], password
        ):
            flash("Invalid username or password")
            
            return redirect('/login')
        else:
            session.clear()
            session["user_id"] = ans[0]['id']
            flash("Login successful")
            return redirect('/')
    else:
        return render_template('login.html')
    



@app.route('/register', methods=['GET', 'POST'])
def register():
    email_format = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    name_format = re.compile("^[A-Za-z]+( [A-Za-z]+)*$")
    response = requests.get('https://restcountries.com/v3.1/all')
    countries = response.json()
    country = [{'code': country['cca2'], 'country': country['name']['common']}for country in countries]

    if request.method == 'POST':
        name = request.form.get("name")
        if not name or is_num(name) or not name_format.match(name):
            flash("Invalid Name")
            return redirect('/register')
        
        username = request.form.get("username")
        if len(username) < 3:
            flash("Invalid Username")
            return redirect('/register')
        
        user_check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(user_check) !=0:
            flash("User already exists!")
            return redirect('/register')
        
    
        email = request.form.get("email")
        if not email_format.match(email):
            flash("Invalid email")
            return redirect('/register')
        
        email_check = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(email_check) !=0:
            flash("Email already exists!")
            return redirect('/register')
        
    
        password = request.form.get("password")
        if len(password) < 6:
            flash("Password is too weak")
            return redirect('/register')

        phone = request.form.get("phone")
        if not phone:
            phone = "None"

        dob = request.form.get("dob")

        try:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        except:
            print("value error")
        dob = dob.date()   
        today = dt.datetime.now()     
        date_limit = today - dt.timedelta(days=365 * 100)
        today = today.date()
        date_limit = date_limit.date()

        if dob < date_limit or dob > today:
            flash("Invalid DOB")
            return redirect('/register')
        country_code = request.form.get("country")
        country_list = [countryy['code'] for countryy in country]
        if not country_code in country_list:
            flash("Don't try to trick meeeeeeeeeee!!!!!!!!!!!")
            return redirect('/register')
        
        ans = db.execute("INSERT INTO users(name, username, email, password_hash, date_of_birth, country, phone_number, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", name, username, email, generate_password_hash(password), dob, country_code, phone, today)

        if ans != None:
            flash("Account created successfully")
            return redirect('/login')
        else:
            flash("There was an error creating your account")
            return redirect('/register')
    else:
        return render_template('register.html', countries=country)
    


@app.route('/my_account', methods=['GET', 'POST'])
@login_required
def my_account():
    if request.method =='POST':
        return "WIP"
    else:
        data = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])

        return render_template("myaccount.html", data=data)


@app.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    if request.method == 'POST':
        old_pass = request.form.get('old_pass')
        new_pass = request.form.get('new_pass')
        confirm_pass = request.form.get('confirm_pass')

        if not new_pass or not confirm_pass:
            flash("Password fields cannot be empty")
            return redirect('/change_pass')
        
        passs = db.execute("SELECT password_hash FROM users WHERE id = ?", session['user_id'])[0]['password_hash']
        if not check_password_hash(passs, old_pass):
            flash("Old password is incorrect")
            return redirect('/change_pass')
        if len(new_pass) < 6:
            flash("New password length is too short")
            return redirect('/change_pass')         
        if new_pass != confirm_pass:
            flash("Passwords don't match")
            return redirect('/change_pass')
        
        ans = db.execute("UPDATE users SET password_hash = ? WHERE id = ?", generate_password_hash(new_pass), session['user_id'],)
        if ans == 1:
            flash("Password changed succesfully!")
            return redirect('/')
    else:
        return render_template("change_pass.html")
    


@app.route('/change_pfp', methods=['GET','POST'])
@login_required
def change_pfp():
    if request.method=='POST':

        img = request.files['profile_pic']
        if not img:
            flash('No image selected')
            return redirect('/my_account')
        image = None
        if valid_extension(img.filename):
            image = base64.b64encode(img.read()).decode('utf-8')
        ans = db.execute("UPDATE users SET profile_picture = ? WHERE id = ? ", image, session['user_id'])
        if ans == 1:
            flash("Profile Picture Changed Successfully")
            return redirect('my_account')
        else:
            flash("There was an error processing your request")
            return redirect('my_account')
        


    

@app.route('/remove_pfp', methods=['POST'])
@login_required
def remove_pfp():
    if request.method == 'POST':
        default_pfp = ''
        with open('assets/default.jpg', "rb") as img:
            default_pfp = base64.b64encode(img.read()).decode('utf-8')
     
        ans = db.execute("UPDATE users SET profile_picture = ? WHERE id = ?", default_pfp, session['user_id'])
        if ans == 1:
            flash("Successfully removed the profile")
            return redirect('/my_account')
        else:
               flash("There was an issue removing your profile")
               return redirect('/my_account')         
        


@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    transfer_methodd = ['Cash', 'Credit card', 'Bank Transfer']

    if request.method == 'POST':
        name = request.form.get('new-transaction-name')
        date = request.form.get('new-transaction-date')
        type = request.form.get('category-type')
        primary_category = request.form.get('primary-category')
        sub_category = request.form.get('sub-category')
        amount = request.form.get('new-transaction-amount')
        transfer_method = request.form.get('transfer-method')
        description = request.form.get('description')
        if not name or not date or not amount or not type or not primary_category or not transfer_method:
            flash("All fields are required")
            return redirect('/transactions')
        try:
            amount = float(amount)
        except:
            flash("Invalid amount")
            return redirect('/transactions')
        
        if amount < 0:
            flash("Amount cannot be negative")
            return redirect('/transactions')
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except:
            flash("Invalid date")
            return redirect('/transactions')
        date = date.date()

        if primary_category not in primary_categories[type]:
            flash("Invalid category")
            return redirect('/transactions')
        if sub_category not in primary_categories[type][primary_category]:
            flash("Invalid category")
            return redirect('/transactions')
        
        ans = db.execute("INSERT INTO transactions(user_id, name, date, amount, type, primary_category, sub_category, method, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session['user_id'], name, date, amount, type, primary_category, sub_category, transfer_method, description)
        if ans == None:
            flash("There was an error processing your request")
            return redirect('/transactions')
        else:
            flash("Transaction added successfully")
            data = db.execute("SELECT * FROM transactions WHERE user_id = ?", session['user_id'])
            return redirect(url_for('transactions', data=data))
    else:
        search_query = request.args.get('search', '')
        data = []
        if search_query:
            data = db.execute('SELECT * FROM transactions WHERE name LIKE ? and user_id = ?', search_query, session['user_id'])
            if len(data) == 0:
                flash('No data found')
            search_mode = True
        else:
            search_mode = False
            data = db.execute("SELECT * FROM transactions WHERE user_id = ?", session['user_id'])
        return render_template('transactions.html', transfer_method=transfer_methodd, data=data, search_mode=search_mode)


primary_categories = {}
@app.route('/categories', methods=['GET','POST'])
@login_required
def categories():
    categories = db.execute('SELECT primary_category, sub_category, type FROM categories')
    primary_categories.clear()
    for category in categories:
        if category['type'] not in primary_categories:
            primary_categories[category['type']] = {}
        if category['primary_category'] not in primary_categories[category['type']]:
                
            primary_categories[category['type']][category['primary_category']] = []
                
        primary_categories[category['type']][category['primary_category']].append(category['sub_category'])

    return jsonify(primary_categories)




@app.route('/delete_transactions', methods=['POST'])
@login_required
def delete_transaction():
    if request.method == 'POST':
        id = request.form.getlist('checkbox-delete')
        if not id:
            flash("No transaction selected")
            return redirect('/transactions')
        for i in id:
            ans = db.execute("DELETE FROM transactions WHERE id = ?", i)
        if ans == None:
            flash("There was an error processing your request")
            return redirect('/transactions')
        return redirect('/transactions')
    


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    if request.method == 'POST':
        data = request.get_json()
        
        name = data.get('name')
        date = data.get('date')
        amount = data.get('amount')
        method = data.get('type')
        description = data.get('description')
        amount = float(amount)
        ans = db.execute('UPDATE transactions SET name = ?, date = ?, method = ?, amount = ?, description = ? WHERE id = ?', name, date, method, amount, description, transaction_id)
        if ans == 1:
            flash('Transaction edited')
            return jsonify({"message":"Transaction edited successfully"}), 200
            
    else:
        transaction = db.execute("SELECT * FROM transactions WHERE id = ?", transaction_id)[0]
        if len(transaction) == 0:
            return jsonify({"error": "Transaction not found"}), 404
        
        return jsonify(transaction)
    



@app.route('/search', methods=['GET'])
@login_required
def search():
    text = request.args.get('search')
    if not text:
        flash('Search cannot be empty')
    text = f"%{text}%"

    return redirect(url_for('transactions', search=text))



@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        id = session['user_id']
        confirmation_pass = request.form.get('confirmation-password')
        user = db.execute('SELECT password_hash FROM users WHERE id = ?', id)[0]['password_hash']
        if check_password_hash(user, confirmation_pass):
            anss = db.execute('DELETE FROM transactions WHERE user_id = ?', id)
            ans = db.execute('DELETE FROM users WHERE id = ?', id)

            if ans > 0 and anss > 0:
                session.clear()
                flash('Account successfully deleted, we are sad to see you go :(')
                return redirect(url_for('login'))
            else:
                flash('There was an error deleting your account')
                return redirect(url_for('/'))

        else:
            return "Invalid password"    
    else:
        return render_template('delete-account.html')
    


@app.route('/update_name', methods=['POST'])
@login_required
def name_change():
    name = request.form.get('name')
    if len(name) <3:
        flash('Too small input')
        return redirect(url_for('my_account'))
    if is_num(name):
        flash('Names can\'t have numbers')
        return redirect(url_for('my_account'))
    ans = db.execute('UPDATE users SET name = ? WHERE id = ?', name, session['user_id'])
    if ans == 1:
        flash('Name successfully updated')
        return redirect(url_for('my_account'))