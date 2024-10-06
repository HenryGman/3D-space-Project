import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math


zoom_factor = 1.1


def calculate_distance(point1, point2):
    return np.linalg.norm(point2 - point1)


def calculate_direction(point1, point2):
    direction_vector = point2 - point1
    yaw = math.degrees(math.atan2(direction_vector[1], direction_vector[0]))
    pitch = math.degrees(math.atan2(direction_vector[2], np.linalg.norm(direction_vector[:2])))
    return yaw, pitch


def display_additional_info(point1, point2, distance, yaw, pitch):
    info = (
        f"Coordinates of Object 1 (Green): ({point1[0]}, {point1[1]}, {point1[2]})\n"
        f"Coordinates of Object 2 (Red): ({point2[0]}, {point2[1]}, {point2[2]})\n"
        f"Distance between objects: {distance:.2f} units\n"
        f"Direction to face from Object 1 to Object 2:\n"
        f"Yaw (horizontal angle): {yaw:.2f} degrees\n"
        f"Pitch (vertical angle): {pitch:.2f} degrees"
    )
    label_info.config(text=info)

def plot_objects(point1, point2, zoom=1.0):
    fig = plt.Figure(figsize=(6,5))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(point1[0], point1[1], point1[2], color='green', s=100, label='Object 1')
    ax.scatter(point2[0], point2[1], point2[2], color='red', s=100, label='Object 2')
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], color='blue')
    ax.view_init(elev=30, azim=30)
    midpoint = (point1 + point2) / 2
    padding = 0.1 
    range_x = (abs(point1[0] - point2[0]) * zoom) * (1 + padding) / 2
    range_y = (abs(point1[1] - point2[1]) * zoom) * (1 + padding) / 2
    range_z = (abs(point1[2] - point2[2]) * zoom) * (1 + padding) / 2
    range_x = max(range_x, 1)
    range_y = max(range_y, 1)
    range_z = max(range_z, 1)
    ax.set_xlim([midpoint[0] - range_x, midpoint[0] + range_x])
    ax.set_ylim([midpoint[1] - range_y, midpoint[1] + range_y])
    ax.set_zlim([midpoint[2] - range_z, midpoint[2] + range_z])

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()

    return fig



def calculate_and_plot(zoom=1.0):
    try:
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        z1 = float(entry_z1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        z2 = float(entry_z2.get())
        point1 = np.array([x1, y1, z1])
        point2 = np.array([x2, y2, z2])
        
  
        distance = calculate_distance(point1, point2)
        yaw, pitch = calculate_direction(point1, point2)
        
        fig = plot_objects(point1, point2, zoom)
    
        for widget in frame_plot.winfo_children():
            widget.destroy()  # Clear the previous plot

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        toolbar = NavigationToolbar2Tk(canvas, frame_plot)
        toolbar.update()
        canvas.get_tk_widget().pack()
        display_additional_info(point1, point2, distance, yaw, pitch)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all coordinates.")

def zoom_in():
    global zoom_factor
    zoom_factor /= 1.1
    calculate_and_plot(zoom_factor)

def zoom_out():
    global zoom_factor
    zoom_factor *= 1.1
    calculate_and_plot(zoom_factor)


root = tk.Tk()
root.title("3D Object Visualizer")

font_large = ("Helvetica", 12, "bold")
font_medium = ("Helvetica", 10)
font_small = ("Helvetica", 8)

frame_input = tk.Frame(root, padx=20, pady=20)
frame_input.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
frame_plot = tk.Frame(root, padx=20, pady=20, bg="white", relief=tk.RAISED, borderwidth=2)
frame_plot.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)
label_title = tk.Label(frame_input, text="Enter Coordinates for 3D Visualization", font=font_large)
label_title.grid(row=0, column=0, columnspan=2, pady=10)
label_obj1 = tk.Label(frame_input, text="Object 1 (Green)", font=font_medium)
label_obj1.grid(row=1, column=0, columnspan=2, pady=(10, 5))
label_x1 = tk.Label(frame_input, text="x1:")
label_x1.grid(row=2, column=0)
entry_x1 = tk.Entry(frame_input)
entry_x1.grid(row=2, column=1)
label_y1 = tk.Label(frame_input, text="y1:")
label_y1.grid(row=3, column=0)
entry_y1 = tk.Entry(frame_input)
entry_y1.grid(row=3, column=1)
label_z1 = tk.Label(frame_input, text="z1:")
label_z1.grid(row=4, column=0)
entry_z1 = tk.Entry(frame_input)
entry_z1.grid(row=4, column=1)
label_obj2 = tk.Label(frame_input, text="Object 2 (Red)", font=font_medium)
label_obj2.grid(row=5, column=0, columnspan=2, pady=(20, 5))
label_x2 = tk.Label(frame_input, text="x2:")
label_x2.grid(row=6, column=0)
entry_x2 = tk.Entry(frame_input)
entry_x2.grid(row=6, column=1)
label_y2 = tk.Label(frame_input, text="y2:")
label_y2.grid(row=7, column=0)
entry_y2 = tk.Entry(frame_input)
entry_y2.grid(row=7, column=1)
label_z2 = tk.Label(frame_input, text="z2:")
label_z2.grid(row=8, column=0)
entry_z2 = tk.Entry(frame_input)
entry_z2.grid(row=8, column=1)
button_calculate = tk.Button(frame_input, text="Calculate and Plot", font=font_medium, command=calculate_and_plot, bg="lightblue", relief=tk.RAISED)
button_calculate.grid(row=9, column=0, columnspan=2, pady=10)
button_zoom_in = tk.Button(frame_input, text="Zoom In", font=font_medium, command=zoom_in, bg="lightgreen", relief=tk.RAISED)
button_zoom_in.grid(row=10, column=0, pady=10)
button_zoom_out = tk.Button(frame_input, text="Zoom Out", font=font_medium, command=zoom_out, bg="lightcoral", relief=tk.RAISED)
button_zoom_out.grid(row=10, column=1, pady=10)
label_info = tk.Label(frame_input, text="", font=font_small, justify=tk.LEFT, anchor='w')
label_info.grid(row=11, column=0, columnspan=2, pady=10)


root.mainloop()
