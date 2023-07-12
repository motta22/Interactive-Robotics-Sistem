from tkcalendar import Calendar, DateEntry
from tkinter import *
import datetime as dt

calendar = Tk()

today = dt.date.today()



def print_sel():
        print(cal.selection_get())
        cal.see(dt.date(year=2016, month=2, day=5))



mindate = dt.date(year=2020, month=11, day=29)
maxdate = today + dt.timedelta(days=5)
print(mindate, maxdate)



cal = Calendar(calendar, font="Arial 14", selectmode='day', mindate=mindate, maxdate=maxdate, disabledforeground='red', cursor="hand1", year=2018, month=2, day=5)
cal.pack(fill="both", expand=True)

Button(calendar, text="ok", command=print_sel).pack()


calendar.mainloop()