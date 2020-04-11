from __future__ import print_function
import requests
import threading
import sys
import argparse
import time
import json
from playsound import playsound


screenlock = threading.Semaphore(value=1)

turnipcodes = {}

class TurnipScraper:
    def __init__(self, verbose, timeinterval, price, queue):
        self.verbose = verbose
        self.API_URL = "https://api.turnip.exchange"
        self.timeinterval = int(timeinterval)
        self.price = price
        self.queue = queue

    def IslandDictBuilder(self, turnipcodedict):
        turnipcodes[turnipcodedict["turnipCode"]] = {}
        turnipcodes[turnipcodedict["turnipCode"]]['name'] = turnipcodedict["name"]
        turnipcodes[turnipcodedict["turnipCode"]]['fruit'] = turnipcodedict["fruit"]
        turnipcodes[turnipcodedict["turnipCode"]]['turnipPrice'] = turnipcodedict["turnipPrice"]
        turnipcodes[turnipcodedict["turnipCode"]]['hemisphere'] = turnipcodedict["hemisphere"]
        turnipcodes[turnipcodedict["turnipCode"]]['islandTime'] = turnipcodedict["islandTime"]
        turnipcodes[turnipcodedict["turnipCode"]]['description'] = turnipcodedict["description"]
        turnipcodes[turnipcodedict["turnipCode"]]['queued'] = turnipcodedict["queued"]
        turnipcodes[turnipcodedict["turnipCode"]]['creationTime'] = turnipcodedict["creationTime"]

    def IslandDictExists(self, turnipcode):
        if turnipcode in turnipcodes.keys():
            return True
        else:
            return False

    def IslandDictCreationTimeCheck(self, turnipcode):
        if turnipcode["creationTime"] == turnipcodes[turnipcode["turnipCode"]]['creationTime']:
            return True
        else:
            return False

    def IslandDictUpdater(self, turnipcodedict):
        turnipcodes[turnipcodedict["turnipCode"]]['name'] = turnipcodedict["name"]
        turnipcodes[turnipcodedict["turnipCode"]]['fruit'] = turnipcodedict["fruit"]
        turnipcodes[turnipcodedict["turnipCode"]]['turnipPrice'] = turnipcodedict["turnipPrice"]
        turnipcodes[turnipcodedict["turnipCode"]]['hemisphere'] = turnipcodedict["hemisphere"]
        turnipcodes[turnipcodedict["turnipCode"]]['islandTime'] = turnipcodedict["islandTime"]
        turnipcodes[turnipcodedict["turnipCode"]]['description'] = turnipcodedict["description"]
        turnipcodes[turnipcodedict["turnipCode"]]['queued'] = turnipcodedict["queued"]
        turnipcodes[turnipcodedict["turnipCode"]]['creationTime'] = turnipcodedict["creationTime"]

    def Alert(self, turnipcode):
        print("\n[!!!] TURNIP ALERT: TURNIP PRICE AND QUEUE HAVE MET YOUR CRITERIA [!!!]")
        print("Island Name:\t\t%s" % turnipcodes[turnipcode]["name"])
        print("Price:\t\t\t%s bells" % turnipcodes[turnipcode]["turnipPrice"])
        print("Currently in queue:\t%s" % turnipcodes[turnipcode]["queued"])
        print("Description:\t\t%s" % turnipcodes[turnipcode]["description"])
        print("Copy and paste the following link to your browser and join the queue:")
        print("\nhttps://turnip.exchange/island/%s\n\n" % turnipcode)
        playsound('SFX.mp3')

    def CriteriaCheck(self, turnipcode):
        if turnipcodes[turnipcode]["turnipPrice"] >= int(self.price) and turnipcodes[turnipcode]["queued"] <= int(self.queue):
            return True
        else:
            return False

    def NookCrook(self):
        try:
            result = None
            response = requests.get(self.API_URL + "/islands")
            try:
                result = response.json()
            except json.decoder.JSONDecodeError:
                print("[X] Island API call returned nothing, you may need to set your time interval higher")
                result = None
                
            if result is None:
                return
            
            if 'islands' in result.keys():
                for islanddictionary in result["islands"]:
                    islanddictionary = islanddictionary
                    if not self.IslandDictExists(islanddictionary["turnipCode"]):
                        self.IslandDictBuilder(islanddictionary)
                        if self.CriteriaCheck(islanddictionary["turnipCode"]):
                            self.Alert(islanddictionary["turnipCode"])
                    if self.IslandDictExists(islanddictionary["turnipCode"]):
                        if not self.IslandDictCreationTimeCheck(islanddictionary):
                            self.IslandDictUpdater(islanddictionary)
                            if self.CriteriaCheck(islanddictionary["turnipCode"]):
                                self.Alert(islanddictionary["turnipCode"])
        except requests.ConnectionError:
            print("[X] Islands pull failed, you may need to set your time interval higher")
            pass

    def STALNKS(self):
        try:
            while True:
                self.NookCrook()
                time.sleep(self.timeinterval)
        except KeyboardInterrupt:
            print("You killed it.")
            sys.exit()


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Turnip Exchange API ')
        parser.add_argument('-s', '--proxy', default=False, help='Specify SOCKS5 proxy (i.e. 127.0.0.1:8123)')
        parser.add_argument('-v', '--verbose', default=False, action='store_true',
                            help='Output in verbose mode while script runs')
        parser.add_argument('-t', '--timeinterval', default=60, help='Time interval to check server in seconds')
        parser.add_argument('-p', '--price', default=300, help='Price to alert on if island price is greater than')
        parser.add_argument('-q', '--queue', default=100, help='Queue to alert on if island queue is less than')

        args = parser.parse_args()
        self.banner()
        scraper = TurnipScraper(args.verbose, args.timeinterval, args.price, args.queue)
        scraper.STALNKS()

    def banner(self):
            print("""
                            @@@@   
          @@@@@@@@@@@      @@@@    
        @@@@@@@@@@@@@@@@  @@       
       @@@@@@@@@@@@@@@@@@@@        
      @@@@@@@@@@@@@@@@@@@@@@@@@    
      @@@@@@@@@@@@@@@@@@@@@@@@@@@  Turnip Exchange Scraper Service
     @@@@@@@@@@@@@@@@@@@@@@@@@@@@  STALNKS!
    @@@@@@@@@@@@@@@@    &@@@@@@@@  @bashexplode
   @@@@@@@@@@@@@@(         @@@@@   
   @@@@@@@@@@@@@@          @@@     
       @@@@@@@@@@@                                        
                   """)


if __name__ == "__main__":
    try:
        Main()
    except KeyboardInterrupt:
        print("You killed it.")
        sys.exit()
