import pandas as pd
import plotly.graph_objects as go
import os
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk, messagebox

# File Paths
TRAJECTORY_FILE = "TGSIM_I395.csv"

CENTERLINE_FILE = os.path.join("boundaries", "I395_boundaries.csv")

# === Load trajectory data ===
traj_df = pd.read_csv(TRAJECTORY_FILE)

# === Initialize Tkinter window ===
root = tk.Tk()
root.title("Vehicle Trajectory Plotter")

# === Global Variables ===
selected_time = tk.StringVar()
selected_initial_lane = tk.StringVar()
selected_exit_lane = tk.StringVar()

def initialize_time_and_lane_options():
    try:
        min_time = int(traj_df["time"].min())
        max_time = int(traj_df["time"].max())

        time_windows = ["all"] + [f"{t}-{t+60}" for t in range(min_time, max_time, 60)]
        time_menu["values"] = time_windows
        selected_time.set("")

        unique_lanes = sorted(traj_df["lane_kf"].dropna().unique().astype(int))
        lane_options = ["all"] + [str(lane) for lane in unique_lanes]
        initial_lane_menu["values"] = lane_options
        exit_lane_menu["values"] = lane_options
        selected_initial_lane.set("all")
        selected_exit_lane.set("all")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_vehicle_options(*args):
    try:
        time_window = selected_time.get()
        run_data = traj_df

        if time_window != "all":
            start_time, end_time = map(int, time_window.split("-"))
            vehicles_in_time_range = run_data[
                (run_data["time"] >= start_time) & (run_data["time"] <= end_time)
            ]["id"].unique()
        else:
            vehicles_in_time_range = run_data["id"].unique()

        full_traj_data = traj_df[
            traj_df["id"].isin(vehicles_in_time_range)
        ].sort_values(["id", "time"])

        first_last_lanes = full_traj_data.groupby("id").agg(
            initial_lane=("lane_kf", "first"),
            exit_lane=("lane_kf", "last"),
            lane_changes=("lane_kf", lambda x: (x.diff().fillna(0) != 0).sum())
        ).reset_index()

        initial_lane_filter = selected_initial_lane.get()
        exit_lane_filter = selected_exit_lane.get()

        if initial_lane_filter != "all":
            first_last_lanes = first_last_lanes[first_last_lanes["initial_lane"] == int(initial_lane_filter)]

        if exit_lane_filter != "all":
            first_last_lanes = first_last_lanes[first_last_lanes["exit_lane"] == int(exit_lane_filter)]

        vehicle_listbox.delete(0, tk.END)
        for _, row in first_last_lanes.iterrows():
            vid = int(row["id"])
            lane_change_count = int(row["lane_changes"])
            vehicle_listbox.insert(tk.END, f"{vid} ({lane_change_count} lane changes)")

    except ValueError:
        messagebox.showerror("Error", "Invalid selection.")

