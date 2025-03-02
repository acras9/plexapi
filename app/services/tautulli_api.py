import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
from core.config import settings

class TautulliAPI:
    def __init__(self):
        self.base_url_korea = settings.TAUTULLI_URL_KOREA
        self.api_key_korea = settings.TAUTULLI_KEY_KOREA
        self.base_url_german = settings.TAUTULLI_URL_GERMAN
        self.api_key_german = settings.TAUTULLI_KEY_GERMAN
        
    def _make_request(self, region, cmd, params=None):
        """API 요청 보내기"""
        try:
            if region == 'korea':
                default_params = {
                    'apikey': self.api_key_korea,
                    'cmd': cmd
                }
                if params:
                    default_params.update(params)
                response = requests.get(self.base_url_korea, params=default_params, verify=False)
                response.raise_for_status()
                return response.json()
            elif region == 'german':
                default_params = {
                    'apikey': self.api_key_german,
                    'cmd': cmd
                }
                if params:
                    default_params.update(params)
                response = requests.get(self.base_url_german, params=default_params, verify=False)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_monthly_usage(self, region="통합"):
        """월간 사용량 데이터 가져오기"""
        try:
            params = {
                'y_axis': 'duration'
            }
            
            result_korea = None
            result_german = None
            
            # Get data based on region
            if region in ["통합", "한국"]:
                result_korea = self._make_request('korea', 'get_plays_per_month', params)
            if region in ["통합", "독일"]:
                result_german = self._make_request('german', 'get_plays_per_month', params)
            
            result = []
            
            # Process Korean server data
            if region in ["통합", "한국"] and result_korea and isinstance(result_korea, dict):
                if result_korea.get('response', {}).get('data', {}).get('series'):
                    korean_data = result_korea['response']['data']
                    categories = korean_data['categories']
                    series_data = korean_data['series']
                    
                    for i, month in enumerate(categories):
                        entry = {
                            "month": month,
                            "tv_독일": 0,
                            "movies_독일": 0,
                            "music_독일": 0,
                            "tv_한국": round(series_data[0]['data'][i]/3600,1) if len(series_data) > 0 else 0,
                            "movies_한국": round(series_data[1]['data'][i]/3600,1) if len(series_data) > 1 else 0,
                            "music_한국": round(series_data[2]['data'][i]/3600,2) if len(series_data) > 2 else 0
                        }
                        result.append(entry)
           
            # Process German server data
            if region in ["통합", "독일"] and result_german and isinstance(result_german, dict):
                german_data = result_german['response']['data']
                series_data = german_data['series']
                
                if region == "독일":
                    categories = german_data['categories']
                    result = [{
                        "month": month,
                        "tv_독일": round(series_data[0]['data'][i]/3600,1) if len(series_data) > 0 else 0,
                        "movies_독일": round(series_data[1]['data'][i]/3600,1) if len(series_data) > 1 else 0,
                        "music_독일": round(series_data[2]['data'][i]/3600,1) if len(series_data) > 2 else 0,
                        "tv_한국": 0,
                        "movies_한국": 0,
                        "music_한국": 0
                    } for i, month in enumerate(categories)]
                else:
                    for i in range(len(result)):
                        result[i]['tv_독일'] = round(series_data[0]['data'][i]/3600,1) if len(series_data) > 0 else 0
                        result[i]['movies_독일'] = round(series_data[1]['data'][i]/3600,1) if len(series_data) > 1 else 0
                        result[i]['music_독일'] = round(series_data[2]['data'][i]/3600,1) if len(series_data) > 2 else 0
            
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_daily_usage(self):
        """일간 사용량 데이터 가져오기"""
        try:
            params = {
                'y_axis': 'duration',
                'time_range': 31
            }
            
            # Get data from both servers
            result_korea = self._make_request('korea', 'get_plays_by_date', params)
            result_german = self._make_request('german', 'get_plays_by_date', params)
            
            # Initialize result list
            result = []
            
            # Process Korean server data
            if not isinstance(result_korea, dict) or not isinstance(result_german, dict):
                raise ValueError("Invalid response format from servers")
            
            if result_korea.get('response', {}).get('data', {}).get('series'):
                korean_data = result_korea['response']['data']
                categories = korean_data['categories']
                series_data = korean_data['series']
                
                # Create base structure
                for i, date in enumerate(categories):
                    entry = {
                        "date": date,
                        "tv_독일": 0,
                        "movies_독일": 0,
                        "music_독일": 0,
                        "tv_한국": round(series_data[0]['data'][i]/3600,1) if len(series_data) > 0 else 0,
                        "movies_한국": round(series_data[1]['data'][i]/3600,1) if len(series_data) > 1 else 0,
                        "music_한국": round(series_data[2]['data'][i]/3600,2) if len(series_data) > 2 else 0
                    }
                    result.append(entry)
            
            # Update with German server data
            if result_german.get('response', {}).get('data', {}).get('series'):
                german_data = result_german['response']['data']
                series_data = german_data['series']
                
                # Update existing entries with German data
                for i in range(len(result)):
                    result[i]['tv_독일'] = round(series_data[0]['data'][i]/3600,1) if len(series_data) > 0 else 0
                    result[i]['movies_독일'] = round(series_data[1]['data'][i]/3600,1) if len(series_data) > 1 else 0
                    result[i]['music_독일'] = round(series_data[2]['data'][i]/3600,1) if len(series_data) > 2 else 0
            
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_stats(self, period, region="통합"):
        """사용자 통계 데이터 가져오기"""
        try:
            active_users = []
            
            # Get active users based on region
            if region in ["통합", "한국"]:
                users_korea = self._make_request('korea', 'get_users')
                if users_korea.get('response', {}).get('data'):
                    active_users.extend([
                        {
                            'user_id': user['user_id'],
                            'friendly_name': user['friendly_name'],
                            'username': user['username']
                        }
                        for user in users_korea['response']['data']
                        if user.get('is_active') == 1
                    ])
            
            if region in ["통합", "독일"]:
                users_german = self._make_request('german', 'get_users')
                if users_german.get('response', {}).get('data'):
                    german_users = [
                        {
                            'user_id': user['user_id'],
                            'friendly_name': user['friendly_name'],
                            'username': user['username']
                        }
                        for user in users_german['response']['data']
                        if user.get('is_active') == 1
                    ]
                    
                    # Remove duplicates only for consolidated view
                    if region == "통합":
                        existing_ids = {user['user_id'] for user in active_users}
                        active_users.extend([user for user in german_users if user['user_id'] not in existing_ids])
                    else:
                        active_users = german_users

            user_stats = []
            for user in active_users:
                user_id = user['user_id']
                params = {'user_id': user_id, 'query_days': period}
                
                korea_time = 0
                german_time = 0
                
                # Get stats based on region
                if region in ["통합", "한국"]:
                    korea_stats = self._make_request('korea', 'get_user_watch_time_stats', params)
                    korea_time = korea_stats.get('response', {}).get('data', [{}])[0].get('total_time', 0)
                
                if region in ["통합", "독일"]:
                    german_stats = self._make_request('german', 'get_user_watch_time_stats', params)
                    german_time = german_stats.get('response', {}).get('data', [{}])[0].get('total_time', 0)
                
                user_stat = {
                    'user_id': user_id,
                    'friendly_name': user['friendly_name'],
                    'username': user['username'],
                    'korea_time': round(korea_time/3600, 1),
                    'german_time': round(german_time/3600, 1),
                    'total_time': round((korea_time + german_time)/3600, 1)
                }
                user_stats.append(user_stat)
            
            user_stats.sort(key=lambda x: x['total_time'], reverse=True)
            return user_stats[:10]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

