import requests
import datetime
import time



class bitStruct(object):
    '''
    import json
    import requests
    import datetime
    import time
    '''
    def __init__(self):
        self.block={}
        self.data={}
    def getOneDayBlock(self,day):
        url = "https://chain.api.btc.com/v3/block/date/"+str(day)
        time.sleep(0.2)
        data = requests.get(url).json()
        self.block[day]=data['data']
        if data['err_no']!=0:
            raise "err_no!=0 error"
        print(day,"block list done")
    def getOneDayBlockAndTx(self,day):
        self.getOneDayBlock(day)
        self.getOneDayTransaction(day)
    def getTxs(self,fromDay,toDay):
        fromDayObj=datetime.datetime.strptime(fromDay,"%Y%m%d")
        toDayObj=datetime.datetime.strptime(toDay,"%Y%m%d")
        date_list_obj = [fromDayObj + datetime.timedelta(days=x) for x in range(0,(toDayObj-fromDayObj).days)]
        date_list=[i.__format__("%Y%m%d") for i in date_list_obj]
        for day in date_list:
            self.getOneDayTransaction(day)
    def getBlocks(self,fromDay,toDay):
        fromDayObj=datetime.datetime.strptime(fromDay,"%Y%m%d")
        toDayObj=datetime.datetime.strptime(toDay,"%Y%m%d")
        date_list_obj = [fromDayObj + datetime.timedelta(days=x) for x in range(0,(toDayObj-fromDayObj).days)]
        date_list=[i.__format__("%Y%m%d") for i in date_list_obj]
        for day in date_list:
            self.getOneDayBlock(day)
    def getBlocksAndTxs(self,fromDay,toDay):
        fromDayObj=datetime.datetime.strptime(fromDay,"%Y%m%d")
        toDayObj=datetime.datetime.strptime(toDay,"%Y%m%d")
        date_list_obj = [fromDayObj + datetime.timedelta(days=x) for x in range(0,(toDayObj-fromDayObj).days)]
        date_list=[i.__format__("%Y%m%d") for i in date_list_obj]
        for day in date_list:
            self.getOneDayBlock(day)
            self.getOneDayTransaction(day)
            print(day,": ")
    def getOneHashTransaction(self,ahash):
        url = "https://blockchain.info/rawblock/"+ahash
        data = requests.get(url).json()
        height=data["height"]
        print("height: ",height)
        return data["tx"]
    def getOneDayTransaction(self,day):
        length=len(self.block[day])
        for i in range(length):
            print("day: ",day,"  blocks: ", i," in ",length )
            time.sleep(20)
            ahash=self.block[day][i]['hash']
            self.block[day][i]['tx']=self.getOneHashTransaction(ahash)
    def findattr(self,attr,fromDay,toDay):
        fromDayObj=datetime.datetime.strptime(fromDay,"%Y%m%d")
        toDayObj=datetime.datetime.strptime(toDay,"%Y%m%d")
        date_list_obj = [fromDayObj + datetime.timedelta(days=x) for x in range(0,(toDayObj-fromDayObj).days)]
        date_list=[i.__format__("%Y%m%d") for i in date_list_obj]
        data={}
        for day in date_list:
            for i in reversed(self.block[day]):
                if attr != "extras":
                    data[i["height"]]=i[attr]
                else:
                    data[i["height"]]=i[attr]["pool_name"]
        if attr != "extras":
            self.data[attr]=data
        else:
            self.data["pool_name"]=data
        return data

fromDay="20090109"
toDay="20171221"
bitcs=bitStruct()
bitcs.getBlocks(fromDay,toDay)
for i in bitcs.block[fromDay][0].keys():
    bitcs.findattr(i,fromDay,toDay)

import pickle
with open("dataFrom"+fromDay+"To"+toDay+".pkl","wb") as f:
    pickle.dump(bitcs,f)

