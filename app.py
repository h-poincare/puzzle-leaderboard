from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os 

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Store the database in a persistent directory

db_path = os.path.join("/opt/render", "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    f_name = db.Column(db.String, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Opt-In: {self.id}" 


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_phone = request.form.get('phone_num', type=int)
        user_name = request.form.get('f_name', type=str)
        new_user = User(phone_num=user_phone, f_name=user_name) 
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = User.query.order_by(User.date_created).all()
        return render_template('index.html', tasks=tasks)

def create_database():  
    with app.app_context():  
        db.create_all()  

# with app.app_context():
#     db.create_all()

# @app.before_first_request
# def create_db():
#     try:
#         db.create_all()  # Create tables if they don't exist
#         app.logger.info("Database and tables created successfully!")
#     except Exception as e:
#         app.logger.error(f"Error creating database: {str(e)}")


if __name__ == '__main__':
    create_database()
    app.run(debug=True)