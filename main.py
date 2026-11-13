import tkinter as tk
import data
import command
import json
root = tk.Tk()
root.geometry("400x300")
root.title("sima_BeaM")
class App():
    def __init__(self):
        self.objdata = data.datas()
        self.obj = {}
        self.signal={}
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()
        self.camera_x = 0
        self.camera_y = 0
        self.undo=[]
        self.CELL = 20
        #キー入力部分
        self.keys = set()
        root.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<Button-1>", self.on_click)
        self.entry=None
        #コマンド部分
        self.commands = command.commands()

    def main(self):
        self.signal={}
        for (x,y),item in self.obj.items():
            d = self.objdata[item["kind"]]#objdataのキーを
            if item["signal"] > 0 :
                func = d["on"]
            else:
                func = d["off"]
            for px,py,signal_level in func(x,y,item["dir"],item["signal"],self.obj,self.signal):
                if signal_level > self.signal.get((px,py),0):
                    self.signal[(px,py)] = signal_level
        for pos,item in self.obj.items():
            item["signal"] = self.signal.get(pos,0)
            

        
    def draw(self):
        
        self.canvas.delete("all")
        CELL = self.CELL
        for y in range(300//self.CELL):
            for x in range(400//CELL):
                wx = x + self.camera_x
                wy = y + self.camera_y
                signal_level = self.signal.get((wx,wy))
                if signal_level:
                    self.canvas.create_rectangle(x*CELL,y*CELL,x*CELL+CELL,y*CELL + CELL,fill="yellow", outline="gray")
                    self.canvas.create_text(
                    x*CELL+CELL//2, y*CELL+CELL//2, text=str(signal_level))
        for y in range(300//CELL):
            for x in range(400//CELL):
                wx = x + self.camera_x
                wy = y + self.camera_y
                obj = self.obj.get((wx,wy))
                if obj:
                    self.canvas.create_rectangle(x*CELL+(CELL*0.05),y*CELL+(CELL*0.05),x*CELL+CELL-(CELL*0.05),y*CELL + CELL-(CELL*0.05))
                    self.canvas.create_text(
                                        x*CELL+CELL//2, y*CELL+CELL//2, text=str(self.objdata[obj["kind"]]["name"]))
    def loop(self,draw=True):
        self.main()
        if draw == True:
            self.draw()
        root.after(200, self.loop)

    def add_obj(self,x,y,kind,dir,signal=0,undo=True):
        self.obj[(x,y)]={"kind": kind, "dir": dir, "signal": signal}
        self.draw()
    def remove_obj(self,x,y):
        remove = self.obj.pop((x,y),None)
        if remove == None:
            return
        kind=remove["kind"]
        dir=remove["dir"]
        self.undo.append([x,y,kind,dir,0])
        self.draw()

    def undo_obj(self):
        if len(self.undo) > 0:
            undo = self.undo.pop()
            x=undo[0]
            y=undo[1]
            k=undo[2]
            d=undo[3]
            self.add_obj(x,y,k,d,0,undo=False)

    def on_key_press(self,e):
        k = e.keysym
        if self.entry:
            return
        print(k)
        if k == "w":
            self.draw()
            self.camera_y -= 1
        if k == "s":
            self.draw()
            self.camera_y += 1
        if k == "a":
            self.draw()
            self.camera_x -= 1
        if k == "d":
            self.draw()
            self.camera_x += 1
        if k == "slash":
            self.open_command()
 
    def on_click(self,e):
        x,y = e.x,e.y
        px = x//self.CELL
        py = y//self.CELL
        ex = px + self.camera_x
        ey = py + self.camera_y
        print(f"座標:{ex},{ey}")
        if (ex,ey) in self.obj:
            print(f"obj {self.obj[(ex,ey)]["kind"]}")

    def open_command(self):
        if self.entry:
            return
        self.keys.clear()
        self.entry = tk.Entry(root)
        self.entry.place(x=0, y=280, width=400)
        self.entry.focus_set()  #入力を受け取る場所(focus)をsetする
        self.entry.bind("<Return>", self.run_command)   # Enterで run_command
        self.entry.bind("<Escape>", self.close_command)

    def run_command(self,e):
        parts = []
        item = ""
        c = self.entry.get()
        print(c)
        for i in c:
            if i == "," or i == " ":
                parts.append(item)
                item = ""
                continue
            item += i
        parts.append(item)
        cmd = parts.pop(0)
        try:
            self.commands[cmd]["func"](self,parts)
        except Exception as ex:
            print(f"エラー!{cmd}:{ex}")
        self.close_command()

    def close_command(self,e=None):
        if self.entry:
            self.entry.destroy()
        self.entry = None
        root.focus_set() 

    def save_machine(self,name,sx,sy,ex,ey):
        try:
            s = {}
            count = 0
            for (x,y),item in self.obj.items():
                if ex>= x >=sx and ey>= y >=sy:
                    s[count] = item
                    s[count]["x"]=x-sx
                    s[count]["y"]=y-sy
                    count += 1
                    
            if len(s) == 0:
                print("セーブ範囲内に何もありません！")
                return

            with open(f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(s, f, indent=2)
            print(f"{name}.jsonを正常に保存しました！")
        except Exception as ex:
            print(f"セーブに失敗しました！ 理由:{ex}")
            return
        
    def load_machine(self,filename,sx=0,sy=0):
        with open(f"{filename}.json", "r", encoding="utf-8") as f:
            d = json.load(f)
        result = {}

        for key,i in d.items():
            x=i["x"]
            y=i["y"]
            result[(x,y)]=i
        for key,item in result.items():
            self.add_obj(key[0]+sx,key[1]+sy,item["kind"],item["dir"],item["signal"])
        print(f"{filename}.jsonを({sx},{sy})に正常に読み込みました！")



            

def test():
    items=[]
    items.append([2,2,"origin:unpower","n",0])
    items.append([3,2,"origin:beam","s",0])
    items.append([3,9,"origin:unpower","s",0])
    items.append([2,9,"origin:beam","n",0])
    items.append([3,3,"origin:levelbeam","e",0])
    items.append([3,4,"origin:levelbeam","e",0])
    items.append([3,5,"origin:levelbeam","e",0])
    items.append([3,6,"origin:levelbeam","e",0])
    items.append([3,7,"origin:levelbeam","e",0])
    items.append([3,8,"origin:levelbeam","e",0])
    for i in items:
        app.add_obj(i[0],i[1],i[2],i[3],i[4])
    app.remove_obj(3,4)

def to_int(value):
    try:
        return int(value)
    except:
        return None

app = App()
app.loop()
root.mainloop()