def plot_trajectories():
    try:
        time_window = selected_time.get()
        selected_indices = vehicle_listbox.curselection()
        selected_vehicle_ids = [int(vehicle_listbox.get(i).split()[0]) for i in selected_indices]

        if not selected_vehicle_ids:
            messagebox.showerror("Error", "No vehicles selected.")
            return

        max_x = traj_df['xloc_kf'].max()
        max_y = traj_df['yloc_kf'].max()
        filtered_traj = traj_df[traj_df["id"].isin(selected_vehicle_ids)]

        if not os.path.exists(CENTERLINE_FILE):
            messagebox.showerror("Error", f"Centerline file not found: {CENTERLINE_FILE}")
            return
        centerline_df = pd.read_csv(CENTERLINE_FILE)

        color_list = list(mcolors.TABLEAU_COLORS.values())
        vehicle_color_map = {vid: color_list[i % len(color_list)] for i, vid in enumerate(selected_vehicle_ids)}

        fig = go.Figure()

        # Plot all lane centerlines
        for lane in centerline_df.columns:
            if lane.startswith("x"):
                lane_number_raw = lane[1]  # e.g., "1", "2", ...
                lane_centerline_column_x = f"x{lane_number_raw}"
                lane_centerline_column_y = f"y"
        
                if lane_centerline_column_x in centerline_df.columns and lane_centerline_column_y in centerline_df.columns:
                    lane_centerline = centerline_df[[lane_centerline_column_x, lane_centerline_column_y]].dropna()
        
                    # Compute logical lane number using your formula
                    try:
                        lane_index = int(lane_number_raw)
                        logical_lane_number = -1 * (6 - lane_index)
                        label_text = f"Lane {logical_lane_number}<br>left boundary"
                    except:
                        logical_lane_number = lane_number_raw  # fallback if conversion fails
                        label_text = f"Lane {logical_lane_number}<br>left boundary"
        
                    # Plot the lane boundary
                    fig.add_trace(go.Scatter(
                        x=lane_centerline[lane_centerline_column_x]*0.3,
                        y=lane_centerline[lane_centerline_column_y]*0.3,
                        mode="lines",
                        line=dict(color="#D3D3D3", width=1.5),
                        name=f"Lane {logical_lane_number}<br>left boundary"
                    ))
        
                    # Add label at the end of the centerline
                    max_y_idx = lane_centerline[lane_centerline_column_y].idxmax()
                    end_x = lane_centerline.at[max_y_idx, lane_centerline_column_x]*0.3
                    end_y = lane_centerline.at[max_y_idx, lane_centerline_column_y]*0.3

                    fig.add_trace(go.Scatter(
                        x=[end_x],
                        y=[end_y],
                        mode="text",
                        text=[label_text],
                        textposition="top center",
                        showlegend=False
                    ))


        for vehicle_id in selected_vehicle_ids:
            vehicle_data = filtered_traj[filtered_traj["id"] == vehicle_id]
            if not vehicle_data.empty:
                hover_texts = [
                    f"ID:{vehicle_id}<br>Time: {t}s<br>Lane: {int(lane)}<br>Speed: {speed:.2f} m/s<br>Acceleration: {accel:.2f} m/s²"
                    for t, lane, speed, accel in zip(vehicle_data["time"], 
                                                     vehicle_data["lane_kf"], 
                                                     vehicle_data["speed_kf"], 
                                                     vehicle_data["acceleration_kf"])
                ]

                fig.add_trace(go.Scatter(
                    x=vehicle_data["xloc_kf"], 
                    y=vehicle_data["yloc_kf"], 
                    mode="markers",
                    marker=dict(size=5),
                    line=dict(color=vehicle_color_map[vehicle_id], width=2),
                    name=f"Vehicle {vehicle_id}",
                    text=hover_texts,
                    hoverinfo="text+x+y"
                ))

        fig.update_layout(
            title="Vehicle Trajectories",
            xaxis=dict(range=[0, max_x]),
            yaxis=dict(range=[0, max_y]),
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            legend_title="Legend",
            template="plotly_white"
        )

        fig.write_html("I395_Full_Plot.html")
        fig.show()

    except ValueError:
        messagebox.showerror("Error", "Invalid vehicle selection.")

# === UI Setup ===
tk.Label(root, text="Select Time Window:").grid(row=0, column=0)
time_menu = ttk.Combobox(root, textvariable=selected_time, state="readonly")
time_menu.grid(row=0, column=1)
time_menu.bind("<<ComboboxSelected>>", update_vehicle_options)

tk.Label(root, text="Initial Lane:").grid(row=1, column=0)
initial_lane_menu = ttk.Combobox(root, textvariable=selected_initial_lane, state="readonly")
initial_lane_menu.grid(row=1, column=1)
initial_lane_menu.bind("<<ComboboxSelected>>", update_vehicle_options)  

tk.Label(root, text="Exit Lane:").grid(row=2, column=0)
exit_lane_menu = ttk.Combobox(root, textvariable=selected_exit_lane, state="readonly")
exit_lane_menu.grid(row=2, column=1)
exit_lane_menu.bind("<<ComboboxSelected>>", update_vehicle_options)  

tk.Label(root, text="Select Vehicles:").grid(row=3, column=0)
vehicle_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
vehicle_listbox.grid(row=3, column=1)

tk.Button(root, text="Plot", command=plot_trajectories).grid(row=4, column=0, columnspan=2)

# === Initialize Dropdowns ===
initialize_time_and_lane_options()

root.mainloop()
