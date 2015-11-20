# Roadrunnr
Python client for APIs of RoadRunnr (http://roadrunnr.in/)

### Installation

```
git+https://github.com/Sandeep4/roadrunnr.git#egg=roadrunnr
```

### Usage

```python
from roadrunnr import RoadRunnrClient

client = RoadRunnrClient(client_id, client_secret)

params  = {}
client.create_order(params)
client.get_order(order_id)
client.ship_order(order_id)
client.track_order(order_id)
client.complete_order(order_id)
client.cancel_order(order_id)
client.get_localities()
client.get_cities()

```