import tkinter as tk
from tkinter import ttk
from backEnd import get_university_data, top_five_universities, get_exchange, get_currency_list

# Later display the criteria list in the GUI
criteriaList = ['U.S. News', 'CS Ranking', 'Placement', 'Best Paper', 'Comprehensive']

# # Read display format or the option lists will be folded 
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# Clear all text fields and combos
def reset():
    resultbox.delete(0, tk.END)
    budget_entry.delete(0, tk.END)
    currency_combo.set("")
    criteria_combo.set("")

# Search for recommended schools
def search(budget, curr, criteria):
    # Clear the result field first
    resultbox.delete(0, tk.END)

    # Check whether the user choose a currency
    if len(curr) == 0:
        resultbox.insert(0, "Search failed.")
        resultbox.insert(0, "Please choose a currency.")
        return

    # Check whether the user choose a criteria
    if len(criteria) == 0:
        resultbox.insert(0, "Search failed.")
        resultbox.insert(0, "Please choose a criteria.")
        return


    # Check whether the user input a valid number
    try:
        budget = int(budget)
    except ValueError:
        budget_entry.delete(0, tk.END)
        budget_entry.insert(0, "Invalid input. Please reset and enter a number")
    
    # Call get_exchange() to transfer the budget to USD
    budgetUSD = get_exchange(budget, curr)
    try:
        budgetUSD = int(budgetUSD)
    except ValueError:
        resultbox.delete(0, tk.END)
        resultbox.insert(tk.END, budgetUSD)

    # Call get_university_data to get the data frame that scraped from web & read from csv
    university = get_university_data()
    if isinstance(university, str):
        resultbox.delete(0, tk.END)
        resultbox.insert(tk.END, university)

    
    # Call top_five_universities() to search for recommended schools
    top_five = top_five_universities(university, budgetUSD, criteria)
    # If the budget is too low, the list can be empty
    if len(top_five) == 0:
        resultbox.insert(tk.END, "I'm sorry but your budget is not enough to study CS in North America,")
        resultbox.insert(tk.END, "I suggest you consider schools in other regions or choose to study online.")
    # Print out the recommendation    
    else:
        resultbox.insert(tk.END, "The recomended universities are")
        for i in top_five:
            resultbox.insert(tk.END,i)


# Build a GUI and name it
root = tk.Tk()
root.title('CS Universities Recommendation System')

# The first label
budget_label = tk.Label(root, text='How much is your budget in your own currency?')
budget_label.pack()

# User enter their budget here
budget_entry = tk.Entry(root)
budget_entry.pack()

# The second label
currency_label = tk.Label(root, text='Please enter the currency you are using:')
currency_label.pack()

# User choose their currency here
currency_combo = ttk.Combobox(root, values=get_currency_list())
currency_combo.pack()

# The third label
criteria_label = tk.Label(root, text='Which ranking would you like to refer to:')
criteria_label.pack()

# User choose their criteria here
criteria_combo = ttk.Combobox(root, values=criteriaList)
criteria_combo.pack()

# Set the search button, bind it with search()
buttonSearch = tk.Button(root, text="Search", command=lambda: search(budget_entry.get(), currency_combo.get(), str(criteria_combo.get())))
buttonSearch.pack()

# Set the reset button, bind it with reset()
buttonReset = tk.Button(root, text="Reset", command=lambda: reset())
buttonReset.pack()

# Build a text field here
resultbox = tk.Listbox(root, width=60)
resultbox.pack()

# Run the GUI
root.mainloop()