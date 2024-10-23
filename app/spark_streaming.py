from kafka import KafkaProducer
import json
from datetime import datetime
from requests import get
import time

# URL API CoinDesk
URL = 'https://production.api.coindesk.com/v2/tb/price/ticker?assets='

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_and_send_data(symbols):
    final_url = URL + symbols
    result = get(final_url)
    json_data = result.json()

    individual_symbols = symbols.split(',')
    
    for s in individual_symbols:
        coin_data = json_data['data'][s]
        data = {
            "iso": coin_data['iso'],
            "name": coin_data['name'],
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_price": coin_data['ohlc']['c'],
            "open": coin_data['ohlc']['o'],
            "high": coin_data['ohlc']['h'],
            "low": coin_data['ohlc']['l'],
            "close": coin_data['ohlc']['c']
        }
        producer.send('crypto-prices', value=data)
        print(f"Sent data to Kafka: {data}")

# Gửi dữ liệu mỗi 10 giây
while True:
    fetch_and_send_data('BTC,ETH')
    time.sleep(10)
