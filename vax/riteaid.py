import requests
import time
import smtplib
import datetime
import config


def rite_url(zip_code="94043", radius=25):
    return f'https://www.riteaid.com/services/ext/v2/stores/getStores?address={zip_code}' \
           f'&attrFilter=PREF-112&fetchMechanismVersion=2&radius={radius}'


def check_riteaid(zip_code="94043", radius=25):
    print("checking RiteAid...")
    lastStoreFound = ""

    fetchStoresRiteAidUrl = rite_url(zip_code, radius)
    fetchStoresResponse = requests.get(fetchStoresRiteAidUrl)

    nearbyStores = []

    data = fetchStoresResponse.json().get("Data").get("stores")

    for store in data:
        nearbyStores.append(store)

    storeWithApptAvailable = None

    if (len(nearbyStores) == 0):
        raise ValueError("no nearby RiteAid stores")

    for store in nearbyStores:
        apptUrl = 'https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber={}'.format(
            store.get('storeNumber'))
        apptsAvailableResponse = requests.get(apptUrl)

        print(apptsAvailableResponse.text)

        try:
            apptAvailable = apptsAvailableResponse.json().get('Data').get('slots').get('1')
        except AttributeError:
            continue
            apptAvailable = False
            # print(f"Error: {apptsAvailableResponse}")

        # print("{} : {}".format(store.get('storeNumber'), apptAvailable))

        if (apptAvailable != False):
            storeWithApptAvailable = store
            if lastStoreFound != storeWithApptAvailable.get('storeNumber'):
                break

        print("-------------")

    appointmentsAvailable = storeWithApptAvailable != None

    if appointmentsAvailable == False:
        print("RiteAid: none available")
        return False
    else:
        print("RiteAid: appointments available. Check on https://www.riteaid.com/covid-vaccine-apt")
        print(storeWithApptAvailable.get('storeNumber'))
        return fetchStoresResponse
        #
        # if (lastStoreFound == storeWithApptAvailable.get('storeNumber')):
        #     print("same store found")
        #
        #
        # lastStoreFound = storeWithApptAvailable.get('storeNumber')
        #
        # storeAddress = "{}, {}, {}, {}".format(storeWithApptAvailable.get('address'),
        #                                        storeWithApptAvailable.get('city'),
        #                                        storeWithApptAvailable.get('state'),
        #                                        storeWithApptAvailable.get('zipcode'))
        # print("Found store: {}".format(storeAddress))
