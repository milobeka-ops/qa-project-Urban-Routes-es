import json
import time


def retrieve_phone_code(driver):
    code = None
    for _ in range(10):
        time.sleep(1)
        logs = driver.get_log('performance')
        for log in logs:
            message = json.loads(log['message'])['message']
            if message['method'] == 'Network.responseReceived':
                url = message['params']['response']['url']
                if 'number?number' in url:
                    request_id = message['params']['requestId']
                    try:
                        body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        code = json.loads(body['body'])['code']
                    except Exception:
                        pass
        if code:
            break
    return code