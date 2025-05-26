"""
Nim Game Data Generator

This script generates data points for Nim game analysis and saves them to a CSV file.
"""

import csv
import argparse
import sys

def generate_nim_data(max_value):
    """
    Generate unique 3-tuple combinations for Nim game analysis.
    
    Args:
        max_value (int): Maximum number of stones in any pile
        
    Returns:
        list: List of tuples containing the data points
    """
    data_points = []
    
    # Generate all combinations of pile sizes
    for x in range(0, max_value + 1):
        for y in range(0, max_value + 1):
            for z in range(0, max_value + 1):
                # Only add if XOR of all numbers is 0 (Nim losing position)
                if x ^ y ^ z == 0:
                    data_points.append((x, y, z))
    
    return data_points

def save_to_csv(data_points, filename):
    """
    Save the data points to a CSV file.
    
    Args:
        data_points (list): List of tuples containing the data points
        filename (str): Name of the output CSV file
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['pile1', 'pile2', 'pile3'])
            # Write data points
            writer.writerows(data_points)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        sys.exit(1)

def main():
    """
    Main function to handle command line arguments and generate data.
    """
    parser = argparse.ArgumentParser(description='Generate Nim game data')

    parser.add_argument('--max_value', type=int, required=True,
                       help='Maximum number of stones in any pile')
    parser.add_argument('--output', type=str, default='nim_data.csv',
                       help='Output CSV filename')
    
    args = parser.parse_args()
    
    # Generate data
    print(f"Generating data with max value {args.max_value}")
    data_points = generate_nim_data(args.max_value)
    
    # Save to CSV
    save_to_csv(data_points, args.output)
    
    print(f"\nGenerated {len(data_points)} losing positions")
    print("\nLosing positions (XOR=0):")
    for point in data_points:
        print(f"{point} (XOR: {point[0]} ^ {point[1]} ^ {point[2]} = 0)")

if __name__ == "__main__":
    main()