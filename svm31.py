#coding:utf-8                                                                   
import csv
import pandas as pd 
import numpy
import sqlite3

#-------------------------------
#DataBase
#        kabuka.dbを使う
#--------------------------------
class DataBase:
    def __init__(self):
        self.connector = sqlite3.connect("kabuka.db")
        self.cursor = self.connector.cursor()
    def Recordset(self,sql):
        self.cursor.execute("select code,date,data1,data2,data3,data4,eval from kabuka")
        result = self.cursor.fetchall()
        for row in result:
            print(row[0],row[1])
        self.cursor.close()
        self.connector.close()
	#------------------------
    #Recordset_trainingdata
    #--------------------------
    def Recordset_trainingdata(self,date,sql):
        tmp=""
        count=0
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            #---------------------------------
            # 1    2    3     4     5     6
			# code,date,data1,data2,data3,data4
            #----------------------------------
            #print(row[0],row[1],row[2],row[3],row[4],row[5])
            if count==0:
                tmp=tmp+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","
                count=count+1
            else:
                tmp=tmp+row[2]+","+row[3]+","+row[4]+","+row[5]+","
                count=count+1
        
        self.cursor.close()
        self.connector.close()
        return(tmp)
    #--------------------------------
    #  traindatamake
    #  日経225のデータ kabuka.db
    #  d   data
    #  l   label
    #--------------------------------
    def traindatamake(self,d,l):
        sql="select code,date,data1,data2,data3,data4 from kabuka where date='"+d+"'"
        tmp=""
        count=0
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            #---------------------------------
            # 1    2    3     4     5     6
			# code,date,data1,data2,data3,data4
            #----------------------------------
            #print(row[0],row[1],row[2],row[3],row[4],row[5])
            if count==0:
                tmp=tmp+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","
                count=count+1
            else:
                tmp=tmp+row[2]+","+row[3]+","+row[4]+","+row[5]+","
                count=count+1
        tmp=tmp+l
        self.cursor.close()
        self.connector.close()
        #print(tmp)
        return(tmp)



