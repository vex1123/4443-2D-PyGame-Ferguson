import tkinter as tk
import json

# Read in player-info json file in
with open("player-info.json") as player_info:
    pdict = json.load(player_info)

# List Player Attributes
player_attributes = ["First","Last","Rank","Email","Power-boost","Available-boosts"]

# Create window
window = tk.Tk()
window.title("Player: "+ pdict["screen_name"])

# Loop through new dictionary and format player info
index = 0
for key,value in pdict.items():
    if(key != "screen_name" and key != "available-boosts" and key != "power-boost"):
        label = tk.Label(text = player_attributes[index] + "\t\t" + ":  " + str(pdict[key]))
        label.pack(anchor = "w")
        index += 1
    if(key == "power-boost"):
        label = tk.Label(text = player_attributes[index] + "\t" + ": " + str(pdict[key]))
        label.pack(anchor = "w")
        index += 1
    if(key == "available-boosts"):
        value = ",  ".join(value)
        label = tk.Label(text = player_attributes[5] + "\t" + ":  " + str(value))
        label.pack(anchor = "w")

window.mainloop()

