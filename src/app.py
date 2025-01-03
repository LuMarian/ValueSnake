import tkinter as tk
from flask import Flask, request
from threading import Thread
from queue import Queue
import random
import hashlib

# Initialize Flask app
app = Flask(__name__)

# Global variables to store data and speed
data = []
speed = 0
vla = 0
totalSpin = 0
hla = 0
current_hash = None

# Queue for GUI updates
data_queue = Queue()

# Helper function to extract case-insensitive keys
def get_case_insensitive(data_item, key, default=""):
    for k, v in data_item.items():
        if k.lower() == key.lower():
            return v
    return default

# Function to update the GUI if data changes
def update_gui_if_changed(new_data):
    global current_hash
    new_hash = hashlib.md5(str(new_data).encode()).hexdigest()
    if new_hash != current_hash:
        current_hash = new_hash
        update_gui(new_data)

# Function to update the GUI
def update_gui(new_data):
    # Clear previous widgets (tiles)
    for widget in frame.winfo_children():
        widget.destroy()

    # Ensure there are always 12 items (add empty data if necessary)
    while len(new_data) < 12:
        new_data.append({"headline": "Empty", "num": "N/A"})

    # Sort the data alphabetically by the "headline" (case-insensitive)
    sorted_data = sorted(new_data[:9], key=lambda x: get_case_insensitive(x, "headline").casefold())

    # Display data as rows of tiles (3 columns, 4 rows)
    for i, item in enumerate(sorted_data): 
        row, col = divmod(i, 3) 

        # Create a tile with fixed size and background color black
        tile = tk.Frame(frame, bd=1, relief="solid", width=450, height=240, bg="black")
        tile.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Get the headline and number with case-insensitivity
        headline = get_case_insensitive(item, "headline", "Unknown")
        num = get_case_insensitive(item, "num", 0)

        # If headline is "clubSpeed" and num is < 1, generate a random value - useful for chip shots
        if headline.lower() == "clubspeed" and isinstance(num, (int, float)) and num < 1:
            num = random.uniform(0.95, 1.1) * speed
        
        # format tiles so they fit the fskit traineddata
        if isinstance(num, (int, float)):
            if headline.lower() in ["totalspin", "backspin", "sidespin"]:
                formatted_num = f"{int(num):,}"  # Format as integer with commas
            elif headline.lower() in ["spinaxis", "hla", "vla"]:
                formatted_num = f"{num:.1f}\u00b0".rstrip('0').rstrip('.')  # Add degree symbol
            else:
                formatted_num = f"{num:.1f}".rstrip('0').rstrip('.')
        else:
            formatted_num = "N/A"

        # Create separate labels for headline and number
        headline_label = tk.Label(
            tile, 
            text=headline, 
            font=("Stratos", 36), 
            anchor="center", 
            bg="black", 
            fg="white"
        )
        headline_label.pack(fill="x", pady=(5, 0))  # Padding to separate from the top

        num_label = tk.Label(
            tile, 
            text=formatted_num, 
            font=("Stratos", 72, "bold italic"), 
            anchor="center", 
            bg="black", 
            fg="white"
        )
        num_label.pack(fill="both", expand=True, pady=(5, 0))  # Padding to separate from the headline

    frame.update_idletasks()

# Flask route to receive data
@app.route('/wurstbrot', methods=['POST'])
def receive_data():
    global data, speed, vla, totalSpin, hla
    new_data = request.get_json()
    # output data to console
    formatted_data = [f"{item['headline']}: {item['num']}" for item in new_data]
    print("received: " + ", ".join(formatted_data))

    if isinstance(new_data, list):
        processed_data = []
        for item in new_data:
            headline = get_case_insensitive(item, "headline")
            num = get_case_insensitive(item, "num", 0)

            # Save "num" if "headline" is "speed" (case-insensitive)
            if headline.lower() == "speed":
                speed = num
            # Save "vla" (case-insensitive)
            if headline.lower() == "vla":
                vla = num
            # Save "spin"
            if headline.lower() == "totalspin":
                totalSpin = num
            # Save "spin"
            if headline.lower() == "hla":
                hla = num

            # Add the processed item to the list
            processed_data.append({"headline": headline, "num": num})

        data = processed_data
        if is_valid_shot():
            data_queue.put(processed_data)
        return {"status": "success", "message": "Data updated!"}, 200
    return {"status": "error", "message": "Invalid data format"}, 400

# Check if it was a valid shot
def is_valid_shot() -> bool:
    is_valid_shot = True
    # Eliminate stupidly high, soft, zero spin or weirdly offline registrated shots
    if (vla > 70):
        is_valid_shot = False
        print(f"Misread Launch Angle: {vla}")
    if (speed < 3):
        is_valid_shot = False
        print(f"Misread ballspeed: {speed}")
    if (totalSpin < 400):
        is_valid_shot = False
        print(f"Misread Spin: {totalSpin}")
    
    return is_valid_shot

# Function to start Flask in a separate thread
def start_flask():
    app.run(host='0.0.0.0', port=8080, threaded=True)

# Process data from the queue asynchronously
def process_queue():
    while not data_queue.empty():
        new_data = data_queue.get()
        update_gui_if_changed(new_data)
    root.after(100, process_queue)  # Check again after 100ms

# Create the GUI
root = tk.Tk()
root.title("ValueSnake")

# Set background color of the window
root.configure(bg="black")

# Set window size with enough space for 3 columns and 4 rows
root.geometry("1350x720") 

# Frame to hold the tiles
frame = tk.Frame(root, bg="black")  # Ensure the frame has the same background color
frame.pack(fill="both", expand=True)

# Ensure that each column and row is evenly distributed
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Start Flask server in a separate thread
flask_thread = Thread(target=start_flask, daemon=True)
flask_thread.start()

# Start the GUI queue processing
root.after(100, process_queue)

# Run the GUI
root.mainloop()