class Data:
    """A simple example class"""         # 三重クォートによるコメント
    def __init__(self):                  # コンストラクタ
        self.name = ""

    def getName(self):                   # getName()メソッド
        return self.name

    def setName(self, name):             # setName()メソッド
        self.name = name

    def ReadCode(self):             # setName()メソッド
        code225=[]
        with open('code.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                code225.append(row['code'])
        return(code225)
    #---------
    #readData
    #---------
    def readData(self,fn):
        Close=[]
        Date=[]
        with open(fn) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Close.append(row['Close'])
                Date.append(row['Date'])
        return(Close,Date)
    #--------------
    #Reverse_List
    #--------------
    def Reverse_List(self,data):
        l=len(data)
        W=[]
        for i in range(l-1,-1,-1):
            W.append(data[i])
        return(W)
    #------------------
    #Nikkei225DataGet
    #-------------------
    def Nikkei225DataGet(self):
        fn="nikkei225.dat"
        Close=[]
        Date=[]
        with open(fn) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Close.append(row['Close'])
                Date.append(row['Date'])
        return(Date,Close)


def main1():
    a = Data()                            # クラスのインスタンスを生成
    #a.setName("Tanaka")                      # setName()メソッドをコール
    #print(a.getName())
    #print(a.ReadCode())
    code225=a.ReadCode()
    #----------------------
    #Loop 個別の２２５株
    #----------------------
    print("code,date,data1,data2,data3,data4,eval")
    for j in range(0,224):
        fn="YH_JP_"+code225[j]+".csv"
        #print(a.readData(fn))
        Close,Date=a.readData(fn)
        Close=a.Reverse_List(Close)
        Date =a.Reverse_List(Date)
        W_Close=[]
        W_Date =[]
        for i in range(0,len(Close)-5):
            #print(Date[i],"  ",Close[i])
            wc1=float(Close[i+1])/float(Close[i])
            wc2=float(Close[i+2])/float(Close[i])
            wc3=float(Close[i+3])/float(Close[i])
            wc4=float(Close[i+4])/float(Close[i])
            wc5=float(Close[i+5])/float(Close[i])
            if Close[i]<Close[i+5]:
                w="1"
            else:
                w="0"
            m=str(code225[j]).strip()+","+str(Date[i]).strip()+","+str(round(wc1,2)).strip()+","+str(round(wc2,2)).strip()+","+str(round(wc3,2)).strip()+","+str(round(wc4,2)).strip()+","+str(w).strip()
            print(m)

		#print(code225[i]," "Date[i]," ",round(wc1,2)," ",round(wc2,2)," ",round(wc3,2)," ",round(wc4,2),"  ",w," ",Close[i],"-",Close[i+5]," ",round(wc5,2))



#----------------------------
#日経２２５のデータでスウィング
#----------------------------
def main2():
    a = Data()                            # クラスのインスタンスを生成
    #a.setName("Tanaka")                      # setName()メソッドをコール
    #print(a.getName())
    print(a.ReadCode())
    code225=a.ReadCode()
    print("日経平均株価２２５Data")
    ND,NC=a.Nikkei225DataGet()
    for i in range(0,len(ND)-5):
	
        wc1=float(NC[i+1])/float(NC[i])
        wc2=float(NC[i+2])/float(NC[i])
        wc3=float(NC[i+3])/float(NC[i])
        wc4=float(NC[i+4])/float(NC[i])
        wc5=float(NC[i+5])/float(NC[i])
        if NC[i]<NC[i+5]:
            w="H"
        else:
            w="L"
        print(ND[i]," ",NC[i],"  ",round(wc1,2)," ",round(wc2,2)," ",round(wc3,2)," ",round(wc4,2),"  ",w)


def main3():
    d=DataBase()
    d.Recordset("select * from kabuka")

#------------
# makedata
#------------
def makedata(date,code):
    sql="select code,date,data1,data2,data3,data4,eval from kabuka where date='"+date+"'"
    #日経平均株価は２００７年からしかないので
    sql="select * from kabuka where "
    sql=sql+"(date like '2007%') or "
    sql=sql+"(date like '2008%') or "
    sql=sql+"(date like '2009%') or "
    sql=sql+"(date like '201%-%') "
    #print(sql)
    d=DataBase()
    d1=d.Recordset_trainingdata(date,sql)
    return(d1)


#---------------------------------------------------------------------------------
#mina4
#以下の処理を書く
#以下ここでは日経平均ん株価のデータを日付をキーにして
#kabudbでアクセスして教師データを作る
#１、日経平均株価を読み込む
#２、日付と日経平均に選ばれているコードを検索してをキーにして４日分データを作る
#３、これを日付２２５のコードを一列にする
#--------------------------------------------------------------------------------
def main4():
    tmp=""
    nikeiheikinkabuka_data=pd.read_csv("nikkei225.dat")
    d=Data()
    nikei225code=d.ReadCode()
    #print(nikei225code)
	#日付をとる
    #print("日付に",len(nikeiheikinkabuka_data["Date"])-1))
	
	
#   for i in range(0,len(nikeiheikinkabuka_data["Date"])-1):
    for i in range(0,10):
        d1=nikeiheikinkabuka_data["Date"][i]
        for j in range(0,len(nikei225code)-1):
            #print(d1,nikei225code[j])
            tmp=tmp+makedata(d1,nikei225code)
        print(tmp)
        tmp=""
#--------------------------
#main5
#svmで学習 Date,Start,High,Low,Close
#--------------------------
def main5():
    diff=4
    d=pd.read_csv("nikkei225.dat")
    for i in range(0,len(d["Close"][i]-1)):
        d1=d["Date"][i]
        d2=d["Close"][i]
        d3=d["Date"][i+diff]
        d4=d["Close"][i+diff]
        if d2<d3:
           print(d1,"H")
        else:
           print(d1,"L")
#-----------------------------------------------
#mian6
#NOTE アヤメのSVMのプログラムをサンプルにコードを改変
#python svm31.py > tarin_kabudata.csvでトレーニングデータができる
#tarin_kabudata.csv
#
#トレーニングデータのテーブルスキーマ
#   date,data1,data1,data1,data1,data2......data225,data225,data225,data225
#   2007-12-28,1.1,1,2......
#以下はラベルのテーブルスキーマ
#nikkei225traindata.csv
#date label
#2007-12-28 L
#2007-12-27 L
#2007-12-26 L
#2007-12-25 L
#
#------------------------------------------------
def main6():
    label=pd.read_csv("nikkei225traindata.csv")#日経２２５の四日後のデータが上がったか下がったかを判定する
    total_len=len(label)                       #総数データ(日経225)
    train_len=int(len(label)*2/3)              #トレーニングデータ2/3はトレーニングデータ残りはテストデータ
    test_len=total_len-train_len               #テストデータの数
    train_data=[]   #トレーニングデータ
    train_label=[]  #
    test_data=[]    #テストデータ
    test_label=[]   #
    i=0
    print("訓練データ",train_len)
    print("全体のデータ",total_len)
    Data_num=len(label["Date"])
    print("日経２２５のデータの数",Data_num)
    count=0
	#日経２２５の教師データだけループす
    for j in range(0,Data_num-1):
    #for j in range(0,12):
        nikkeidata=DataBase()
        d=label["Date"][j]
        l=label["label"][j]
        if count<train_len:
            train_data.append(nikkeidata.traindatamake(d,l))
        else:
            test_data.append(nikkeidata.traindatamake(d,l))
        count=count+1
        print("count=",count)
    print(len(train_data))
    
	#------------------------
    #配列からファイルに書き込む
    #------------------------
    tmp2=""
    for k in range(0,len(train_data)-1):
        tmp2=tmp2+train_data[k]+'\n'
    f=open('train_data.csv',"w")
    f.write(tmp2)
    f.close
    
    tmp2=""
    for k in range(0,len(test_data)-1):
        tmp2=tmp2+test_data[k]+'\n'
    f=open('test_data.csv',"w")
    f.write(tmp2)
    f.close






    #----------------------
    #データを書きこむ
    #-----------------------
    df1 = pd.DataFrame(train_data)
    df1.to_csv("traindata.csv")
    df1 = pd.DataFrame(test_data)
    df1.to_csv("testdata.csv")
    #---------
    #svm学習
    #---------
	#tbl=pd.read_csv("traindata.csv")
    #clf=svm.SVC()
    #clf.fit(data_train,label_train)
    #predict=clf.predict(data_test)
	
	#dt1=pd.read_csv("traindata.csv")
    #dt2=pd.read_csv("")
	
    #clf=svm.SVC()
    #clf.fit(data_train,label_train)
    #predict=clf.predict(data_test)





if __name__ == '__main__':
	main6()







