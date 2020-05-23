import requests
import json
from payeezy import api


def lambda_handler(event, context):

    method = event.get("httpMethod")

    if method == 'POST':
        event_body = event.get("body")
        json_data = json.loads(event_body)
        result = card_transaction(json_data)
    else:

        data = {"message": "Method Not Allowed"}
        result = {'statusCode': 405, 'body': json.dumps(data)}

    # Add Header to every Response
    response_headers = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
        }
    }

    result.update(response_headers)

    return result


def card_transaction(data):
    try:

        API_KEY = 'ENTER_YOUR_API_KEY_HERE'
        API_SECRET = 'ENTER_YOUR_API_SECRET'
        TOKEN = 'ENTER_YOUR_TOKEN'
        URL = 'https://api-cert.payeezy.com/v1/transactions'

        payeezy = api.API(API_KEY, API_SECRET, TOKEN, URL)

        card_info = data["card_info"]
        transaction = payeezy.process_purchase(transaction_total=card_info["transaction_total"],
                                               card_type=card_info["card_type"],
                                               card_number= card_info["card_number"],
                                               card_expiry=card_info["card_expiry"],
                                               card_cvv=card_info["card_cvv"],
                                               cardholder_name=card_info["cardholder_name"],
                                               merchant_reference=card_info["merchant_reference"])

        transaction_response = transaction.transaction_response.json()

        if transaction_response['transaction_status'] == 'approved':
            for key in transaction_response:
                print('%s : %s' % (key, transaction_response[key]))

            result = {'status': True, "message": "Payzee Credit Card Payment Success",
                      "result": transaction_response}

        else:
            print(transaction_response['Error'])
            result = {'status': False, "message": "Payzee Credit Card Payment Failure",
                      "result": transaction_response}

        return {'statusCode': 200, 'body': json.dumps(result)}


    except Exception as e:
        result = {'status': False, "message": "Payzee Credit Card Payment Transaction Failure", "error": e}
        return {'statusCode': 401, 'body': json.dumps(result)}
