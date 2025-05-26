# Nim Game 3D Visualization

This project provides tools for generating and visualizing Nim game losing positions in 3D space. Nim is a mathematical game of strategy where players take turns removing objects from piles, and the player who removes the last object wins.

The visualization reveals a fascinating mathematical pattern - the Sierpinski tetrahedron (also known as the Sierpinski pyramid). This fractal pattern emerges naturally from the Nim losing positions and demonstrates the deep connection between combinatorial game theory and fractal geometry.

## Requirements

- Python 3.7+
- Plotly
- Pandas

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip3 install plotly pandas
```

## Usage

### Generating Nim Losing Positions

The `generate_nim_data.py` script generates all possible losing positions in Nim where the XOR of pile sizes equals 0. Run it with:
```bash
python3 generate_nim_data.py --max_value 50
```

This will generate all losing positions where pile sizes range from 0 to 50 and save them to `nim_data.csv`. The script will also display the number of losing positions found and show some sample positions.

### Visualizing the Data

The `3d_plot.py` script creates an interactive 3D visualization of the Nim losing positions. Run it with:
```bash
python3 3d_plot.py nim_data.csv
```

The visualization will open in your default web browser and show:
- A 3D scatter plot of all losing positions
- Interactive features allowing you to:
  - Rotate the plot
  - Zoom in/out
  - Pan around
  - Hover over points to see their values
- Color-coded points showing the XOR value (which is always 0 for losing positions)

## Features

- Generates all Nim losing positions (where XOR of pile sizes equals 0)
- Handles permutations of pile sizes
- Creates interactive 3D scatter plots
- Customizable max value for pile sizes
- Visualizes patterns in Nim losing positions

## Example

To generate and visualize Nim losing positions for pile sizes up to 50:

```bash
# Generate data
python3 generate_nim_data.py --max_value 50

# Visualize the data
python3 3d_plot.py nim_data.csv
```

## Output

The visualization reveals the Sierpinski tetrahedron fractal pattern in the Nim losing positions, showing:
- The origin point (0,0,0) at the center
- Diagonal lines and planes forming tetrahedral structures
- Symmetry in the distribution of points
- Larger gaps between points as values increase, creating the fractal pattern
- Self-similar structures at different scales, characteristic of fractals

The Sierpinski tetrahedron pattern emerges because Nim losing positions correspond to positions where the XOR of pile sizes equals 0. This mathematical property creates a fractal structure that is both beautiful and mathematically significant.

## Tips

- Start with smaller max_values (like 5 or 10) to understand the basic patterns
- Use larger max_values (like 50 or 100) to see the full Sierpinski tetrahedron fractal
- The visualization is interactive - use your mouse to explore different views
- Hover over points to see their exact values and XOR calculations
- Zoom out to see the larger fractal structure
- Rotate the plot to view the tetrahedral symmetry from different angles
- Observe how the pattern repeats at different scales, a key characteristic of fractals

## License

MIT License
