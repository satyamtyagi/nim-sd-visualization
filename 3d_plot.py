import plotly.graph_objects as go
import pandas as pd
import argparse
import sys

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create a 3D scatter plot of Nim losing positions')
    parser.add_argument('filename', type=str, help='Path to the CSV file containing pile sizes')
    args = parser.parse_args()

    try:
        # Read data from CSV file
        df = pd.read_csv(args.filename)
        # Use column names
        x = df['pile1']
        y = df['pile2']
        z = df['pile3']
        
        # Calculate XOR values for hover text
        xor_values = x ^ y ^ z
        hover_text = [f'Pile1: {a}<br>Pile2: {b}<br>Pile3: {c}<br>XOR: {xor}' 
                      for a, b, c, xor in zip(x, y, z, xor_values)]
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found!")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{args.filename}' is empty!")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: Could not parse '{args.filename}' as CSV!")
        sys.exit(1)
    except KeyError:
        print(f"Error: CSV file must have columns 'pile1', 'pile2', and 'pile3'!")
        sys.exit(1)

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.7,
            colorscale='Viridis',   # Add color gradient
            color=xor_values,       # Color by XOR value
            showscale=True,         # Show color scale legend
            colorbar=dict(
                title='XOR Value'
            )
        ),
        text=hover_text,           # Add hover text
        hovertemplate=
        '<b>Losing Position</b><br>' +
        'Pile1: %{x}<br>' +
        'Pile2: %{y}<br>' +
        'Pile3: %{z}<br>' +
        'XOR: %{marker.color}<br>' +
        '<extra></extra>'
    )])

    # Update layout
    fig.update_layout(
        scene=dict(
            xaxis_title='Pile 1 Size',
            yaxis_title='Pile 2 Size',
            zaxis_title='Pile 3 Size',
            aspectmode='cube',
            xaxis=dict(
                range=[0, df['pile1'].max() + 1],
                tickvals=list(range(0, df['pile1'].max() + 1, 5))
            ),
            yaxis=dict(
                range=[0, df['pile2'].max() + 1],
                tickvals=list(range(0, df['pile2'].max() + 1, 5))
            ),
            zaxis=dict(
                range=[0, df['pile3'].max() + 1],
                tickvals=list(range(0, df['pile3'].max() + 1, 5))
            )
        ),
        title='Nim Game Losing Positions (XOR = 0)',
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

    # Show the plot
    fig.show()

if __name__ == '__main__':
    main()
