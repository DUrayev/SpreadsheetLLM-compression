import pandas as pd
from collections import defaultdict
import itertools

def create_cell_address(row, col, df):
    """Convert row, col indices to Excel-style address like 'A1', 'B2', etc."""
    return f'{df.columns[col]}{row + 1}'

def merge_cell_ranges(addresses):
    """
    Merge consecutive cell addresses into ranges like A1:A4, B5:B7, etc.
    This implements the range merging.
    """
    if not addresses:
        return ""
    
    # Parse addresses into (column, row) tuples
    parsed = []
    for addr in addresses:
        col = addr[0]  # Assume single letter column for simplicity
        row = int(addr[1:])
        parsed.append((col, row, addr))
    
    # Sort by column then row
    parsed.sort()
    
    ranges = []
    current_range_start = None
    current_range_end = None
    current_col = None
    
    for col, row, addr in parsed:
        if current_col != col:
            # New column, finish previous range
            if current_range_start:
                if current_range_start == current_range_end:
                    ranges.append(current_range_start)
                else:
                    ranges.append(f"{current_range_start}:{current_range_end}")
            
            # Start new range
            current_col = col
            current_range_start = addr
            current_range_end = addr
        else:
            # Same column, check if consecutive
            prev_row = int(current_range_end[1:])
            if row == prev_row + 1:
                # Consecutive, extend range
                current_range_end = addr
            else:
                # Not consecutive, finish current range and start new one
                if current_range_start == current_range_end:
                    ranges.append(current_range_start)
                else:
                    ranges.append(f"{current_range_start}:{current_range_end}")
                current_range_start = addr
                current_range_end = addr
    
    # Finish last range
    if current_range_start:
        if current_range_start == current_range_end:
            ranges.append(current_range_start)
        else:
            ranges.append(f"{current_range_start}:{current_range_end}")
    
    return ','.join(ranges)

def invert_index_with_ranges(df: pd.DataFrame):
    """
    Create inverted index with proper range merging.
    Maps values to cell address ranges (e.g., "$100": "A1:A4", "$150": "B5,B7")
    """
    index = defaultdict(list)
    
    # Build value-to-addresses mapping
    for r, c in itertools.product(range(df.shape[0]), range(df.shape[1])):
        val = df.iat[r, c]
        if pd.notna(val) and str(val).strip() != '':
            addr = create_cell_address(r, c, df)
            index[str(val)].append(addr)
    
    # Merge addresses into ranges
    result = {}
    for val, addrs in index.items():
        result[val] = merge_cell_ranges(addrs)
    
    return result

# =============================================================================
# DEMONSTRATION: Inverted Index Translation for Token Efficiency
# =============================================================================

print("=" * 80)
print("INVERTED INDEX TRANSLATION DEMONSTRATION")
print("=" * 80)

print("\nTechnique Description:")
print("Instead of traditional row-by-row serialization, this method creates a")
print("value-to-address dictionary that:")
print("- Maps identical cell values to their address ranges")
print("- Eliminates redundant encoding of repeated values") 
print("- Merges consecutive addresses into ranges (e.g., A1:A4)")
print("- Skips empty cells entirely")

# Create a realistic spreadsheet with repeated values that demonstrates the technique
print("\n" + "-" * 60)
print("EXAMPLE: Financial Report with Repeated Values")
print("-" * 60)

# Create sample data with intentional repetitions to show the benefit
data = {
    'A': ['Quarter', 'Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', '', 'Total', '$500K', '$500K'],
    'B': ['Product', 'Laptop', 'Laptop', 'Desktop', 'Laptop', 'Desktop', 'Desktop', '', 'Revenue', '$300K', '$200K'], 
    'C': ['Revenue', '$100K', '$150K', '$100K', '$200K', '$100K', '$150K', '', 'Target', 'Met', 'Met'],
    'D': ['Status', 'Active', 'Active', 'Pending', 'Active', 'Pending', 'Active', '', 'Goal', 'Yes', 'Yes'],
    'E': ['Region', 'North', 'North', 'South', 'North', 'South', 'South', '', '', '', '']
}

df = pd.DataFrame(data)

print("ORIGINAL SPREADSHEET:")
print("Shape:", df.shape, f"({df.shape[0] * df.shape[1]} cells)")
print()
# Add row numbers for reference
df_display = df.copy()
df_display.index = [f'Row {i+1}' for i in range(len(df))]
print(df_display)

print("\n" + "-" * 60)
print("TRADITIONAL ENCODING (Row-by-Row):")
print("-" * 60)
print("This would encode every cell individually:")
token_count = 0
for r in range(df.shape[0]):
    for c in range(df.shape[1]):
        val = df.iat[r, c]
        addr = create_cell_address(r, c, df)
        if pd.notna(val) and str(val).strip():
            print(f"  {addr}: '{val}'")
            token_count += 1
        elif str(val).strip() == '':
            print(f"  {addr}: ''")  # Empty cells still need to be encoded
            token_count += 1

print(f"\nTraditional method tokens: {token_count}")

print("\n" + "-" * 60)
print("INVERTED INDEX TRANSLATION:")
print("-" * 60)

# Apply inverted index
inverted = invert_index_with_ranges(df)

print("Value-to-Address Range Mapping:")
print("(Empty cells excluded, ranges merged where possible)")
print()

# Sort by value for better readability
for val in sorted(inverted.keys()):
    ranges = inverted[val]
    print(f"  '{val}': {ranges}")

print(f"\nInverted index entries: {len(inverted)}")
print(f"Token reduction: {token_count} -> {len(inverted)} ({(token_count - len(inverted))/token_count*100:.1f}% reduction)")

print("\n" + "-" * 60)
print("KEY BENEFITS DEMONSTRATED:")
print("-" * 60)
print("1. REDUNDANCY ELIMINATION:")
print("   - 'Q1' appears 3 times -> mapped once to 'A2:A4'")
print("   - '$100K' appears 3 times -> mapped once to 'C2,C4,C6'") 
print("   - 'Active' appears 4 times -> mapped to ranges")

print("\n2. RANGE MERGING:")
print("   - Consecutive cells with same value become ranges")
print("   - 'Q1' in A2,A3,A4 becomes 'A2:A4'")
print("   - Non-consecutive cells stay separate: 'C2,C4,C6'")

print("\n3. EMPTY CELL ELIMINATION:")
print("   - Empty cells in column E and row 8 are completely skipped")
print("   - No wasted tokens on encoding empty positions")

print("\n4. LOSSLESS COMPRESSION:")
print("   - All non-empty data is preserved")
print("   - Exact cell positions are maintained")
print("   - Can be perfectly reconstructed")

print("\n" + "=" * 80)
print("This technique significantly reduces token usage while preserving")
print("all structural and content information needed for LLM processing.")
print("=" * 80) 