from flask import Flask, render_template, request
from weather import main as get_weather

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    data=None
    if request.method == 'POST':
        # uses form controls to collect the input
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        # calls main grom weather.py using above input
        data = get_weather(city,state,country)
    # returns that information to the index.html to format it on the webpage. 
    return render_template('index.html', data=data)
if __name__ == '__main__':
    app.run(debug=True)