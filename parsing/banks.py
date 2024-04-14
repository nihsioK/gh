import requests
import json
from tqdm.auto import tqdm

banks = json.load(open('banks.json'))
sub2parent = json.load(open('sub2parent.json'))
ready_to_go = []

for bank in banks:
    for category in bank['category']:
        x = {
            'category': category['name'],
            'main_category': sub2parent[category['name']] if category else None,
            'bank': bank['bank'],
            'card': "Base",
            'cashback': category['cashback'],
            'nfc': category['nfc']
        }

        ready_to_go.append(x)

with open('upload_banks.json', 'w') as f:
    json.dump(ready_to_go, f, ensure_ascii=False, indent=4)

# delete
response = requests.delete('https://orca-app-mjl8a.ondigitalocean.app/bankcashbacks/')

for i in tqdm(range(0, len(ready_to_go), 100)):
    response = requests.post('https://orca-app-mjl8a.ondigitalocean.app/bankcashbacks/', json=ready_to_go[i:i+100])
    print(response.status_code)
    print(i)
    print()

