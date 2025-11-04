import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

class CurrencyData:
    def __init__(self):
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.currencies = {}
        self.last_update = None
        
    def get_curr_rates(self):
        """Получение актуальных курсов валют с сайта ЦБ РФ"""
        try:
            response = requests.get(self.url)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                raise Exception(f"Ошибка подключения: {response.status_code}")
            
            root = ET.fromstring(response.content)
            self.last_update = root.attrib['Date']
            
            currencies_data = {}
            for valute in root.findall('Valute'):
                try:
                    char_code = valute.find('CharCode').text
                    name = valute.find('Name').text

                    value_text = (valute.find('Value')).text if (valute.find('Value')).text is not None else "0"
                    value = float(value_text.replace(',', '.'))
                    
                    nominal = int((valute.find('Nominal')).text) if (valute.find('Nominal')).text is not None else 1
                    

                    currencies_data[char_code] = {
                        'name': name,
                        'rate': value / nominal,
                        'nominal': nominal
                    }
                except Exception as e: 
                    print(f"Ошибка при обработке валюты {char_code}: {e}")
                    continue

            currencies_data['RUB'] = {
                'name': 'Российский рубль',
                'rate': 1.0,
                'nominal': 1
            }
            
            self.currencies = currencies_data
            return currencies_data
            
        except Exception as e: 
            raise Exception(f"Ошибка при получении данных: {str(e)}")
    
    def convert_curr(self, amount, from_curr, to_curr):
        """Конвертация валюты"""
        if from_curr not in self.currencies or to_curr not in self.currencies:
            raise Exception("Неверный код валюты")
        
        amount_in_rub = amount * self.currencies[from_curr]['rate']
        converted_amount = amount_in_rub / self.currencies[to_curr]['rate']
        
        return round(converted_amount, 3)
