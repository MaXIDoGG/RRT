from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
from tkinter.ttk import *
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox as mbox
from matplotlib.patches import Polygon
from algo import main

matplotlib.use("TkAgg")
root = Tk()
root.title('RRT')


def Save():
    f = asksaveasfile(initialfile='Untitled.json',
                      defaultextension=".json", filetypes=[("All Files", "*.*"), ("Images", "*.json")])


root.geometry("1000x800")


frame_buttons = Frame(root, relief=RAISED, borderwidth=1, background="#FFF")
frame_buttons.pack(fill=BOTH, expand=True)
# Кнопка сохранения
saveButton = Button(frame_buttons, text="Сохранить",
                    command=lambda: Save())
saveButton.pack(side=LEFT, padx=5, pady=5)

figure = Figure(figsize=(10, 8), dpi=100)
plt = figure.add_subplot(1, 1, 1)


obstacle_list = [
    ([1, -10], [5, 1], [1, 10])]

rrt = main([0, 0], [8, 9], [-10, 10], obstacle_list)

for node in rrt.nodeList:
    if node.parent is not None:
        plt.plot([node.x, rrt.nodeList[node.parent].x], [
            node.y, rrt.nodeList[node.parent].y], "-g")

for (a, b, c) in obstacle_list:
    plt.plot([a[0], b[0], c[0], a[0]], [a[1], b[1], c[1], a[1]], "-b")


plt.plot(rrt.start.x, rrt.start.y, "^r")
plt.plot(rrt.end.x, rrt.end.y, "^b")
plt.axis([rrt.min_rand, rrt.max_rand, rrt.min_rand, rrt.max_rand])

if rrt.path != 'Error':
    plt.plot([rrt.nodeList[data].x for data in rrt.path], [
        rrt.nodeList[data].y for data in rrt.path], '-r')
    plt.grid(True)
else:
    print(1)
    mbox.showwarning("Ошибка", "Не удалось найти путь")


canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()


root.mainloop()


# for dot in rrt.nodeList:
#     if dot.parent == None:
#         c1.create_oval(dot.x, dot.y, dot.x+0.1, dot.y+0.1)
#     else:
#         dot1 = rrt.nodeList[dot.parent]
#         c1.create_line(dot.x, dot.y, dot1.x, dot1.y)
