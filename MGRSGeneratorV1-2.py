import tkinter as tk
import math
import pyperclip
from mgrs import MGRS

class MGRSCoordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("MGRS Coordinate Generator")

        self.mgrs_label = tk.Label(master, text="Enter MGRS Coordinate:")
        self.mgrs_label.pack()
        self.mgrs_entry = tk.Entry(master)
        self.mgrs_entry.pack()

        self.distance_label = tk.Label(master, text="Enter Distance (in meters):")
        self.distance_label.pack()
        self.distance_entry = tk.Entry(master)
        self.distance_entry.pack()

        self.direction_label = tk.Label(master, text="Enter Direction (in degrees):")
        self.direction_label.pack()
        self.direction_entry = tk.Entry(master)
        self.direction_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.generated_label = tk.Label(master, text="New MGRS Coordinate:")
        self.generated_label.pack()

        self.generated_text = tk.Text(master, height=1, state='disabled')
        self.generated_text.pack()

    def calculate(self):
        mgrs_coord = self.mgrs_entry.get()
        distance = float(self.distance_entry.get())
        direction = float(self.direction_entry.get())

        lat, lon = MGRS().toLatLon(mgrs_coord)
        R = 6378.1  # Radius of the Earth in km
        brng = math.radians(direction)  # Bearing is converted to radians.
        d = distance / 1000  # Distance m converted to km
        lat1 = math.radians(lat)  # Current lat point converted to radians
        lon1 = math.radians(lon)  # Current long point converted to radians

        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                                 math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        new_mgrs_coord = MGRS().toMGRS(lat2, lon2)

        self.generated_text.configure(state='normal')
        self.generated_text.delete(1.0, 'end')
        self.generated_text.insert('end', new_mgrs_coord)
        self.generated_text.configure(state='disabled')

        # Copy the new MGRS coordinate to the clipboard
        pyperclip.copy(new_mgrs_coord)

root = tk.Tk()
app = MGRSCoordGenerator(root)
root.mainloop()

