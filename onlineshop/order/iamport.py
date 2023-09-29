import requests

from django.conf import settings

def get_token():

    access_data = {
        "imp_key": settings.IAMPORT_KEY,
        "imp_secret": settings.IAMPORT_SECRET
    }

    url = "https://api.iamport.kr/users/getToken"

    req = requests.post(url, data=access_data)
    access_res = req.json

    if access_res["code"] == 0:
        return access_res["response"]["access_token"]
    else:
        return None


def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:
        access_data = {
            "merchant_id": order_id,
            "amount": amount
        }

        url = "https://api.import.kr/payments/prepare"
        headers = {
            "Anthorized": access_token
        }

        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()
        
        if res["code"] is not 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")

def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.import.kr/payments/find/"+order_id

        headers = {
            "Authorization": access_token
        }

        req = requests.post(url, headers=headers)
        res = req.json()

        if res["code"] is 0:
            context = {
                "imp_id": res["response"]["imp_uid"],
                "merchant_id": res["response"]["merchant_uid"],
                "amount": res["response"]["amount"],
                "status": res["response"]["status"],
                "type": res["response"]["pay_method"],
                "receipt_url": res["response"]["receipt_utl"]
            }
            return context
        else:
            return None
    else:
        raise ValueError("토큰 오류")