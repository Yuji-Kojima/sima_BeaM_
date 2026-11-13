def datas():
    #x座標、y座標、向き、信号の強さ、周囲のオブジェクト、周囲の信号を受け取る。
    def off(x,y,a,b,c,d):
        return []
    
    def power(x,y,a,b,c,d):
        result=[]
        for w in range(3):
            for h in range(3):
                if w == 1 and h == 1:
                    continue
                else:
                    result.append(((x+w-1),(y+h-1),8))
        return result

    def beam(x,y,angle,b,obj,d):
        result=[]
        for i in range(1,9):
            n = 8-i
            if angle == "n":
                result.append((x,(y-i),n))
            if angle == "s":
                result.append((x,(y+i),n))
            if angle == "w":
                result.append(((x-i),y,n))
            if angle == "e":
                result.append(((x+i),y,n))
        return result

    def level_beam(x,y,angle,level,obj,d):
        result=[]
        for i in range(1,9):
            n = level-i
            if angle == "n":
                result.append((x,(y-i),n))
            if angle == "s":
                result.append((x,(y+i),n))
            if angle == "w":
                result.append(((x-i),y,n))
            if angle == "e":
                result.append(((x+i),y,n))
        return result
            
    def bishop_beam(x,y,angle,b,obj,d):
        result=[]
        for i in range(1,9):
            n = 8-i
            if angle == "n":
                result.append(((x+i),(y-i),n))
            if angle == "s":
                result.append(((x-i),(y+i),n))
            if angle == "w":
                result.append(((x-i),(y-i),n))
            if angle == "e":
                result.append(((x+i),(y+i),n))
        return result

    objdata={
            "power":{
                     "name":"電源",
                     "pass":False,
                     "on":power,
                     "off":off
                     },
            "abpower":{
                     "name":"絶対電源",
                     "pass":False,
                     "on":power,
                     "off":power
                     },
            "unpower":{
                     "name":"反抗期電源",
                     "pass":False,
                     "on":off,
                     "off":power
                     },
            "beam":{
                     "name":"直線ビーム",
                     "pass":False,
                     "on":beam,
                     "off":off
                     },
            "levelbeam":{
                     "name":"可変出力ビーム",
                     "pass":False,
                     "on":level_beam,
                     "off":off
                     },
            "bishop_beam":{
                     "name":"斜めビーム",
                     "pass":False,
                     "on":bishop_beam,
                     "off":off
                     },

        }
    result = databack(objdata,"origin")
    return result

def databack(objdata,dataname):
    result={}
    for key,i in objdata.items():
        full_key = f"{dataname}:{key}" 
        result[full_key]=i
    return result
#アドオンの作り方:
#import dataしておく。内部にdatas()メソッドを作り、中に機械用のメソッド、
#名前、信号貫通、on/off時に実行されるメソッドを入れた機械のデータの辞書をobjdata辞書に入れる。
#最後に、result = data.databack(objdata,"アドオン名")を付けて、return resultする。:

#メソッドの作り方:
#メソッド名(x座標, y座標, 向き, 信号の強さ, 世界全体のオブジェクトの辞書, 世界全体の信号の辞書)
#で作る。かならず最後に、信号を送る先のリストをreturnする。
#信号を送る先のリストの中身は、[(x座標,y座標,信号の強さ),...]とする。