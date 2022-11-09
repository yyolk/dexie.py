# dexie.py
Simple dexie client


## Installation

```
pip install dexie.py
```

## Overview

Refer to the main [dexie.space API docs](https://dexie.space/api) for information on the endpoints and their parameters.

Basically you need to

1. Instantiate the client
2. Call a method on the client, that's related to it's endpoint
3. Use data that's returned by dexie

## Quick Start

```pycon
>>> import dexie

# initialize the api client
# the base_url can be either for mainnet or testnet
# use https://api.dexie.space for mainnet
# use https://api-testnet.dexie.space for testnet
>>> dc = dexie.Dexie(base_url="https://api.dexie.space")

# query for an offer file that we have the bytes of,
# by first converting it to Dexie's id format
>>> dexie.offer_file_to_dexie_id(b"""offer1qqz83wcsltt6wcmqvpsxygqq6tmp20fkzcmnnwmf7mff2a7a0shrpjyfl0ytl6e7hwt0887qncnmeemqatsymvx33fkmgcsm4hvyv2ak6x9xmdrzlvl5q9gm53c97c97aaeu9w7kgm3k6uer5vnwg85fv4wp7cp7wakkphxwczhd6ddjtf24qewtxs8puwhkv7ak7uzfvtup8zu8rjhmv8kcd5rue94ny5znv0mf6c2gv4s46zax6a9wrzxyzvstm343y95gk9v4nud7m8qd8uxdtx7wnu49anrvd7njl9wlm07dk7rzcqp2n9f8kvrng4eueap854ka09z00rwmsheadhc7hlk9wvfhc86a0muj5n080u97h4u8p3zzspzehy47f5k8d2534sumk7mdacnwvqk9mxaxkuu73gyyulga0kmx0qawu0wwrzcv9ac6vwzxdhwhrkwvjyl79rwp8vj5n6jmnenj2fadg8h9mxfhvvpsxrrd5lvls8d9sxwwd0xuqpn0tr7x0nukdup2ln896m4n9meamuh0v38u53rve9t90wtrzptkm602sat9dksf97u58tncxmld56d3cntnxszxkmvq5n407zmk84eyc74lx7kt7u60j5ylhrr9s2737f8xa470cganltw2925l70ajhlahxx7ddk8sskssrtr6uh2fjfw07em7ah009sa2kuhdksd7rz6hxwwxv2n7nmmyeqhn3wzutchl44zkymjtgz9xml306zv02g4t3wqa8vy5fhtkhwjsc0jk46e433zlclnpt0memngfnkct78dgetl07qkpyalry6c4tl9uel2l8r4mnxk8n2jvctpenvnk6pl7cjk9eha3w0gj5uysdca2zdlfuk2wu0f889nt29ttrrwusvm6uc0r60e6608u309jdnccggxdgv0eu3y2ua6sthmuktxg86lj8802llck3268cckemuhwkwytgl22pu7arjgehdvd2un7m7w6npcfch08484wn496h05jhx5mdewh49rqkyvqp0kf04kq8hvfh8""")
'HR7aHbCXsJto7iS9uBkiiGJx6iGySxoNqUGQvrZfnj6B'
>>> dexie_offer_id = _
>>> dc.get_offer(dexie_offer_id)
{'success': True, 'offer': {'id': 'HR7aHbCXsJto7iS9uBkiiGJx6iGySxoNqUGQvrZfnj6B', 'status': 4, 'offer': 'offer1qqz83wcsltt6wcmqvpsxygqq6tmp20fkzcmnnwmf7mff2a7a0shrpjyfl0ytl6e7hwt0887qncnmeemqatsymvx33fkmgcsm4hvyv2ak6x9xmdrzlvl5q9gm53c97c97aaeu9w7kgm3k6uer5vnwg85fv4wp7cp7wakkphxwczhd6ddjtf24qewtxs8puwhkv7ak7uzfvtup8zu8rjhmv8kcd5rue94ny5znv0mf6c2gv4s46zax6a9wrzxyzvstm343y95gk9v4nud7m8qd8uxdtx7wnu49anrvd7njl9wlm07dk7rzcqp2n9f8kvrng4eueap854ka09z00rwmsheadhc7hlk9wvfhc86a0muj5n080u97h4u8p3zzspzehy47f5k8d2534sumk7mdacnwvqk9mxaxkuu73gyyulga0kmx0qawu0wwrzcv9ac6vwzxdhwhrkwvjyl79rwp8vj5n6jmnenj2fadg8h9mxfhvvpsxrrd5lvls8d9sxwwd0xuqpn0tr7x0nukdup2ln896m4n9meamuh0v38u53rve9t90wtrzptkm602sat9dksf97u58tncxmld56d3cntnxszxkmvq5n407zmk84eyc74lx7kt7u60j5ylhrr9s2737f8xa470cganltw2925l70ajhlahxx7ddk8sskssrtr6uh2fjfw07em7ah009sa2kuhdksd7rz6hxwwxv2n7nmmyeqhn3wzutchl44zkymjtgz9xml306zv02g4t3wqa8vy5fhtkhwjsc0jk46e433zlclnpt0memngfnkct78dgetl07qkpyalry6c4tl9uel2l8r4mnxk8n2jvctpenvnk6pl7cjk9eha3w0gj5uysdca2zdlfuk2wu0f889nt29ttrrwusvm6uc0r60e6608u309jdnccggxdgv0eu3y2ua6sthmuktxg86lj8802llck3268cckemuhwkwytgl22pu7arjgehdvd2un7m7w6npcfch08484wn496h05jhx5mdewh49rqkyvqp0kf04kq8hvfh8', 'offered_coins': ['0xac057183bb929bf7f1a585f38ecafab6f22c0339c02ba08b50ceae1ae5b95b11'], 'date_found': '2022-08-06T08:28:49.121Z', 'date_completed': '2022-08-07T13:55:19.000Z', 'date_pending': '2022-08-07T13:55:11.373Z', 'spent_block_index': 2366671, 'price': 99009.900990099, 'offered': [{'id': 'xch', 'code': 'XCH', 'name': 'Chia', 'amount': 1.01}], 'requested': [{'id': 'a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913', 'code': 'SBX', 'name': 'Spacebucks', 'amount': 100000}], 'fees': 0, 'mempool': None, 'related_offers': [], 'coins': [{'amount': 1.5, 'puzzle_hash': '0x0150a84dd60158297ef5b8096390fc20de1239239a29acd362675abc239b92b8', 'parent_coin_info': '0xba54d2f17b1a7c31d9dab5da0b800175ad662eb352c11849c5ebb6984941bdc7', 'name': '0xac057183bb929bf7f1a585f38ecafab6f22c0339c02ba08b50ceae1ae5b95b11', 'code': 'XCH'}]}}
```
Price API also included
```pycon
# get all pairs
>>> dc.get_pairs()
# get all tickers
>>> dc.get_tickers()
{...}
# calculate the current price from ticker data
>>> ticker = dc.get_tickers("XCH_USDS)["tickers"][0]
>>> base_vol, target_vol = ticker["base_volume"], ticker["target_volume"]
>>> from decimal import Decimal
>>> Decimal(target_vol) / Decimal(base_vol)
Decimal('30.43791071338040603262456230')
```



## TODO

- [ ] Streaming API
