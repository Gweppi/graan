from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from dotenv import load_dotenv
import os

load_dotenv()

password = os.environ.get('PASSWORD')

api = SentinelAPI('jeppi', password)

product = os.environ.get('PRODUCT')

data = api.get_product_odata(product)

api.download(product, nodefilter="*B02")