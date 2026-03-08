import tkinter as tk
from tkinter import ttk,messagebox,simpledialog
from material_lib import BoardLibrary
from order import OrderManagement
import json
1
#####Creating main window=============================
window=tk.Tk()
window.title("Board Library Management System")
window.geometry("900x700")   #The size of window

####scroll==============================Scrollbar====================
canvas = tk.Canvas(window)
scroll = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scroll.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.configure(yscrollcommand=scroll.set)

mainFrame=ttk.Frame(canvas)
mainFrame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=mainFrame, anchor="nw")

####call the class====================================
board_lib=BoardLibrary()
orderMgr=OrderManagement()


####order function==============================order function====================
#refresh
def refresh_orderList():
    orderListbox.delete(0,tk.END)
    if not orderMgr.orderList:
        return
    for i in orderMgr.orderList:
        board_count=len(i.boardList)
        displayText=f"{i.community}|{i.roomNum}|{i.status}|Board:{board_count}"
        orderListbox.insert(tk.END,displayText)

#create
def create_order():
    commnity=entry_com.get().strip()
    roomnum=entry_roomnum.get().strip()
    if not commnity or not roomnum:
        messagebox.showerror("Error","Empty!")
        return
    #call order.py
    orderMgr.addOrders(commnity,roomnum,[])
    #clear and refresh
    entry_com.delete(0,tk.END)
    entry_roomnum.delete(0,tk.END)
    refresh_orderList()
    messagebox.showinfo("Success","Order Created!")

#delete
def delete_order():
    selected=orderListbox.curselection()
    if not selected:
        messagebox.showerror("Error","Please select a order first!")
        return
    #call delete function
    index=selected[0]
    if orderMgr.deleteOrders(index):
        refresh_orderList()
        messagebox.showinfo("Success","Order deleted successfully!")
    else:
        messagebox.showerror("Error","Failed to delete order!")
   

#change
def change_order():
    s=orderListbox.curselection()
    if not s:
        messagebox.showerror("Error","Select order first!")
        return
    index=s[0]
    order=orderMgr.orderList[index]
    #change status
    if order.status=="pending":
        order.status="completed"
    else:
        order.status="pending"
    #save and refresh
    orderMgr.saveOrders()
    refresh_orderList()
    messagebox.showinfo("Success",f"Status changed to:{order.status}")

#show board of order
def showBoardInO():
    #1.clean view box
    orderBoardList.delete(0,tk.END)
    #2.select order?
    selectedOrder=orderListbox.curselection()
    if not selectedOrder:
        messagebox.showerror("Error","Please select an order first!")
        return
    orderIndex=selectedOrder[0]
    targetOrder=orderMgr.orderList[orderIndex]
    #3.If the order didn't have board
    if not targetOrder.boardList:
        orderBoardList.insert(tk.END,"No boards in this order yet.")
        return
    #show board
    for b in targetOrder.boardList:
        brand=b["brand"]
        color=b["color"]
        factory=b["factory"]
        quantity=b["quantity"]
        data=f"Brand:{brand}|Color:{color}|Factory:{factory}|Quantity:{quantity}"
        orderBoardList.insert(tk.END,data)

