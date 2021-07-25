from flask import Flask, request, render_template, redirect, flash
import hashlib
import requests
import csv
import datetime


app = Flask(__name__)
app.secret_key = "topsecret"


@app.route("/")
def payment_form():
    return render_template('payment.html')


def write_to_database(payer_request):

    # this function writes the necessary info submitted by user
    # to the "database.csv" file

    with open('database.csv', newline='', mode='a') as database:

        currency = request.form['currency']
        amount = request.form['payment_amount']
        payment_time = datetime.datetime.now()
        description = request.form['item_description']
        shop_order_id = payer_request['shop_order_id']

        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([currency, amount, payment_time, description, shop_order_id])


@app.route('/payment_request', methods=['GET', 'POST'])
def pay():

    # this function redirects user to the necessary payment platform / method
    # depending on currency chosen by user

    if request.method == 'POST':
        payment_method = request.form['currency']

        # chosen currency - EUR, payment method - 'Pay' protocol

        if payment_method == 'eur':

            amount = request.form['payment_amount']
            currency = '978'
            shop_id = '5'
            shop_order_id = '112'
            description = request.form['item_description']

            keys_required = [amount, currency, shop_id, shop_order_id]
            secret = 'SecretKey01'
            sign = hashlib.sha256(f"{':'.join(keys_required)}{secret}".encode('utf-8')).hexdigest()

            payer_request = {
                'amount': amount,
                'currency': currency,
                'shop_id': shop_id,
                'shop_order_id': shop_order_id,
                'description': description,
                "sign": str(sign)
            }

            write_to_database(payer_request)

            return render_template('eur_payment.html', data=payer_request)

        # chosen currency - USD, payment method - Bill

        elif payment_method == 'usd':

            shop_amount = request.form['payment_amount']
            shop_currency = '840'
            shop_id = '5'
            shop_order_id = '112'
            payer_currency = '840'
            description = request.form['item_description']

            keys_required = [payer_currency, shop_amount, shop_currency, shop_id, shop_order_id]
            secret = 'SecretKey01'
            sign = hashlib.sha256(f"{':'.join(keys_required)}{secret}".encode('utf-8')).hexdigest()

            payer_request = {
                'shop_amount': shop_amount,
                'shop_currency': shop_currency,
                'shop_id': shop_id,
                'shop_order_id': shop_order_id,
                'payer_currency': payer_currency,
                'description': description,
                "sign": str(sign)
            }

            write_to_database(payer_request)

            url = 'https://core.piastrix.com/bill/create'
            response = requests.post(url, json=payer_request)
            if response.json()['result']:
                redirect_url = str(response.json()['data']['url'])
                return redirect(redirect_url)
            else:
                error_message = response.json()['message']
                message = f'Error: {error_message}. Please check your request and try again.'
                flash(message, 'error')
                return render_template('payment.html')

        # chosen currency - RUB, payment method - invoice, platform - Advcash

        elif payment_method == 'rub':

            amount = request.form['payment_amount']
            currency = '643'
            payway = "advcash_rub"
            shop_id = '5'
            shop_order_id = '112'

            keys_required = [amount, currency, payway, shop_id, shop_order_id]
            secret = 'SecretKey01'
            sign = hashlib.sha256(f"{':'.join(keys_required)}{secret}".encode('utf-8')).hexdigest()

            payer_request = {
                'amount': amount,
                'currency': currency,
                'shop_id': shop_id,
                'shop_order_id': shop_order_id,
                'payway': payway,
                "sign": str(sign)
            }

            write_to_database(payer_request)

            url = 'https://core.piastrix.com/invoice/create'
            response = requests.post(url, json=payer_request)

            if response.json()['result']:
                return render_template('rub_payment.html', data=response.json()['data'])
            else:
                error_message = response.json()['message']
                message = f'Error: {error_message}. Please check your request and try again.'
                flash(message, 'error')
                return render_template('payment.html')


if __name__ == "__main__":
    app.run(debug=True)
