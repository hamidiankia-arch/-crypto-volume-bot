import requests
import json
from datetime import datetime, timedelta

class CryptoAnalyzer:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        
    def get_top_cryptos(self, limit=20):
        """دریافت لیست 20 ارز برتر بر اساس مارکت کپ"""
        url = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching top cryptos: {e}")
            return []
    
    def get_coin_volume_data(self, coin_id):
        """دریافت داده‌های حجم معاملات برای یک ارز خاص"""
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': 4,  # 4 روز برای محاسبه 3 روز گذشته + امروز
            'interval': 'daily'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('total_volumes', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching volume data for {coin_id}: {e}")
            return []
    
    def analyze_volume_condition(self):
        """آنالیز ارزها بر اساس شرط حجم"""
        top_cryptos = self.get_top_cryptos(20)
        qualified_coins = []
        
        for crypto in top_cryptos:
            coin_id = crypto['id']
            symbol = crypto['symbol'].upper()
            name = crypto['name']
            current_price = crypto['current_price']
            market_cap = crypto['market_cap']
            
            volume_data = self.get_coin_volume_data(coin_id)
            
            if len(volume_data) >= 4:  # اطمینان از وجود داده‌های کافی
                # استخراج حجم‌های 4 روز اخیر
                volumes = [item[1] for item in volume_data[-4:]]  # آخرین 4 روز
                
                today_volume = volumes[3]  # امروز
                last_3_days_volume = sum(volumes[0:3])  # مجموع 3 روز گذشته
                
                # بررسی شرط: حجم امروز > مجموع 3 روز گذشته
                if today_volume > last_3_days_volume:
                    volume_increase_ratio = (today_volume / last_3_days_volume) if last_3_days_volume > 0 else 0
                    
                    qualified_coins.append({
                        'name': name,
                        'symbol': symbol,
                        'current_price': current_price,
                        'market_cap': market_cap,
                        'today_volume': today_volume,
                        'last_3_days_volume': last_3_days_volume,
                        'volume_increase_ratio': volume_increase_ratio
                    })
            
            # تاخیر کوچک برای احترام به API
            import time
            time.sleep(0.5)
        
        # مرتب‌سازی بر اساس نسبت افزایش حجم
        qualified_coins.sort(key=lambda x: x['volume_increase_ratio'], reverse=True)
        return qualified_coins