from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import messagebox as mbox
from algo import main

root = Tk()
root.title("RRT")
root.geometry("1000x800")
width = 600
height = 600

canvas = Canvas(bg="white", width=width, height=height)  # график
canvas.pack(side=LEFT, anchor=CENTER, expand=1)


# BUTTONS
frame_buttons = Frame(root, relief=RAISED, borderwidth=1, background="#FFF")
frame_buttons.pack(side=RIGHT, fill=BOTH, expand=True)

# saveButton = Button(frame_buttons, text="Сохранить")
# saveButton.pack(side=TOP, padx=5, pady=5)


def getStart():
    start.append(float(startX.get()))
    start.append(float(startY.get()))
    x1, y1 = (start[0] - 3), (start[1] - 3)
    x2, y2 = (start[0] + 3), (start[1] + 3)
    canvas.create_oval(x1+300, height-y1-300, x2+300,
                       height-y2-300, fill="#ff0000")
    btnStart["state"] = "disabled"


startX = ttk.Entry(frame_buttons)
startX.pack(side=TOP, padx=5, pady=5)
startY = ttk.Entry(frame_buttons)
startY.pack(side=TOP, padx=5, pady=5)
btnStart = ttk.Button(frame_buttons, text="Add Start", command=getStart)
btnStart.pack(side=TOP, padx=5, pady=5)
start = []


def getEnd():
    end.append(float(endX.get()))
    end.append(float(endY.get()))
    x1, y1 = (end[0] - 3), (end[1] - 3)
    x2, y2 = (end[0] + 3), (end[1] + 3)
    canvas.create_oval(x1+300, height-y1-300, x2+300,
                       height-y2-300, fill="#0000ff")
    btnEnd["state"] = "disabled"


endX = ttk.Entry(frame_buttons)
endX.pack(side=TOP, padx=5, pady=5)
endY = ttk.Entry(frame_buttons)
endY.pack(side=TOP, padx=5, pady=5)
btnEnd = ttk.Button(frame_buttons, text="Add End", command=getEnd)
btnEnd.pack(side=TOP, padx=5, pady=5)

end = []


triangles = []


def getTriangle():
    x1 = float(triangle1X.get())
    y1 = float(triangle1Y.get())
    x2 = float(triangle2X.get())
    y2 = float(triangle2Y.get())
    x3 = float(triangle3X.get())
    y3 = float(triangle3Y.get())
    triangles.append(([x1, y1], [x2, y2], [x3, y3]))
    canvas.create_polygon(x1+300, 300-y1, x2+300, 300-y2,
                          x3+300, 300-y3, fill="#80CBC4", outline="#004D40")
    print(triangles)


triangle1X = ttk.Entry(frame_buttons)
triangle1X.pack(side=TOP, padx=5, pady=5)
triangle1Y = ttk.Entry(frame_buttons)
triangle1Y.pack(side=TOP, padx=5, pady=5)

triangle2X = ttk.Entry(frame_buttons)
triangle2X.pack(side=TOP, padx=5, pady=5)
triangle2Y = ttk.Entry(frame_buttons)
triangle2Y.pack(side=TOP, padx=5, pady=5)

triangle3X = ttk.Entry(frame_buttons)
triangle3X.pack(side=TOP, padx=5, pady=5)
triangle3Y = ttk.Entry(frame_buttons)
triangle3Y.pack(side=TOP, padx=5, pady=5)


def build():
    rrt = main(start, end, [-300, 300], triangles)

    for node in rrt.nodeList:
        if node.parent is not None:
            canvas.create_line(
                node.x+300, 300-node.y, rrt.nodeList[node.parent].x+300, 300-rrt.nodeList[node.parent].y, fill="#000")

    if rrt.path != 'Error':
        points = [(rrt.nodeList[data].x+300, 300-rrt.nodeList[data].y)
                  for data in rrt.path]
        canvas.create_line(points, fill="#ff0000", width=2)
    else:
        print(1)
        mbox.showwarning("Ошибка", "Не удалось найти путь")


btnTriangle = ttk.Button(
    frame_buttons, text="Add Triangle", command=getTriangle)
btnTriangle.pack(side=TOP, padx=5, pady=5)

btnBuild = ttk.Button(frame_buttons, text="Build path", command=build)
btnBuild.pack(side=TOP, padx=5, pady=5)


def clear():
    canvas.delete("all")
    start.clear()
    end.clear()
    triangles.clear()
    btnStart["state"] = "normal"
    btnEnd["state"] = "normal"


btnClear = ttk.Button(frame_buttons, text="Clear all", command=clear)
btnClear.pack(side=TOP, padx=5, pady=5)


root.mainloop()
