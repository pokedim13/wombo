"""
	URLs for calling APIs.
"""

from typing import Dict

urls = {
    "js_filename": "https://dream.ai/create",
    "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp",
    "draw_url": "https://paint.api.wombo.ai/api/v2/tasks",
}

auth_key_headers = {
    "authority": "identitytoolkit.googleapis.com",
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://dream.ai",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-client-version": "Chrome/JsCore/9.1.2/FirebaseCore-web",
}

check_headers = {
    "authority": "paint.api.wombo.ai",
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "authorization": "bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImM4MjNkMWE0MTg5ZjI3NThjYWI4NDQ4ZmQ0MTIwN2ViZGZhMjVlMzkiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wYWludC1wcm9kIiwiYXVkIjoicGFpbnQtcHJvZCIsImF1dGhfdGltZSI6MTY4MTY2NjM1MCwidXNlcl9pZCI6ImhUTTlGdmcxUjdURXJvd29FYnFBMU1ucG95QTIiLCJzdWIiOiJoVE05RnZnMVI3VEVyb3dvRWJxQTFNbnBveUEyIiwiaWF0IjoxNjgxNjY2MzUwLCJleHAiOjE2ODE2Njk5NTAsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.cwcqHkKpVgq6B9CUnQmM4hA6uWmjW9jOdzC98MYZVvSgp02cn3lA9JUMNBqoZS3tKj2aLzIRRr0v-LRK4Hq-223vPI1USmDQ543BZZDlI4mGwR428hPOD8iIZxdR6d-kTEyvg82GtrJ7QIgTByrqkhAxwwdxMyLvEiUkAgggefjuTE0-dNxDxX9PI-_7bnJ5bc2sYFkwTiDQ_snyj34TE9C5stVtubtCqaCtKKEt3HO7nBhxRFjh7IeN18QWG8Qt1WLbKoqPFo3QJVuZDSk6tmb5YZpvwQjTsRuUjQSMTGytHMLBZ2eAubr7MQYctYklE8GDQ3G5dksgbVtCxsDI8g",
    "origin": "https://dream.ai",
    "referer": "https://dream.ai/",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.895 Yowser/2.5 Safari/537.36",
    "x-app-version": "WEB-2.0.0",
}


def headers_gen(auth_key: str) -> Dict:
    return {
        "authority": "paint.api.wombo.ai",
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9",
        "authorization": f"bearer {auth_key}",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://dream.ai",
        "referer": "https://dream.ai/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.895 Yowser/2.5 Safari/537.36",
        "x-app-version": "WEB-2.0.0",
    }
