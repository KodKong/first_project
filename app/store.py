import requests 
from config import URL_AUTHORIZATION, APP_CLIENT_SECRET, APP_CLIENT_ID, SECRET_KEY, URL_POINT_LIST, URL_PRICE_LIST, URL_PRODUCT_LIST
import datetime

def get_token(): 
    response = requests.post(URL_AUTHORIZATION, json = {
                                                    "app_client_id": APP_CLIENT_ID,
                                                    "app_secret": APP_CLIENT_SECRET,
                                                    "secret_key": SECRET_KEY })
    if response.status_code == 200:
        json_response = response.json()
        token = json_response['access_token']
    else:
        token = f'Ошибка при получении токена:, {response.text}'
    return token

def get_point_list(token: str): 
    request_header = {'X-SBISAccessToken': token}
    response = requests.get(URL_POINT_LIST, headers = request_header)
    if response.status_code == 200:
        point_list = response.json()
    else:
        point_list = f'Ошибка при получении точек:, {response.text}'
    return point_list

def get_points_price_list(token: str, point_id: str): 
    request_header = {'X-SBISAccessToken': token}
    current_date = datetime.date.today().isoformat()
    response = requests.get(URL_PRICE_LIST, headers = request_header, json = {
                                                                        "pointId": point_id,
                                                                        "actualDate": str(current_date)})
    if response.status_code == 200:
        price_list = response.json()
    else:
        price_list = f'Ошибка при получении прайс-листов по точке:, {response.text}'
    print(str(response.text))
    return price_list

def get_products(token: str, point_id: str, label: str): 
    request_header = {'X-SBISAccessToken': token}
    response = requests.get(URL_PRODUCT_LIST, headers = request_header, json = {"pointId": token,
                                                                                "priceListId": point_id,
                                                                                "searchString": label,
                                                                                "withBalance": "True", 
                                                                                "pageSize": "1100"})
    if response.status_code == 200:
        product_list = response.json()
    else:
        product_list = f'Ошибка при получении прайс-листов по точке:, {response.text}'
    print(str(response.text))
    return product_list