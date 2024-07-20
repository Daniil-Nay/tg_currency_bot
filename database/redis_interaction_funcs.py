from aiogram.client.session import aiohttp
import xml.etree.ElementTree as ET


async def update_currency(redis_client):
    """
    Функция, предназначенная для заполнения БД [валюта] [значение]
    :param redis_client:
    :return:
    """
    #не знаю, есть ли смысл прятать ссылку в env
    XML_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
    async with aiohttp.ClientSession() as session:
        async with session.get(XML_URL) as response:
            xml_data = await response.text()
            tree = ET.ElementTree(ET.fromstring(xml_data))
            root = tree.getroot()
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                value = float(valute.find('Value').text.replace(',', '.'))
                redis_client.set(char_code, value)
    print('успешно передали данные xml в редис')