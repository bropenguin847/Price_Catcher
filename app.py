"""
Docstring for Price_Catcher.app

Initally, the webpage is at index, then when user press submit, it will go to the game

TODO:
Improve the look of the websites
"""


from flask import Flask, render_template, request, jsonify
from game import load_data, grab_info, get_image_url, calculate_delta

DATA_URL = 'https://storage.data.gov.my/pricecatcher/pricecatcher_2026-02.parquet'
LOOKUP_PREMISE_URL = 'https://storage.data.gov.my/pricecatcher/lookup_premise.parquet'
LOOKUP_ITEM_URL = 'https://storage.data.gov.my/pricecatcher/lookup_item.parquet'

app = Flask(__name__)

# Dataframe to be used
df = None
df_main = None
df_lookup = None
df_premise = None

df_main, df_lookup, df_premise = load_data()
random_row = df_main.sample(n=1)    # Chooses a random row
ori_premise = random_row["premise_code"].values[0]
ori_code = random_row["item_code"].values[0] 

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        image_url = get_image_url(ori_code)
        )

@app.route('/pricecatcher', methods=["POST","GET"])
def pricecatcher():
    result = None
    ori_price = 0
    df_main, df_lookup, df_premise = load_data()
    item_info = grab_info(df_main, df_lookup, df_premise)

    ori_price = item_info['price']

    if request.method == 'POST':
        user_guess = request.form.get('user_guess')
        if user_guess:
            guess_price = float(user_guess)

            result = calculate_delta(ori_price, guess_price)
            return jsonify(
                ori_price=ori_price,
                result=result)

    return render_template(
        'pricecatcher.html',
        district = item_info['district'],
        state = item_info['state'],
        item_name = item_info['item_name'],
        item_unit = item_info['unit'],
        image_url = item_info['image_url'],
        price = item_info['price'],
        ori_price=ori_price,
        result = result
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
