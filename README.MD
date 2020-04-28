THIS SCRIPT IS NOW DEPRECATED. TURNIP EXCHANGE ADDED BOT DEFENSE SERVICES WHICH PREVENT THE AUTOMATED API PULLS USED IN THIS SCRIPT. SORRY FOR THE INCONVENIENCE. Send me a message if you have any workarounds.

Animal Crossing: New Horizons Turnip Exchange Alert Service

Allows you to set criteria for islands that pop up on the Turnip Exchange, if the price goes over and certain threshold
and the amount of players in queue are lower the your criteria receive a sound notification with information in text
form. The command prompt will also give you the link to the island on Turnip Exchange to copy and paste into your 
browser for quick queueing.

*Requirements:*

* Python 3 + packages in requirements.txt

*Usage:*
```buildoutcfg:usage
python .\turnip-scraper.py -p <price> -q <queue> -t <timeinterval>
```

* -t: Time interval to check Turnip Exchange server in seconds
* -p: Price to alert on if island price is greater than
* -q: Queue to alert on if island queue is less than
