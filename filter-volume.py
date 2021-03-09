import requests
import time

def current_second():
    """
    fungsi ini mengembalikan nilai current second
    """
    return round(time.time())

def get_all_stocks():
    """
    fungsi ini digunakan untuk mengambil semua kode/symbol saham dan
    mengembalikan kode-kode tersebut dalam bentuk list
    """
    endpoint = "https://www.idx.co.id/umbraco/Surface/Helper/GetEmiten?emitenType=s"
    headers={'User-Agent': 'Mozilla/5.0'}
    r = requests.get(endpoint, headers=headers)
    data = r.json()
    list_stock = []
    for symbol in data:
        list_stock.append(symbol['KodeEmiten'])
    return list_stock
    
def get_ticker(symbol):
    """
    fungsi ini digunakan untuk mendapatkan ticker dari sebuah saham dan
    mengembalikan nilai ticker
    """
    endpoint = "https://tvc4.forexpros.com/88188ad8a4ba93aa158435fa11015623/1614910553/54/54/27/symbols?symbol=JAKARTA%20%3A"+symbol
    headers={'User-Agent': 'Mozilla/5.0'}
    r = requests.get(endpoint, headers=headers)
    ticker = r.json()['ticker']
    return ticker

def volume_filter(ticker, second):
    """
    fungsi ini digunakan untuk mendeteksi kenaikan volume dalam jumlah besar daripada 2 hari sebelumnya 
    dan mengembalikan nilai True jika terdapat kenaikan volume
    """
    endpoint = "https://tvc4.forexpros.com/88188ad8a4ba93aa158435fa11015623/1614910553/54/54/27/history?symbol="+ticker+"&resolution=D&from=1583806606&to="+second
    headers={'User-Agent': 'Mozilla/5.0'}    
    # get all volume
    try :
        r = requests.get(endpoint, headers=headers)    
        data = r.json()['v']    
    except Exception as e:
        print(e)
        return False
    # ambil volume 2 hari sebelumnya
    volume_2 = data[-3:-1]        
    # get latest volume
    last_volume = str(data[-1:][0])
    len_last_volume = int(len(last_volume))    

    # compare selisih digit volume 2 hari sebelumnya dengan volume terakhir
    for x in volume_2:
        x = str(x)        
        len_x = int(len(x))                
        selisih = len_last_volume - len_x                   
        if selisih < 1:
            return False            
    return True            
    
def latest_candle_up(symbol):
    """
    fungsi ini digunakan untuk mendeteksi candlestick terakhir berada di posisi naik atau turun
    dan mengembalikan nilai True jika candlestick terakhir berada di posisi naik
    """
    endpoint = "https://tvc4.forexpros.com/ce985cbfd0436c9471fe946ab112cedb/1614919007/54/54/27/quotes?symbols=Jakarta%20%3A"+symbol
    headers={'User-Agent': 'Mozilla/5.0'}
    r = requests.get(endpoint, headers=headers)    
    data = r.json()['d'][0]['v']        
    if data['open_price'] is not None and data['lp'] is not None :
        open_price = int(data['open_price'].translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}))   
        last_price = int(data['lp'].translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}))         
        if open_price < last_price:
           return True
    return False

def main():        
    second = current_second()
    watchlist_stocks = []
    stocks = get_all_stocks()
    for symbol in stocks:   
        print("Processing "+symbol)     
        if latest_candle_up(symbol):
            ticker = get_ticker(symbol)
            if volume_filter(ticker, str(second)):
                watchlist_stocks.append(symbol)                
            print(watchlist_stocks)    
    
if __name__ == '__main__':
    main()