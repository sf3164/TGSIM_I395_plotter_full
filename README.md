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
<img width="1304" alt="Screenshot 2025-06-18 at 11 07 56 AM" src="https://github.com/user-attachments/assets/8b09275c-724a-404c-913c-f3a2c28c05d6" />


## File Structure

```bash
.
├── updated_TGSIM_I395.csv            # Main trajectory dataset
├── boundaries/
│   ├── updated_I395_boundaries.csv
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

1. Use the updated TGSIM I395 maindatasets and the boundary file.
2. Make sure the updated main dataset updated_TGSIM_I395.csv is in the same directory as the `plotter.py` script.
3. Create a folder `boundaries` containing the updated boundary file updated_I395_boundaries.csv, and make sure the folder is in the same directory as `plotter.py`
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
