import requests

def HealthCheck():
    url = "https://bdo.mos.gov.pl/api/api/WasteRegister/WasteTransferCard/v1/HealthCheck"
    response = requests.get(url)

    if response.status_code == 200:
        headers = response.headers
        request_duration = response.elapsed.total_seconds() * 1000
        request_duration = round(request_duration)
        headers['request_duration'] = str(request_duration)
        return headers
    else:
        response = (f"Błąd {response.status_code}: {response.text}")
        return response

HealthCheck()