import requests
def checkConnection():
    reference="https://deniz.eu-latest.cumulocity.com/"
    try:
        requests.head(reference,timeout=10)
        return True
    except:
        return False
