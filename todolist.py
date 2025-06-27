import tkinter
from tkinter import *
from PIL import Image, ImageTk

root= Tk()
root.title("To-Do-List")
root.geometry("400x650+400+100")
root.configure(bg="#f0f0f0")
root.resizable(False,False)

task_list= [] 

def addTask():
    task =task_entry.get()
    task_entry.delete(0, END)

    if task:
        with open("tasklist.txt",'a') as taskfile:
            taskfile.write(f"\n{task}")
        task_list.append(task)
        listbox.insert(END, task)

def deleteTask():
    task= str(listbox.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
        with open("tasklist",'w') as taskfile:
            for task in task_list:
                taskfile.write(task+"\n")

        listbox.delete(ANCHOR)



def opentaskfile():
    
    try:
        global task_list
        with open("tasklist.txt","r") as taskfile:
            tasks= taskfile.readlines()

        for task in tasks:
            if task !='\n':
                task_list.append(task)
                listbox.insert (END, task)

    except:
        file=open('tasklist.txt', 'w')
        file.close() 

# --------------------------------- icon --------------------------------- 
Image_icon=PhotoImage(file="image/task.png")
root.iconphoto(False,Image_icon)

# --------------------------------- header ---------------------------------
img = ImageTk.PhotoImage(Image.open("image/header.png"))
Label(root,image=img).pack()

dockImage = PhotoImage(file="image/dock.png")
Label(root,image=dockImage,bg="#19191A").place(x=30,y=25)

noteImage=PhotoImage(file="image/task.png")
Label(root,image=noteImage,bg="#19191A").place(x=340,y=25)

heading=Label(root,text="List of Tasks", font="arial 20 bold",fg="white", bg="#19191A") 
heading.place(x=110,y=20)

# --------------------------------- main ---------------------------------
frame=Frame(root,width=400,height=50, bg="white")
frame.place(x=0,y=130)

task=StringVar()
task_entry= Entry(frame,width=18,font="arial 20" ,bd=0)
task_entry.place(x=10,y=7)
task_entry.focus() 

button=Button(frame,text="ADD",font="arial 20 bold", width=6, bg="#080808", fg="#fff",bd=0, command=addTask)
button.place(x=300,y=0)

# --------------------------------- listbox ---------------------------------
frame1=Frame(root,bd=3,width=700,height=380,bg="#19191A")
frame1.pack (pady=(80,0))

listbox= Listbox(frame1, font=('arial', 12),width=40,height=20,bg="#1c1d1f", fg="white", cursor="hand2",selectbackground="#40444b")
listbox.pack(side=LEFT, fill=BOTH, padx=2)

# --------------------------------- scrollbar ---------------------------------
scrollbar=Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)


listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

opentaskfile()

# --------------------------------- deleteicon ---------------------------------
delete_icon = ImageTk.PhotoImage(Image.open("image/delete.png"))
Button(root, image=delete_icon, bd=0, command=deleteTask).pack(side=BOTTOM,pady=13,)


root.mainloop()
