#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tkinter import Tk, Grid, Frame, Entry, Button, Label, END, ttk, VERTICAL, Checkbutton, IntVar, messagebox
from tkinter.colorchooser import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pylab as pylab


class Plotter():
    def __init__(self, root):

        self.root = root
        self.root.title("r[Plotter]X")
        self.root.wm_minsize(400, 200)
        self.root.grid_anchor(anchor = 'c')

        self.first_row = 0
        self.first_column = 0
        self.max_plot = 10
        self.labels_array = [0 for i in range(0, self.max_plot)]
        self.entry_array = [0 for i in range(0, self.max_plot)]
        self.color_array = [0 for i in range(0, self.max_plot)]
        self.check_array = [0 for i in range(0, self.max_plot)]
        self.checked = [ IntVar() for i in range(0, self.max_plot)]

        frame = Frame(root)

        for each_label in range(1, self.max_plot):
            self.labels_array[each_label] = Label(frame, text = str("y" + str(each_label) + "(x) = "))
            self.labels_array[each_label].grid(row = self.first_row + 1 + each_label, column = self.first_column, sticky = "e")

        for each_entry in range(1, self.max_plot):
            self.entry_array[each_entry] = Entry(frame)
            self.entry_array[each_entry].grid(row = self.first_row + 1 + each_entry, column = self.first_column + 1)

        for each_color in range(1, self.max_plot):
            self.color_array[each_color] = Button(frame, text='█', fg = "#0c00c0", command = lambda each_color = each_color: self.getColor(each_color))
            self.color_array[each_color].grid(row = self.first_row + 1 + each_color, column = self.first_column + 2)

        for each_check in range(1, self.max_plot):
            self.check_array[each_check] = Checkbutton(frame, variable = self.checked[each_check])
            self.check_array[each_check].grid(row = self.first_row + 1 + each_check, column = self.first_column + 3)



        self.plot = Button(frame, text = "Plot", width = 10)
        self.plot.grid(row = 2 + self.max_plot, column = 1)
        self.plot.config(command = self.to_plot)

        self.line = ttk.Separator(frame, orient = VERTICAL)
        self.line.grid(sticky = "NS", row = self.first_row, column = self.first_column + 5, rowspan = 1 + self.max_plot, pady = 10)

        self.label_graph_title = Label(frame, text = "Plot Title: ")
        self.label_first_x = Label(frame, text = "Starts on x = ")
        self.label_last_x = Label(frame, text = "Ends on x = ")
        self.label_step = Label(frame, text = "Step: ")


        self.entry_graph_title = Entry(frame)
        self.entry_first_x = Entry(frame)
        self.entry_last_x = Entry(frame)
        self.entry_step = Entry(frame)


        self.label_graph_title.grid(row = self.first_row + 2, column = self.first_column + 6, sticky = "e")
        self.label_first_x.grid(row = self.first_row + 3, column = self.first_column + 6, sticky = "e")
        self.label_last_x.grid(row = self.first_row + 4, column = self.first_column + 6, sticky = "e")
        self.label_step.grid(row = self.first_row + 5, column = self.first_column + 6, sticky = "e")

        self.entry_graph_title.grid(row = self.first_row + 2, column = self.first_column + 7)
        self.entry_first_x.grid(row = self.first_row + 3, column = self.first_column + 7)
        self.entry_last_x.grid(row = self.first_row + 4, column = self.first_column + 7)
        self.entry_step.grid(row = self.first_row + 5, column = self.first_column + 7)



        self.entry_array[1].insert(END, "x**2")
        self.check_array[1].select()
        self.entry_graph_title.insert(END, "My cool plot!")
        self.entry_first_x.insert(END, "-10")
        self.entry_last_x.insert(END, "10")
        self.entry_step.insert(END, "0.5")


        frame.grid()


    def getColor(self, line):
        color = askcolor()
        self.color_array[int(line)]['fg'] = color[1]


    def to_plot(self):
        self.x = Symbol('x')

        self.xmin = float(self.entry_first_x.get())
        self.xmax = float(self.entry_last_x.get())
        self.step = abs(float(self.entry_step.get()))
        self.checkreadings = [ self.checked[x].get() for x in range(self.max_plot)]


        if self.xmax <= self.xmin:
            self.error("Last x should be greater then the first x!")
        elif (self.xmax - self.xmin) < self.step:
            self.error("Step should be smaller then range (last x - first x)!")
        elif not any(self.checkreadings):
            self.error("You should check at least one function to plot!")
        else:

            self.yy = [ [] for i in range(1, self.max_plot + 1 ) ]
            self.xx = [ [] for i in range(1, self.max_plot + 1 ) ]


            for i in range(1, self.max_plot):
                if self.entry_array[i].get() is not "" :
                    self.xzing = float(self.xmin)
                    self.y = parse_expr(self.entry_array[i].get(), evaluate = False)

                    while self.xzing <= self.xmax:
                        self.xx[i].append(self.xzing)
                        self.yy[i].append(float(self.y.subs({self.x:self.xzing})))
                        self.xzing = self.xzing + self.step


            pylab.figure("r[Plotter]X")

            for i in range(1, self.max_plot):
                if self.checkreadings[i] == 1:
                    pylab.plot(self.xx[i], self.yy[i], label = str(self.entry_array[i].get()), color = self.color_array[i]['fg'])


            pylab.xlabel("x")
            pylab.ylabel("f(x)")

            pylab.legend()
            pylab.grid()
            pylab.title(self.entry_graph_title.get())
            pylab.show()


    def error(self, message):
        messagebox.showerror("Error", message)


    def main(self):
        pass


if __name__ == "__main__":
    root = Tk()
    plotter = Plotter(root)
    plotter.main()
    root.mainloop()
