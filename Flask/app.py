from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from verify_email import verify_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscribers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unsubscribe')
def unsubscribe():
    return render_template('unsubscribe.html')

@app.route('/subscribe', methods=['POST'])
def add_subscriber():
    email = request.form.get('email')
    if not email:
        return "No email provided, please enter an email.", 400
    
    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    if existing_subscriber is not None:
        return "Email already subscribed. Please use another email.", 409
    
    verification_result = verify_email(email)
    if verification_result and verification_result['data']['status'] == 'valid':
        try:
            new_subscriber = Subscriber(email=email)
            db.session.add(new_subscriber)
            db.session.commit()
            return "Subscription successful!", 200
        except Exception as e:
            print(str(e))
        return "Error processing your subscription.", 500
    else:
        return "Please provide a valid email address.", 400
@app.route('/unsubscribeAction', methods=['POST'])
def unsubscribeAction():
    email = request.form.get('email')
    if not email:
        return "No email provided, please enter an email.", 400

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        try:
            db.session.delete(subscriber)
            db.session.commit()
            return "You have been successfully unsubscribed.", 200
        except Exception as e:
            print(str(e))
            return "Error processing your unsubscribe request.", 500
    else:
        return "Email not found in our database.", 404
    
if __name__ == "__main__":
    app.run(debug=True)
