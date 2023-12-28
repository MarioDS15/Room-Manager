import tkinter as tk
import gui

if __name__ == "__main__":
    root = tk.Tk()
    app = gui.Application(root)
    root.mainloop()

"""
Add rented items to display
Implement remove entry
Fix display (grid)
Auto update time (Threading)
Check out system
Make time entry be 12 hour format and do not include seconds
Add checkout everyone button
Add tabs, FAQ, quick fix, item inventory, etc

"""