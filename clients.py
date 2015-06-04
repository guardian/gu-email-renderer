
import configuration

from guardianapi.apiClient import ApiClient

api_key = configuration.read('CAPI_KEY')
base_url=configuration.read('CAPI_BASE_URL')

client = ApiClient(base_url, api_key, edition="uk")
clientUS = ApiClient(base_url, api_key, edition='us')
clientAUS = ApiClient(base_url, api_key, edition='au')