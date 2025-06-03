# Vehicle Trajectory Visualization Tool full version (for TGSIM I395 Data)

This repository contains a Python-based interactive GUI tool for plotting vehicle trajectories from the TGSIM dataset. It allows users to filter vehicles based on time window and lane-changing behavior, and generates interactive Plotly plots showing detailed movement patterns over road boundaries.

## Features

- Filter vehicles by **time window**, **initial lane**, and **exit lane**.
- View vehicle **lane change counts** directly in the selection menu (in the format of "vehicle_id (lane change counts)").
- Plot interactive **vehicle trajectories** using Plotly with hoverable data points showing:
  - ID
  - Time
  - Lane
  - Speed
  - Acceleration
- View **lane boundaries** based on corresponding geometry CSVs.

## Example Output

The tool produces an HTML file (`I395_Full_Plot.html`) displaying the interactive plot.
![Screenshot 2025-06-03 at 3 07 39 PM](https://github.com/user-attachments/assets/003550f0-2c54-4dc0-9230-c2dff8f1ffdb)



## File Structure

```bash
.
├── TGSIM_I395.csv            # Main trajectory dataset
├── boundaries/
│   ├── I395_boundaries.csv
├── plotter.py           # Python file with Tkinter GUI and plotting code
└── README.md
```

## Dependencies

- `pandas`
- `plotly`
- `matplotlib`
- `tkinter` (built-in in most Python distributions)

You can install the required packages with:

```bash
pip install pandas plotly matplotlib
```

> `tkinter` is usually included with standard Python installations. If you're using Linux and don't have it installed, try:
>
> ```bash
> sudo apt-get install python3-tk
> ```

## How to Use

1. Download the TGSIM I395 main dataset and the boundaries files from the following website:
https://data.transportation.gov/Automobiles/Third-Generation-Simulation-Data-TGSIM-I-395-Traje/97n2-kuqi/about_data
2. Rename the main dataset to TGSIM_I395.csv and move it to the same directory as the `plotter.py` script.
3. In the same directory as `plotter.py`, create a new folder named `boundaries`, and move all the centerline files into this folder.
4. Launch the Python to run `plotter.py` and run all cells.
5. A GUI window will appear.
6. Choose a **time window**, **initial lane**, and **exit lane** (or leave as "all").
7. Select one or more vehicles from the list.
8. Click **Plot** to generate the interactive plot.

The plot will open in a browser window and also be saved as `I395_Full_Plot.html`.


## Notes

- Boundary CSV must be named in the format:  
  `I395_boundaries.csv`
- These files must be placed in the `boundaries/` directory relative to the notebook.
- The code currently writes to a fixed output file (`I395_Full_Plot.html`) — feel free to modify this for custom output names.

## License

This project is open-source

## Author

David Feng <br />
Ph.D. Student, UVA Civil & Environmental Engineering Dept.  <br />
Graduate Research Assistant, Turner-Fairbank Highway Research Center
