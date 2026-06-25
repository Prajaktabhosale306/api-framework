import allure
import json

def attach_request(method, url, headers=None, payload=None):
    allure.attach(json.dumps({
        "method": method,
        "url": url,
        "headers": headers,
        "payload": payload
    }, indent=4), name="Request", attachment_type=allure.attachment_type.JSON)


def attach_response(response):
    content_type = response.headers.get("Content-Type", "")

    if "application/json" in content_type:
        body = response.json()
    else:
        body = response.text

    response_data = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": body
    }
   