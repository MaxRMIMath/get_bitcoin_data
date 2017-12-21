import json
import requests
import datetime
import time

'''
all data get from https://btc.com
bitStruct is a calss with no initial paramater, and having following methods
    
    getOneDayBlock(day):
        "day" with form "YYYYMMDD" 
        getting all blockheads in specific day
    
    getOneHeightTransaction(height):
        "height" with datatype integer
        getting all transactions in specific height
        return a list of Transactions in this height

    getOneDayTransaction(day):
        "day" with form "YYYYMMDD" 
        getting all transactions in specific day

    getOneDayBlockAndTx(day)
        "day" with form "YYYYMMDD"
        getting all entire blocks in specific day

    getBlocksAndTxs(fromDay,toDay):
        "fromDay" with form "YYYYMMDD"
        "toDay" with form "YYYYMMDD"
        getting all entire blocks in a range of days
'''

class bitStruct(object):
    '''
    import json
    import requests
    import datetime
    import time
    '''
    def __init__(self):
        self.block={}
    def getOneDayBlock(self,day):
        url = "https://chain.api.btc.com/v3/block/date/"+str(day)
        data = requests.get(url).text
        data  = json.loads(data)
        self.block[day]=data['data']
        if data['err_no']!=0:
            raise "err_no!=0 error"
        print(day,"block list done")
    def getOneDayBlockAndTx(self,day):
        self.getOneDayBlock(day)
        self.getOneDayTransaction(day)
    def getBlocksAndTxs(self,fromDay,toDay):
        fromDayObj=datetime.datetime.strptime(fromDay,"%Y%m%d")
        toDayObj=datetime.datetime.strptime(toDay,"%Y%m%d")
        date_list_obj = [fromDayObj + datetime.timedelta(days=x) for x in range(0,(toDayObj-fromDayObj).days)]
        date_list=[i.__format__("%Y%m%d") for i in date_list_obj]
        for day in date_list:
            time.sleep(1)
            self.getOneDayBlock(day)
            self.getOneDayTransaction(day)
    def getOneHeightTransaction(self,height):
        url = "https://chain.api.btc.com/v3/block/"+str(height)+"/tx"
        data = requests.get(url).text
        data  = json.loads(data)
        if data['err_no']!=0:
            raise "err_no!=0 error"
        pages=int(data['data']['total_count']/50)+1
        newdata=data['data']['list']
        print("height: ",height,"  pages:  1  in ",pages)
        for i in range(2,pages+1):
            time.sleep(1)
            url = "https://chain.api.btc.com/v3/block/"+str(height)+"/tx"
            data = requests.get(url).text
            data  = json.loads(data)
            if data['err_no']!=0:
                raise "err_no!=0 error"
            newdata=newdata+data['data']['list']
            print("height: ",height,"  pages: ",i," in ",pages)
        return newdata
    def getOneDayTransaction(self,day):
        length=len(self.block[day])
        for i in range(length):
            time.sleep(1)
            height=self.block[day][i]['height']
            self.block[day][i]['tx']=self.getOneHeightTransaction(height)


AugToNov=bitStruct()
