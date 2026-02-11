"""
    Price Catcher
    by: Keith Lim

Based on The Price is Right game

Game mode:
1 = The Price is Right (Guess the price as close as possible without going over)
2 = Delta (Get as close as possible over or under)

functions:
load_data()
calculate_delta()
price_is_right()
get_image_url()

Variables to use:
ori_premise         premise_state           item_name
ori_code            premise_district        item_unit
ori_price

Dataframes:
df_main
df_lookup
df_premise
ORDER: df_main > df_lookup > df_premise

Image URL Pattern
https://img.manamurah.com/barang_nobg/{ori_code}.png

Reference:
https://open.dosm.gov.my/data-catalogue/pricecatcher
"""


import gc
import pandas as pd
import fastparquet  # Dummy import for pipreqs

DATA_URL = 'https://storage.data.gov.my/pricecatcher/pricecatcher_2026-01.parquet'
LOOKUP_PREMISE_URL = 'https://storage.data.gov.my/pricecatcher/lookup_premise.parquet'
LOOKUP_ITEM_URL = 'https://storage.data.gov.my/pricecatcher/lookup_item.parquet'

item_info = {}

def load_data():
    """
    Load all necessary data upon startup
    Returns three dataframe
    (df_main, df_lookup, df_premise)
    """
    global df_main, df_lookup, df_premise

    try:
        # Lookup Premise (state & district), loads df_premise and drops first row
        df_premise = pd.read_parquet(LOOKUP_PREMISE_URL, columns=['premise_code', 'state', 'district'])
        df_premise = df_premise.iloc[1:]

        df_premise = df_premise.astype({
            'premise_code': 'float32',
            'state': 'str',
            'district': 'str'
        })

        # Lookup Item (item name, code & unit), loads df_lookup and drops first row
        df_lookup = pd.read_parquet(LOOKUP_ITEM_URL, columns=['item_code', 'item', 'unit'])
        df_lookup = df_lookup.iloc[1:]
        # Get the unique list of valid item codes, in array form
        item_codes = df_lookup['item_code'].unique()

        df_lookup = df_lookup.astype({
            'item_code': 'int16',
            'item': 'str',
            'unit': 'str'
        })

        # Load df_main
        df = pd.read_parquet(DATA_URL)
        df = df.astype({
            'premise_code': 'int16',
            'item_code': 'int16',
            'price': 'float16'
        })
        df = df[df['item_code'].isin(item_codes)].copy()

        # df_main = df_main.sample(n=1000).copy()
        df_main = df.sample(n=1000)
        del df
        gc.collect()

        return df_main, df_lookup, df_premise
    
    except Exception as e:
        print(f"Error loading data: {e}")

def calculate_delta(ori_price, guess_price):
    """
    Calculates the delta of the guessed price with the original price
    Returns a positive value of the difference (Delta) in type float, rounded up to 2 decimal points
    """
    diff = ori_price - guess_price
    delta = abs(diff)

    return round(delta, 3)

def price_is_right(game_mode, guessed, actual):
    """
    Prints out statements depending on game mode
    """
    if game_mode == 1:  # The price is right, is default option
        if guessed == actual:
            print("EXACT GUESS!!")
        elif guessed <= actual:
            print("You win!")
        else:
            print("You lose :(")
    elif guessed <= actual:
        print("Close enough...")
    else:
        print("Bit over...")

def get_image_url(item_code):
    """
    Generate image URL from item code
    Returns url in string format
    """
    return f"https://img.manamurah.com/barang_nobg/{item_code}.png"

def grab_info(df_main, df_lookup, df_premise):
    """
    Picks a random row & gets all the neccessary info from dataframes
    Prints info in terminal
    Returns in dictionary
    """
    # Choose a random row from df_main
    random_row = df_main.sample(n=1) # Choose a random row
    ori_code = random_row["item_code"].values[0]            # What type of item it is, type = int
    ori_premise = random_row["premise_code"].values[0]      # Where the item is from, type = string
    ori_price = random_row["price"].values[0]
    image_url = get_image_url(ori_code)

    # Get the item name and unit
    matching_rows = df_lookup.loc[df_lookup['item_code'] == ori_code]
    item_name = matching_rows["item"].values[0]
    item_unit = matching_rows["unit"].values[0]

    matching_premise = df_premise.loc[df_premise['premise_code'] == float(ori_premise)]
    premise_state = matching_premise['state'].values[0]
    premise_district = matching_premise['district'].values[0]

    print(f"""\nFrom {premise_district}, {premise_state}:
    Item: {item_name}
    Unit: {item_unit}
    IMG: {image_url}
    oriprice = {ori_price:.2f}
    """)

    return {
        "district": premise_district,
        "state": premise_state,
        "item_name": item_name,
        "unit": item_unit,
        "image_url": image_url,
        "price": round(ori_price,2)
    }


# if __name__ == '__main__':
#     tracemalloc.start()
#     best_guess = 1000.0
#     df_main, df_lookup, df_premise = load_data()

#     while True:
#         item_info = grab_info(df_main, df_lookup, df_premise)
#         ori_price = item_info['price']

#         guess_price = float(input("Guess the price: RM "))
#         difference = calculate_delta(ori_price, guess_price)
#         print("=====================================")
#         price_is_right(game_mode=1, guessed=guess_price, actual=ori_price)  # Set to always Price is right mode
#         print(f"You guessed   : RM {guess_price: .2f}")
#         print(f"Correct price : RM {ori_price}")
#         print(f"Difference    : RM {difference: .2f}")
        
#         # Update best guess
#         # if best_guess == None:
#         #     best_guess = difference
#         # elif difference < best_guess:
#         #     best_guess = difference
#         #     print(f"New Best! : RM {best_guess: .2f}")
#         if difference < best_guess:
#             best_guess = difference
#             print(f"New Best! : RM {best_guess: .2f}")
#         else:
#             print(f"Best Guess  : RM {best_guess: .2f}")

#     # Game loop repeat, add while True:
#         player = input("Do you want to play another round? (y/n): ")
#         if player.lower() == 'n':
#             print("Thanks for playing")
#             break


#         # df_main.info(memory_usage="deep")
#         process = psutil.Process(os.getpid())
#         print(f"RAM used: {process.memory_info().rss / 1024**2:.2f} MB")
#         current, peak = tracemalloc.get_traced_memory()
#         print(f"Current: {current / 1024**2:.2f} MB; Peak: {peak / 1024**2:.2f} MB")
#     tracemalloc.stop()
