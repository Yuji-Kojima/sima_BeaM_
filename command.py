def commands():
    def camera_move(app,args):
        app.camera_x = int(args[0])
        app.camera_y = int(args[1])

    def add_obj(app,args):
        x = int(args[0])
        y = int(args[1])
        k = args[2]
        if k not in app.objdata:
            if "origin:"+k in app.objdata:
                k = "origin:"+k
            else:
                return
        d = "n"
        if len(args) > 3:
            d = args[3]
        if d == "0":
            d = "e"
        elif d == "1":
            d = "w"
        elif d == "2":
            d = "s"
        elif d == "3":
            d = "n"

        s=0
        if len(args) > 4:
            s = int(args[4])

        app.add_obj(x,y,k,d,s)

    def del_obj(app,args):
        x = int(args[0])
        y = int(args[1])
        app.remove_obj(x, y)

    def cell_size(app,args):
        check = int(args[0])
        if check <= 0:
            return
        app.CELL = check 
        app.draw()
    def save(app,args):
        name=args[0]
        sx,sy = int(args[1]),int(args[2])
        ex,ey = int(args[3]),int(args[4])
        app.save_machine(name,sx,sy,ex,ey)

    def load(app,args):
        name = args[0]
        x,y = 0,0
        if len(args) > 1:
            x=int(args[1])
            y=int(args[2])
        app.load_machine(name,x,y)


    cmddata={
        "camera":{"func":camera_move},
        "put":{"func":add_obj},
        "del":{"func":del_obj},
        "cell":{"func":cell_size},
        "save":{"func":save},
        "load":{"func":load},
        }
    result = cmdback(cmddata,"origin")
    return result

def cmdback(cmddata,dataname):
    result = {}
    for key,i in cmddata.items():
        result[key]=i
        i["from"] = dataname

    return result

    