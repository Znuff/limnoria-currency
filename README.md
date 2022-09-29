Currency conversion plugin for Limnoria/Supybot.

This uses the Free Plan API from https://apilayer.com/marketplace/currency_data-api.

You will need an API KEY.

Configure it with

````
config supybot.plugins.currency.apikey <api-key>
````

Example:

````
user: >currency convert 1 btc to usd
bot: 1.00 BTC == 6896.55 USD
````