#export
def export():
    export_data = []
    for order in orderMgr.orderList:
        for board in order.boardList:
            export_data.append({
                "community": order.community,
                "room": order.roomNum,     
                "brand": board["brand"],
                "color": board["color"],
                "quantity": board.get("quantity", 1)
            })
    # save as  JSON file
    with open("task1_orders.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("Export successfully", f"Exported {len(export_data)} plates are recorded in the  task1_orders.json")
#=================================================================================



####Board function ==============================================
#refresh board
def refresh_boardList():
    boardListbox.delete(0,tk.END)
    #get all board
    allBoard=board_lib.get_allBoard()
    for b in allBoard:
        showText="Brand: "+b.brand+"|Color: "+b.color+"|Factory: "+b.factory
        boardListbox.insert(tk.END,showText)

#add board
def add_board():
    #1.get the conntent in input box
    brand=entry_brand.get().strip()
    color=entry_color.get().strip()
    factory=entry_factory.get().strip()
    #Calibrate
    if not brand or not color or not factory:
        messagebox.showerror("Error","Brand, Color, Factory cannot be empty!")
        return
    #2.call the add function
    result=board_lib.add_board(brand,color,factory)
    #3.success or failure
    if result:
        messagebox.showinfo("Success","Board registered successfully!")
        #clear input box
        entry_brand.delete(0,tk.END)
        entry_color.delete(0,tk.END)
        entry_factory.delete(0,tk.END)
        refresh_boardList()
    else:
        messagebox.showwarning("Warning","This Board already exists!")

#delete board
def delboard():
    selected=boardListbox.curselection()
    if not selected:
        messagebox.showerror("Error","Please select a board first!")
        return
    #call delete function
    i=selected[0]
    if board_lib.delete_board(i):
        refresh_boardList()
        messagebox.showinfo("Success","Board deleted successfully!")
    else:
        messagebox.showerror("Error","Failed to delete board!")
#=================================================================================



####add board to order function==================================================
def addBtoO():
    #1.get the selected order and board
    selectedOrder=orderListbox.curselection()
    selectedBoard=boardListbox.curselection()
    if not selectedOrder:
        messagebox.showerror("Error","Please select an order first!")
        return
    if not selectedBoard:
        messagebox.showerror("Error","Please select a board first!")
        return
    orderIndex=selectedOrder[0]
    boardIndex=selectedBoard[0]
    targetOrder=orderMgr.orderList[orderIndex]
    targetBoard=board_lib.board_list[boardIndex]
    #2.pop-up quantity box
    quantity = simpledialog.askinteger("Input quantity", "Please input quantity：", minvalue=1, maxvalue=1000)
    if quantity is None:
        return
   



    #2.add board into the boardList of order
    boardData={"brand":targetBoard.brand,"color":targetBoard.color,"factory":targetBoard.factory,"quantity":quantity}
    targetOrder.boardList.append(boardData)
    #3.save and refresh
    orderMgr.saveOrders()
    refresh_orderList()
    messagebox.showinfo("Success",f"Added{targetBoard.brand}({targetBoard.color})to order:{targetOrder.community}!")

def delshowBoard():
    #1.check select order
    if not orderListbox.curselection():
        messagebox.showerror("Error","Please select an order first!")
        return
    orderI=orderListbox.curselection()[0]
    targetOrder=orderMgr.orderList[orderI]
    #2.chech select board
    if not orderBoardList.curselection():
        messagebox.showerror("Error","Please select an board in this order first!")
        return
    boardInOrder=orderBoardList.curselection()[0]
    #3.delete
    try:
        del targetOrder.boardList[boardInOrder]
        orderMgr.saveOrders()
        showBoardInO()
        refresh_orderList()
        messagebox.showinfo("Success","Boad remove from order!")
    except IndexError:
        messagebox.showerror("Error","Invalid selection!")
#=================================================================================






#=================================================================================


####order frame =================================================================
frameOrder=ttk.LabelFrame(mainFrame,text="Order Management")
frameOrder.pack(fill="x",padx=20,pady=10)
#entry frame
#entry community
ttk.Label(frameOrder,text="Community: ").grid(row=0,column=0,padx=5,pady=8)
entry_com=ttk.Entry(frameOrder,width=15)
entry_com.grid(row=0,column=1,padx=5,pady=8)
#entry roomnumber
ttk.Label(frameOrder,text="Roomnumber:").grid(row=0,column=2,padx=5,pady=8)
entry_roomnum=ttk.Entry(frameOrder,width=15)
entry_roomnum.grid(row=0,column=3,padx=5,pady=8)
#create button 
btn_CreateOrder=ttk.Button(frameOrder,text="Creating",command=create_order)
btn_CreateOrder.grid(row=1,column=0,padx=10,pady=8)
#delete button
btn_DeleteOrder=ttk.Button(frameOrder,text="Delete",command=delete_order)
btn_DeleteOrder.grid(row=1,column=1,padx=10,pady=8)
#change button
btn_changeStatus=ttk.Button(frameOrder,text="Changing Status",command=change_order)
btn_changeStatus.grid(row=1,column=2,padx=10,pady=8)
#show board button
btn_showBoard=ttk.Button(frameOrder,text="Show Board",command=showBoardInO)
btn_showBoard.grid(row=1,column=3,padx=10,pady=8)
#show board frame
frame_view_board=ttk.Labelframe(mainFrame,text="Board in This Order")
frame_view_board.pack(fill="x",padx=10,pady=10)
#show board list
orderBoardList=tk.Listbox(frame_view_board,width=60,height=4,exportselection=False)
orderBoardList.grid(row=0,column=0,padx=5,pady=5)
#order list 
orderListbox=tk.Listbox(frameOrder,width=60,height=5,exportselection=False)
orderListbox.grid(row=2,column=0,columnspan=6,pady=5)
#
btnexport=ttk.Button(frameOrder,text="Export",command=export)
btnexport.grid(row=1,column=4)
#=======================================================================================






#======================================board frame=================================================
frame_input=ttk.LabelFrame(mainFrame,text="Register New Board")
frame_input.pack(fill="x",padx=20,pady=10)  #size

#input box
#enter brand
ttk.Label(frame_input,text="Brand:").grid(row=0,column=0,padx=5,pady=8)
entry_brand=ttk.Entry(frame_input)
entry_brand.grid(row=0,column=1, padx=5,pady=8)
#enter color
ttk.Label(frame_input,text="Board color").grid(row=1,column=0,padx=5,pady=8)
entry_color=ttk.Entry(frame_input)
entry_color.grid(row=1,column=1, padx=5,pady=8)
#enter factory
ttk.Label(frame_input,text="Board factory").grid(row=2,column=0,padx=5,pady=8)
entry_factory=ttk.Entry(frame_input)
entry_factory.grid(row=2,column=1, padx=5,pady=8)

#Add button
addbutt=ttk.Button(frame_input,text="Add",command=add_board)
addbutt.grid(row=0,column=2,columnspan=2,padx=10,pady=8)

#delete button
delbutt=ttk.Button(frame_input,text="Delete",command=delboard)
delbutt.grid(row=1,column=2,columnspan=2,padx=10,pady=8)


#Show the list of boar

flist=ttk.LabelFrame(mainFrame,text="Board List")
flist.pack(fill="both",expand=True,padx=20,pady=10)

#list frame
boardListbox=tk.Listbox(flist,font=("Arial",15),exportselection=False)   #style of board list
boardListbox.pack(fill="both",expand=True,padx=5,pady=5)
#=======================================================================================





#======================================add board frame=================================================
frameAddboard=ttk.LabelFrame(mainFrame,text="Add Board to Order")
frameAddboard.pack(fill="x",padx=20,pady=10)

#Display the currently selected plate
selectedOrder=ttk.Label(frameAddboard,text="Selected Order:None")
selectedOrder.grid(row=0,column=0,padx=5,pady=8)

#add board button
addBtoO_button=ttk.Button(frameAddboard,text="Add",command=addBtoO)
addBtoO_button.grid(row=0,column=1,padx=5,pady=8)

#delete button
delbutt=ttk.Button(frameAddboard,text="Delete",command=delshowBoard)
delbutt.grid(row=0,column=2,padx=5,pady=8)
#=======================================================================================





####clear selection==================================================

def clearSelection(event):
    wclass = event.widget.winfo_class()
    if wclass not in ['Listbox','Button','TButton','Entry','LabelFrame','Label']:
        orderListbox.selection_clear(0, tk.END)
        orderBoardList.selection_clear(0, tk.END)
        boardListbox.selection_clear(0, tk.END)

window.bind("<Button-1>", clearSelection)
#=======================================================================================











refresh_orderList()
refresh_boardList()


window.mainloop()
