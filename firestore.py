import keys
import requests as http
import firebase_admin
from firebase_admin import auth, firestore, credentials
import time

def authenticate():
    token = auth.create_custom_token(keys.user_id)
    body = {
        'returnSecureToken': True,
        'token': token
    }

    token = http.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={keys.firebase_api_key}', data=body)
    token = token.json()
    return token['idToken']

def uploadToFirestore(data):
    try:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        client = firestore.client()

        for i, row in data.iterrows():
            client.collection('stock_picks').add({
                'symbol': row['symbol'],
                'name': row['name'],
                'roa': row['roa'],
                'pe_ratio': row['pe_ratio'],
                'roa_ranking': row['roa_ranking'],
                'pe_ranking': row['pe_ranking'],
                'overall_ranking': row['overall_ranking'],
                'industry': row['industry'],
                'created_at': time.time()
            })
    except Exception as ex:
        print(ex)
