from stream.stream_settings import BASE_URL
from stream.exceptions import AuthorizationError, ServerError
import requests


def handle_status_code(status_code: int, msg_404: str = None):
    if status_code == 401:
        raise AuthorizationError("Failed to authorize your request.")
    elif status_code == 404:
        raise TypeError(msg_404 if msg_404 != None else "The Response returned 404.")
    elif status_code == 500:
        raise ServerError("An error has occurred in the Bunny servers while handling your request.")


def send_bunny_request(endpoint: str, method: str, access_key: str, error_message_404: str = None, json: dict = None, data: object = None, params: dict = None, content_type: str = None) -> dict:
    """
    This function will send a request to the Bunny servers.
    
    <endpoint> - The relative URL of the endpoint.
    <method> - The request method. Send this in all caps. Like "POST", "PUT", "DELETE", etc.
    <access_key> - The API key or the Authorization key that will be used in the request headers.
    <error_message_404> - The error message to display for response status code 404.
    <json> - Request data in JSON form.
    <data> - Request data in the form of any object you want to send.
    <params> - Query params to be sent with the request.
    """
    headers = {
        "AccessKey": access_key,
    }
    if content_type:
        headers.update({"Content-Type": content_type})

    if method == "GET":
        resp = requests.get(url=BASE_URL + endpoint, headers=headers, json=json, data=data, params=params)
    elif method == "POST":
        resp = requests.post(url=BASE_URL + endpoint, headers=headers, json=json, data=data, params=params)
    elif method == "PUT":
        resp = requests.put(url=BASE_URL + endpoint, headers=headers, json=json, data=data)
    elif method == "DELETE":
        resp = requests.delete(url=BASE_URL + endpoint, headers=headers)
    else:
        raise TypeError("Invalid method specified.")
    
    handle_status_code(status_code=resp.status_code, msg_404=error_message_404)
    return resp.json()