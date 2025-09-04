#  A. HTTP
#  • Write a Python program to:
#  1. Send GET and POST requests to a test API or website.
#  2. Display the response status code, headers, and body.
#  3. Log errors if the request fails.

# http_client.py

import requests

try:
    # GET request
    response = requests.get("https://httpbin.org/get")
    print("GET Request:")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    # POST request
    payload = {"name": "Hari Kishan", "course": "Computer Networks"}
    response = requests.post("https://httpbin.org/post", data=payload)
    print("\nPOST Request:")
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

except requests.exceptions.RequestException as e:
    print("Error occurred:", e)
