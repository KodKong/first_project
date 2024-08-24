import requests 
from config import URL_AUTHORIZATION, APP_CLIENT_SECRET, APP_CLIENT_ID, SECRET_KEY, URL_POINT_LIST, URL_PRICE_LIST, URL_PRODUCT_LIST
import datetime

def get_token(): 
    try: 
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
    except:
        return 'error'

async def get_point_list(): 
    try: 
        token = str(get_token())
        request_header = {'X-SBISAccessToken': token}
        response = requests.get(URL_POINT_LIST, headers = request_header)
        if response.status_code == 200:
            point_list = response.json()
        else:
            point_list = f'Ошибка при получении точек:, {response.text}'
        return point_list
    except:
        return 'error'

async def get_points_price_list(point_id: str): 
    try: 
        token = str(get_token())
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
    except:
        return 'error'

async def get_products(point_sbys_id: str, price_list_id: str, label: str): 
    try: 
        token = str(get_token())
        request_header = {'X-SBISAccessToken': token}
        response = requests.get(URL_PRODUCT_LIST, headers = request_header, json = {"pointId": point_sbys_id,
                                                                                    "priceListId": price_list_id,
                                                                                    "searchString": label,
                                                                                    "withBalance": "True", 
                                                                                    "pageSize": "1100"})
        if response.status_code == 200:
            product_list = response.json()
        else:
            product_list = f'Ошибка при получении прайс-листов по точке:, {response.text}'
        return product_list
    except:
        return 'error'

async def show_products(point_sbys_id: str, price_list_id: str, label: str): 
    try:
        json_list_products = await get_products(point_sbys_id, price_list_id, label)
        array_products = []
        string_product = ''
        iteraction = 1
        for item in json_list_products['nomenclatures']:
            if item['balance'] is not None: 
                product = str(iteraction) + '. ' + item['name'] + '\n'
                if len(string_product) + len(product) > 4098: 
                    array_products.append(string_product)
                    string_product = product
                else: 
                    string_product += product
                iteraction += 1
        if string_product:
                array_products.append(string_product)
        return array_products
    except:
        return 'error'