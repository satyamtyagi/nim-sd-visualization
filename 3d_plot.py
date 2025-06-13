import plotly.graph_objects as go
import pandas as pd
import argparse
import sys
import plotly.io as pio

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create a 3D scatter plot of Nim losing positions')
    parser.add_argument('filename1', type=str, help='Path to the first CSV file containing pile sizes')
    parser.add_argument('filename2', type=str, help='Path to the second CSV file containing pile sizes')
    parser.add_argument('filename3', type=str, help='Path to the third CSV file containing pile sizes')
    parser.add_argument('--output', type=str, default='nim_plot.html',
                       help='Output HTML filename (default: nim_plot.html)')
    parser.add_argument('--show', action='store_true',
                       help='Show the plot in browser (default: False)')
    args = parser.parse_args()

    try:
        # Read data from all three CSV files
        df1 = pd.read_csv(args.filename1)
        df2 = pd.read_csv(args.filename2)
        df3 = pd.read_csv(args.filename3)
        
        # Convert to tuples for easy comparison
        positions1 = list(zip(df1.iloc[:, 0], df1.iloc[:, 1], df1.iloc[:, 2]))
        positions2 = list(zip(df2.iloc[:, 0], df2.iloc[:, 1], df2.iloc[:, 2]))
        positions3 = list(zip(df3.iloc[:, 0], df3.iloc[:, 1], df3.iloc[:, 2]))
        
        # Find overlapping positions
        overlap12 = set(positions1) & set(positions2)
        overlap13 = set(positions1) & set(positions3)
        overlap23 = set(positions2) & set(positions3)
        overlap_all = overlap12 & set(positions3)
        
        # Create separate lists for each type of position
        unique1 = [pos for pos in positions1 if pos not in overlap12 and pos not in overlap13]
        unique2 = [pos for pos in positions2 if pos not in overlap12 and pos not in overlap23]
        unique3 = [pos for pos in positions3 if pos not in overlap13 and pos not in overlap23]
        overlap12_only = [pos for pos in overlap12 if pos not in overlap_all]
        overlap13_only = [pos for pos in overlap13 if pos not in overlap_all]
        overlap23_only = [pos for pos in overlap23 if pos not in overlap_all]
        
        # Convert back to separate x, y, z coordinates
        x1, y1, z1 = zip(*unique1)
        x2, y2, z2 = zip(*unique2)
        x3, y3, z3 = zip(*unique3)
        x12, y12, z12 = zip(*overlap12_only)
        x13, y13, z13 = zip(*overlap13_only)
        x23, y23, z23 = zip(*overlap23_only)
        xa, ya, za = zip(*overlap_all)
        
        # Create hover text
        hover_text1 = [f'File 1: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x1, y1, z1)]
        hover_text2 = [f'File 2: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x2, y2, z2)]
        hover_text3 = [f'File 3: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x3, y3, z3)]
        hover_text12 = [f'Overlap 1-2: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x12, y12, z12)]
        hover_text13 = [f'Overlap 1-3: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x13, y13, z13)]
        hover_text23 = [f'Overlap 2-3: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(x23, y23, z23)]
        hover_text_all = [f'Overlap All: X: {a}<br>Y: {b}<br>Z: {c}' for a, b, c in zip(xa, ya, za)]
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found!")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{args.filename}' is empty!")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: Could not parse '{args.filename}' as CSV!")
        sys.exit(1)
    except IndexError:
        print(f"Error: CSV file must have at least 3 columns!")
        sys.exit(1)

    # Create the 3D scatter plot with seven different traces
    fig = go.Figure()
    
    # Add file 1 points
    fig.add_trace(go.Scatter3d(
        x=x1,
        y=y1,
        z=z1,
        mode='markers',
        marker=dict(
            size=5,
            color='blue',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text1,
        name='File 1',
        hovertemplate=
        '<b>Point</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add file 2 points
    fig.add_trace(go.Scatter3d(
        x=x2,
        y=y2,
        z=z2,
        mode='markers',
        marker=dict(
            size=5,
            color='green',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text2,
        name='File 2',
        hovertemplate=
        '<b>Point</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add file 3 points
    fig.add_trace(go.Scatter3d(
        x=x3,
        y=y3,
        z=z3,
        mode='markers',
        marker=dict(
            size=5,
            color='red',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text3,
        name='File 3',
        hovertemplate=
        '<b>Point</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add overlap 1-2 points
    fig.add_trace(go.Scatter3d(
        x=x12,
        y=y12,
        z=z12,
        mode='markers',
        marker=dict(
            size=6,
            color='purple',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text12,
        name='Overlap 1-2',
        hovertemplate=
        '<b>Overlap Point 1-2</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add overlap 1-3 points
    fig.add_trace(go.Scatter3d(
        x=x13,
        y=y13,
        z=z13,
        mode='markers',
        marker=dict(
            size=6,
            color='orange',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text13,
        name='Overlap 1-3',
        hovertemplate=
        '<b>Overlap Point 1-3</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add overlap 2-3 points
    fig.add_trace(go.Scatter3d(
        x=x23,
        y=y23,
        z=z23,
        mode='markers',
        marker=dict(
            size=6,
            color='cyan',
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text23,
        name='Overlap 2-3',
        hovertemplate=
        '<b>Overlap Point 2-3</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Add overlap all points
    fig.add_trace(go.Scatter3d(
        x=xa,
        y=ya,
        z=za,
        mode='markers',
        marker=dict(
            size=7,
            color='magenta',
            opacity=1.0,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text_all,
        name='Overlap All',
        hovertemplate=
        '<b>Overlap Point All</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Create buttons for toggling visibility
    buttons = [
        dict(
            label="Show All",
            method="update",
            args=[{"visible": [True, True, True, True, True, True, True]}]
        ),
        dict(
            label="Show File 1",
            method="update",
            args=[{"visible": [True, False, False, False, False, False, False]}]
        ),
        dict(
            label="Show File 2",
            method="update",
            args=[{"visible": [False, True, False, False, False, False, False]}]
        ),
        dict(
            label="Show File 3",
            method="update",
            args=[{"visible": [False, False, True, False, False, False, False]}]
        ),
        dict(
            label="Show Overlap 1-2",
            method="update",
            args=[{"visible": [False, False, False, True, False, False, False]}]
        ),
        dict(
            label="Show Overlap 1-3",
            method="update",
            args=[{"visible": [False, False, False, False, True, False, False]}]
        ),
        dict(
            label="Show Overlap 2-3",
            method="update",
            args=[{"visible": [False, False, False, False, False, True, False]}]
        ),
        dict(
            label="Show Overlap All",
            method="update",
            args=[{"visible": [False, False, False, False, False, False, True]}]
        ),
        dict(
            label="Show Files 1+2",
            method="update",
            args=[{"visible": [True, True, False, True, False, False, False]}]
        ),
        dict(
            label="Show Files 1+3",
            method="update",
            args=[{"visible": [True, False, True, False, True, False, False]}]
        ),
        dict(
            label="Show Files 2+3",
            method="update",
            args=[{"visible": [False, True, True, False, False, True, False]}]
        )
    ]
    
    # Update layout with buttons
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                center=dict(x=0, y=0, z=0)
            )
        ),
        title='Nim Game Positions Comparison',
        title_x=0.5,
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=True,
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                buttons=buttons
            )
        ]
    )

    # Update layout
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                center=dict(x=0, y=0, z=0)
            )
        ),
        title='Nim Game Positions',
        title_x=0.5,
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=True
    )

    # Add grid lines
    fig.update_scenes(
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        zaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )

    # Save the plot as HTML
    fig.write_html(args.output)
    print(f"Plot saved to {args.output}")

    # Save a static PNG image
    image_filename = args.output.replace('.html', '.png')
    pio.write_image(fig, image_filename, scale=2)
    print(f"Static image saved to {image_filename}")

    # Show the plot if requested
    if args.show:
        fig.show()

if __name__ == '__main__':
    main()
