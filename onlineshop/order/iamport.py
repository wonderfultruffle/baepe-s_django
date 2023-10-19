import requests
from django.conf import settings

def get_token():
    '''
    아임포트 서버와 통신하기 위한 토큰을 받아오는 함수. requests 모듈을 이용하여 통신함.
    '''

    access_data = {
        "imp_key": settings.IAMPORT_KEY,
        "imp_secret": settings.IAMPORT_SECRET
    }

    url = "https://api.iamport.kr/users/getToken"

    req = requests.post(url, data=access_data)
    access_res = req.json()

    if access_res["code"] == 0:
        return access_res["response"]["access_token"]
    else:
        return None


def payments_prepare(order_id, amount, *args, **kwargs):
    '''
    결제를 준비하는 함수
    -> 결제에 필요한 정보(=주문번호order_id, 결제 금액amount)를 준비하여 아임포트 서버로 전달한다.(request 사용)
    '''
    access_token = get_token()
    if access_token:
        access_data = {
            "merchant_uid": order_id,
            "amount": amount
        }

        url = "https://api.iamport.kr/payments/prepare"
        headers = {
            "Authorization": access_token
        }

        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()
        
        if res["code"] != 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")

def find_transaction(order_id, *args, **kwargs):
    '''
    결제 완료 후 실제 결제 이력을 확인하는 함수.
    -> 아임포트 서버에 주문번호로 결제 이력을 요청(requests.post) -> 해당 정보는 res에 들어감.
    '''
    access_token = get_token()
    if access_token:
        url = "https://api.import.kr/payments/find/"+order_id

        headers = {
            "Authorization": access_token
        }

        req = requests.post(url, headers=headers)
        res = req.json()

        if res["code"] == 0:
            context = {
                "imp_id": res["response"]["imp_uid"],
                "merchant_order_id": res["response"]["merchant_uid"],
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