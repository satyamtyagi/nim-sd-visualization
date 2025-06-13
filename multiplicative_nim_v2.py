"""
Multiplicative Nim Analysis v2

Enhanced version of Multiplicative Nim analysis with improved performance and features.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Set
from itertools import combinations_with_replacement
import argparse
import sys
from math import comb

class MultiplicativeNim:
    def __init__(self, max_value: int, prime: int):
        """
        Initialize Multiplicative Nim analysis.
        
        Args:
            max_value: Maximum value for each element (1 to max_value)
            prime: Prime number for filtering
        """
        if max_value <= 0 or prime <= 0:
            raise ValueError("max_value and prime must be positive integers")
            
        self.max_value = max_value
        self.prime = prime
        self.valid_numbers = [i for i in range(1, max_value + 1) if i % prime != 0]
        
    def count_positions(self, n: int) -> int:
        """
        Calculate the total number of positions of length n.
        
        Args:
            n: Length of each combination
            
        Returns:
            Total number of positions
        """
        return comb(len(self.valid_numbers) + n - 1, n)
        
    def generate_positions(self, n: int, allow_duplicates: bool = False) -> List[Tuple[int, ...]]:
        """
        Generate positions of length n with valid numbers.
        
        Args:
            n: Number of elements in each position
            allow_duplicates: If True, generate all combinations (including duplicates)
                           If False, generate combinations with repetition (unique sorted combinations)
            
        Returns:
            List of positions
        """
        if allow_duplicates:
            # Generate all combinations (including duplicates)
            positions = []
            for x in self.valid_numbers:
                for y in self.valid_numbers:
                    for z in self.valid_numbers:
                        positions.append((x, y, z))
            return positions
        else:
            # Generate combinations with repetition (unique sorted combinations)
            return list(combinations_with_replacement(self.valid_numbers, n))
        
    def filter_positions(self, positions: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
        """
        Filter positions to remove:
        1. Positions where all elements are less than prime
        2. Positions containing multiples of prime
        
        Args:
            positions: List of tuples to filter
            
        Returns:
            List of filtered positions
        """
        filtered = []
        for pos in positions:
            # Check if all elements are less than prime
            if all(x < self.prime for x in pos):
                continue
                
            # Check if any element is a multiple of prime
            if any(x % self.prime == 0 for x in pos):
                continue
                
            filtered.append(pos)
        return filtered
        
    def find_losing_positions(self, positions: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
        """
        Find positions where the product of elements is congruent to 1 modulo prime.
        
        Args:
            positions: List of tuples to analyze
            
        Returns:
            List of losing positions (where product % prime == 1)
        """
        return [pos for pos in positions if np.prod(pos) % self.prime == 1]
        
def main():
    parser = argparse.ArgumentParser(description='Multiplicative Nim Analysis v2')
    parser.add_argument('max_value', type=int, help='Maximum value for each element')
    parser.add_argument('prime', type=int, help='Prime number for filtering')
    parser.add_argument('count', type=int, help='Number of elements in each position')
    parser.add_argument('--output', type=str, help='Output CSV filename')
    parser.add_argument('--duplicates', action='store_true',
                       help='Generate all combinations including duplicates (default: False)')
    
    args = parser.parse_args()
    
    # Initialize the game
    game = MultiplicativeNim(args.max_value, args.prime)
    
    # Generate positions
    print(f"Generating positions for n={args.count}")
    positions = game.generate_positions(args.count, args.duplicates)
    print(f"Total positions generated: {len(positions)}")
    
    # Filter positions
    filtered = game.filter_positions(positions)
    print(f"Filtered positions: {len(filtered)}")
    
    # Find losing positions
    losing = game.find_losing_positions(filtered)
    print(f"Losing positions: {len(losing)}")
    
    # Export results if output file is specified
    if args.output:
        df = pd.DataFrame(losing)
        df.to_csv(args.output, index=False, header=False)
        print(f"Results exported to {args.output}")

if __name__ == "__main__":
    main()
