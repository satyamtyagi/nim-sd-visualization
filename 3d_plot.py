import plotly.graph_objects as go
import pandas as pd
import argparse
import sys
import plotly.io as pio

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create a 3D scatter plot of Nim losing positions')
    parser.add_argument('filename', type=str, help='Path to the CSV file containing pile sizes')
    parser.add_argument('--output', type=str, default='nim_plot.html',
                       help='Output HTML filename (default: nim_plot.html)')
    parser.add_argument('--show', action='store_true',
                       help='Show the plot in browser (default: False)')
    args = parser.parse_args()

    try:
        # Read data from CSV file
        df = pd.read_csv(args.filename)
        # Use first three columns directly
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        z = df.iloc[:, 2]
        
        # Create simple hover text
        hover_text = [f'X: {a}<br>Y: {b}<br>Z: {c}' 
                      for a, b, c in zip(x, y, z)]
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

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=5,
            color='red',          # Changed to red for better visibility
            opacity=0.8,
            line=dict(
                width=2,
                color='black'
            )
        ),
        text=hover_text,           # Add hover text
        hovertemplate=
        '<b>Point</b><br>' +
        'X: %{x}<br>' +
        'Y: %{y}<br>' +
        'Z: %{z}<br>' +
        '<extra></extra>'
    )])

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
