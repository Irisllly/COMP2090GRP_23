# COMP2090 course project
<Task1> Board Inventory and Order Management System
1.Overview:
    Task 1 is a desktop application developed in Python using Object‑Oriented Programming. It helps a board trading company manage its board inventory and customer orders. Users can add different types of boards (brand, colour, factory) to the library, create orders, add boards to orders (with quantity), delete boards from orders, and change order status. All data is saved persistently in JSON files.
  
2.Core function:
2.1: Board Library Management: Add a new board (brand, colour, factory) – duplicate check prevents same brand+colour. Delete a selected board from the library. View all boards in a list.
2.2: Order Management: Create a new order by entering community and room number. Delete an existing order. Change order status between “pending” and “completed”. View all orders with a summary of how many boards each contains.
2.3: Board‑Order Association: Select an order and a board, then add the board to the order with a specified quantity. Remove a board from an order. When viewing an order, all its boards (with brand, colour, quantity) are displayed.
2.4: Data Persistence: Automatically load data from board.json and orders.json on startup; automatically save after any modification.
  
3.GUI
The graphical interface is built with Python’s tkinter. It features a scrollable main canvas containing input fields, buttons, and listboxes. Data is stored in two JSON files: board.json holds the global board library, and orders.json holds all orders. Each order’s board list is stored as an array of dictionaries with brand, colour, and quantity. The program reads these files at startup and writes to them after every change, ensuring data consistency across sessions.



==========================================================================
<Task2> Procurement Summarisation(Union-Find)
1.Overview
To demonstrate its practical use, we applied it to group board items exported from Task 1 by brand and colour. The result is a standalone HTML page that visualises the grouping and shows a procurement summary – i.e., for each brand+colour, the total quantity needed and which orders require it.

2.Union-Find Data Structure
Union‑Find maintains a collection of disjoint sets. It supports two main operations:
2.1: find(x): returns the representative (root) of the set containing x. Application path compression, speeding up future queries.
2.2: union(x, y): merges the two sets that contain x and y. In this implementation, we use a simple union for clarity.

3.Data Linkage with Task1
The tow tasks are linked through a JSON data file exported from Task1 and loaded into a standalone HTML page for Task2. We added an "Export" button that generates a file of all board items in the required format. This file is then loaded into the Task 2 HTML page. 








