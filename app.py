"""
Main web app

Initally, the webpage is at index, then when user press submit, it will go to the game

"""


import os
from flask import Flask, render_template, jsonify, session, request
from game import load_data, grab_info, get_image_url, calculate_delta

DATA_URL = 'https://storage.data.gov.my/pricecatcher/pricecatcher_2026-02.parquet'
LOOKUP_PREMISE_URL = 'https://storage.data.gov.my/pricecatcher/lookup_premise.parquet'
LOOKUP_ITEM_URL = 'https://storage.data.gov.my/pricecatcher/lookup_item.parquet'

app = Flask(__name__)
app.secret_key = 'my_super_duper_secret_key'

df_main, df_lookup, df_premise = load_data()        # Loads data in the beginning

@app.route('/')
@app.route('/index')
def index():
    # Chooses a random item to display on idex page
    random_row = df_main.sample(n=1)
    ori_code = random_row["item_code"].values[0]

    return render_template(
        'index.html',
        image_url = get_image_url(ori_code)
        )

@app.route("/pricecatcherTPIR")
def pricecatcher():
    global result, best_guess, ori_price, item_info
    item_info = grab_info(df_main, df_lookup, df_premise)

    return render_template(
        'pricecatcherTPIR.html',
        district = item_info['district'],
        state = item_info['state'],
        item_name = item_info['item_name'],
        item_unit = item_info['unit'],
        image_url = item_info['image_url'],
        ori_price = item_info['price'],
        # result = result,
        # best_guess = session['best_guess']
    )

@app.route("/pricecatcherDelta")
def delta():
    global result, best_guess, ori_price, item_info
    item_info = grab_info(df_main, df_lookup, df_premise)

    return render_template(
        'pricecatcherDelta.html',
        district = item_info['district'],
        state = item_info['state'],
        item_name = item_info['item_name'],
        item_unit = item_info['unit'],
        image_url = item_info['image_url'],
        ori_price = item_info['price'],
    )

# Route user to guess price
@app.route('/userguess', methods=["POST","GET"])
def userguess():
    global item_info
    ori_price = float(item_info['price'])
    if 'best_guess' not in session:
        session['best_guess'] = 1000.00

    data = request.get_json()
    user_guess = float(data.get("user_guess", 0))
    result = float(calculate_delta(ori_price, user_guess))

    # "The Price is Right" Logic: Over is a loss
    if user_guess > ori_price:
        message = "Bust! You went over the price."
        status = "lose"

    else:
        message = f"Great guess! You are RM {result:.2f} away."
        status = "win"

        if result < float(session['best_guess']):
            session['best_guess'] = result

    # To avoid TypeError, change all values to Python default
    return jsonify({
        'ori_price': ori_price,
        'user_guess': user_guess,
        'result': result,
        'best_guess': float(session['best_guess']),
        'message': message,
        'status': status
        })
    # if request.method == 'POST':
    #     user_guess = request.form.get('user_guess')
    #     if user_guess:
    #         guess_price = float(user_guess)

    #         result = calculate_delta(ori_price, guess_price)
    #         if result < session['best_guess']:
    #             session['best_guess'] = result  # Saves to browser cookie
    #         return jsonify(
    #             ori_price=ori_price,
    #             result=result,
    #             best_guess=session['best_guess'])


if __name__ == "__main__":
    # gunicorn --bind 0.0.0.0:8000 app:app)
    
    # For deployment on Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
