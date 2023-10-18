from whatsapp_api_client_python import API
from local.io import get_secrets

_secrets = get_secrets()
green_api = API.GreenAPI(_secrets["greenApiId"], _secrets["greenApiToken"])