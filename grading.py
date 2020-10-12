import numpy as np
from tkinter import Button, Label, Frame, Tk, Entry, END, Checkbutton, IntVar
import pyperclip


class Homework:
    def __init__(self, master):

        self.copy_btn = Button(master=master, text="copy result ", command=self.copy_output)
        self.copy_btn.grid(column=0, row=0)

        self.add_btn = Button(master=master, text="add problem ", command=self.add_problem)
        self.add_btn.grid(column=1, row=0)

        self.rst_btn = Button(master=master, text="reset ", command=self.reset)
        self.rst_btn.grid(column=2, row=0)

        self.master_frame = Frame(master=master)
        self.master_frame.grid(column=1, row=1)

        self.count = 1
        self.problems = [Problem(self.master_frame, 0)]

    def add_problem(self):
        self.problems += [Problem(self.master_frame, self.count)]
        self.count += 1

    def copy_output(self):
        total_deducted = 0
        total_problems = len(self.problems)
        comment_str = ''
        for index, problem in enumerate(self.problems):
            comments, deducted = problem.get_missed_and_comment(total_problems)
            if len(comments)>0:
                comment_str += "Problem " + str(index + 1) + "\n"
            else:
                continue
            for comment in comments:
                comment_str += comment + "\n"
            total_deducted += ((deducted / (total_problems * 100)) * 10)
            comment_str += "\n"
            p = 0

        start_str = "final grade= " + str(10 - total_deducted) + '\n'
        out_str = start_str + comment_str
        pyperclip.copy(out_str)

    def reset(self):
        for problem in self.problems:
            problem.rest_chks()


class Problem:
    def __init__(self, master, row):
        self.count = 1
        self.missed = []

        self.problem_frame = Frame(master=master)
        self.problem_frame.grid(column=0, row=row)

        self.problem_lbl = Label(master=self.problem_frame, text='problem:' + str(row + 1))
        self.problem_lbl.grid(column=0, row=0)

        self.add_btn = Button(master=self.problem_frame, text="add ", command=self.add_correction)
        self.add_btn.grid(column=1, row=0)

    def add_correction(self):
        self.missed += [Missed(self.problem_frame, self.count)]
        self.count += 1

    def get_missed_and_comment(self, problem_count):
        total_deducted = 0
        comments = []
        for miss in self.missed:
            check = miss.get_chk()
            if check == 0:
                continue
            point = miss.get_points()
            if point == '0':
                continue
            comments += [miss.get_comment() + " points deducted: -" + str(
                (float(miss.get_points()) / (100 * problem_count)) * 10)]
            total_deducted += int(miss.get_points())
        return comments, total_deducted

    def rest_chks(self):
        for miss in self.missed:
            miss.set_false()


class Missed:
    def __init__(self, master, count):
        self.text = ''
        self.points = 0

        self.comment_txt = Entry(master=master)
        self.comment_txt.grid(column=0, row=count)
        self.comment_txt.insert(END, "")

        self.point_txt = Entry(master=master)
        self.point_txt.grid(column=1, row=count)
        self.point_txt.insert(END, "0")

        self.var = IntVar()
        self.chk = Checkbutton(master, text=" ", variable=self.var)
        self.chk.grid(column=2, row=count)

    def get_points(self):
        return self.point_txt.get()

    def get_comment(self):
        return self.comment_txt.get()

    def get_chk(self):
        return self.var.get()

    def set_false(self):
        self.var.set(False)



window = Tk()
window.title("grading app")
window.geometry('1300x900')


master_frame = Frame(master=window)
master_frame.grid(column=0, row=0)

hw = Homework(master_frame)

window.mainloop()
