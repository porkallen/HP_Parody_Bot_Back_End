from wit import Wit

access_token = "6WI5F3AWG37B7SMUPI53VIKY4WSF3C4U"
access_token_dudley = "P2KLAZVQTTCKRFADW4WZ4JTELKT2FX4O"
access_token_petunia = "32FYMNSQS4TBBZUZHWQ3MOL7DV5OEQWM"
access_token_hagrid = "IEXS7ZQNI66SMYBCDQBNONSYZFY4CV62"
access_token_ollivander = "2C4ZEX5J3BGPW56OVCSJ52BEO3ESKV76"

client = Wit(access_token=access_token)
client_dudley = Wit(access_token=access_token_dudley)
client_petunia = Wit(access_token=access_token_petunia)
client_hagrid = Wit(access_token=access_token_hagrid)
client_ollivander = Wit(access_token=access_token_ollivander)


def wit_response(message_text):
    resp = client.message(message_text)
    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass
    return(entity, value)


#I Feel like this can be condensed so I don't have different one for each character

def wit_dudley_response(message_text):
    resp = client_dudley.message(message_text)
    print(resp)

    response_wit_parsed = {}

    try:
        for x in resp['entities']:
            for y in resp['entities'][x]:
                if x in response_wit_parsed:
                    response_wit_parsed[x].append(y['value'])
                else:
                    response_wit_parsed[x] = [y['value']]
    except:
        print('Something definitely is broken...')
        pass
    return response_wit_parsed

def wit_petunia_response(message_text):
    resp = client_petunia.message(message_text)

    response_wit_parsed = {}

    try:
        for x in resp['entities']:
            for y in resp['entities'][x]:
                if x in response_wit_parsed:
                    response_wit_parsed[x].append(y['value'])
                else:
                    response_wit_parsed[x] = [y['value']]
    except:
        print('Something definitely is broken...')
        pass
    return response_wit_parsed

#print(wit_response("I want to be in Ravenclaw"))

def wit_hagrid_response(message_text):
    resp = client_hagrid.message(message_text)

    response_wit_parsed = {}

    try:
        for x in resp['entities']:
            for y in resp['entities'][x]:
                if x in response_wit_parsed:
                    response_wit_parsed[x].append(y['value'])
                else:
                    response_wit_parsed[x] = [y['value']]
    except:
        print('Something definitely is broken...')
        pass
    return response_wit_parsed

def wit_ollivander_response(message_text):
    resp = client_ollivander.message(message_text)

    response_wit_parsed = {}

    try:
        for x in resp['entities']:
            for y in resp['entities'][x]:
                if x in response_wit_parsed:
                    response_wit_parsed[x].append(y['value'])
                else:
                    response_wit_parsed[x] = [y['value']]
    except:
        print('Something definitely is broken...')
        pass
    return response_wit_parsed