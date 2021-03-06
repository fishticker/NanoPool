import requests
from datetime import date
from time import sleep


class NanoPool:

    def __init__(self,address):
        self.hashrateInfo,self.payementData,self.moneyData = self.initiateConnection(address)


    def initiateConnection(self,address):
        hashrateContent = requests.get("https://api.nanopool.org/v1/eth/user/"+address)
        hashrateInfo=hashrateContent.json()
        hashrateData=hashrateInfo["data"]
        payementContent=requests.get("https://api.nanopool.org/v1/eth/payments/"+address)
        payementInfo=payementContent.json()
        payementData=payementInfo["data"]
        moneyContent=requests.get("https://api.nanopool.org/v1/eth/approximated_earnings/"+hashrateData["hashrate"])
        moneyInfo=moneyContent.json()
        moneyData=moneyInfo["data"]
        return hashrateInfo,payementData,moneyData

    def printHashrate(self):
        data = self.hashrateInfo["data"]
        print("\n"*5)
        print("NanoPool ----> {}\033[0m".format("\033[92mONLINE" if self.hashrateInfo["status"] else "\033[91mOUTLINE"))
        print("\nbalance :\t\t{} ETH".format(data["balance"]))
        print("current hashrate :\t{} Mh/s".format(data["hashrate"]))
        print("\tavgH1 : {:.4} Mh/s\t avgH6 : {:.4} Mh/s".format(data["avgHashrate"]["h1"],data["avgHashrate"]["h6"]))
        print("\tavgH3 : {:.4} Mh/s\t avgH12 : {:.4} Mh/s".format(data["avgHashrate"]["h3"],data["avgHashrate"]["h12"]))
        print()
        for worker in data["workers"]:
            print("Worker [{}]".format(worker["id"]))
            print("\thashrate :\t{} Mh/s".format(worker["hashrate"]))
            print("\tWAvgH1 : {:.4} Mh/s\t WAvgH6 : {:.4} Mh/s".format(worker["h1"],worker["h6"]))
            print("\tWAvgH3 : {:.4} Mh/s\t WAvgH12 : {:.4} Mh/s".format(worker["h3"],worker["h12"]))

    def printPayement(self):
        print("\nPayements:")
        for payement in self.payementData :
            print("\taddress: {}\n\tamount: {} ETH\t\tconfirmed: {}\033[0m".format(payement["txHash"],payement["amount"],"\033[92mTrue" if payement["confirmed"] else "\033[91mFalse"))

    def printMoney(self):
        print("\nEstimate:\n\t{:.2f}€/hour\t{:.2f}€/day\t{:.2f}€/week\t{:.2f}€/month".format(self.moneyData["hour"]["euros"],self.moneyData["day"]["euros"],self.moneyData["week"]["euros"],self.moneyData["month"]["euros"]))


#TODO: make update method



if __name__ == "__main__":
    try:
        file=open("nanopool.config","r")
        address=file.readline()[:-1]
        file.close()
        currentNano = NanoPool(address)
        while True:
            currentNano.printHashrate()
            currentNano.printPayement()
            currentNano.printMoney()
            sleep(60)

    except IOError as e:
        print(e)



# try:
#     file=open("nanopool.config","r")
#     address=file.readline()[:-1]
#     file.close()
#
# except IOError as e:
#     print(e)
#
# while True:
#     try:
#
#         ########INITIATE CONNECTION#########
#         content=requests.get("https://api.nanopool.org/v1/eth/user/"+address)
#         generalInfo=content.json()
#         data=generalInfo["data"]
#         payementContent=requests.get("https://api.nanopool.org/v1/eth/payments/"+address)
#         payementInfo=payementContent.json()
#         payementData=payementInfo["data"]
#         moneyContent=requests.get("https://api.nanopool.org/v1/eth/approximated_earnings/"+data["hashrate"])
#         moneyInfo=moneyContent.json()
#         moneyData=moneyInfo["data"]
#
#         #########HASHRATE INFO########
#         print("\n"*5)
#         print("NanoPool ----> {}\033[0m".format("\033[92mONLINE" if generalInfo["status"] else "\033[91mOUTLINE"))
#         print("balance :\t\t{} ETH".format(data["balance"]))
#         print("current hashrate :\t{} Mh/s".format(data["hashrate"]))
#         print("\tavgH1 : {:.4} Mh/s\t avgH6 : {:.4} Mh/s".format(data["avgHashrate"]["h1"],data["avgHashrate"]["h6"]))
#         print("\tavgH3 : {:.4} Mh/s\t avgH12 : {:.4} Mh/s".format(data["avgHashrate"]["h3"],data["avgHashrate"]["h12"]))
#         print()
#         for worker in data["workers"]:
#             print("Worker [{}]".format(worker["id"]))
#             print("\thashrate :\t{} Mh/s".format(worker["hashrate"]))
#             print("\tWAvgH1 : {:.4} Mh/s\t WAvgH6 : {:.4} Mh/s".format(worker["h1"],worker["h6"]))
#             print("\tWAvgH3 : {:.4} Mh/s\t WAvgH12 : {:.4} Mh/s".format(worker["h3"],worker["h12"]))
#
#         #######PAYEMENT#######
#         print("\nPayements:")
#         for payement in payementData :
#             print("\taddress: {}\n\tamount: {} ETH\t\tconfirmed: {}\033[0m".format(payement["txHash"],payement["amount"],"\033[92mTrue" if payement["confirmed"] else "\033[91mFalse"))
#
#
#         ########MONEY########
#         print("\nEstimate:\n\t{:.2f}€/hour\t{:.2f}€/day\t{:.2f}€/week\t{:.2f}€/month".format(moneyData["hour"]["euros"],moneyData["day"]["euros"],moneyData["week"]["euros"],moneyData["month"]["euros"]))
#
#
#
#         sleep(60)
#     except Exception as e:
#         print(e)
