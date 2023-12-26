from flask import Flask, render_template, abort, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Products & Services
@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Ride
@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/safety')
def safety():
    return render_template('safety.html')

@app.route('/sustainability')
def sustainability():
    return render_template('sustainability.html')

@app.route('/insurance')
def insurance():
    return render_template('insurance.html')

# Resources
@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/user-agreement')
def user_agreement():
    return render_template('user-agreement.html')

@app.route('/refund-policy')
def refund_policy():
    return render_template('refund-policy.html')

# Logs
@app.route('/messages/<int:idx>')
def message(idx):
    messages = [{'title': 'Message One',
                'content': 'Message One Content'},
                {'title': 'Message Two',
                'content': 'Message Two Content'}
                ]
    return render_template('message.html', messages=messages)

# Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/500')
def error500():
    abort(500)

if __name__ == '__main__':
    app.run()
