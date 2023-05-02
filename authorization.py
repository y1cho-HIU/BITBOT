from binance.client import Client
import params_private as prv

Auth = Client(api_key=prv.api_key, api_secret=prv.api_secret)
