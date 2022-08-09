import requests
def checkConnection():
    reference="https://deniz.eu-latest.cumulocity.com/" #URL needs to be changed to the tenant's URL regardless of the use of the start-up script
    try:
        requests.head(reference,timeout=10)
        return True
    except:
        return False
