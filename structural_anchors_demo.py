import pandas as pd



# Implementation of SpreadsheetLLM compression techniques

# 1. Structural Anchors for Efficient Layout Understanding
# This technique identifies heterogeneous rows/columns (structural anchors) and removes
# distant homogeneous areas that don't contribute to understanding spreadsheet layout
def extract_structural_skeleton(df: pd.DataFrame, k: int = 1):
    """
    Extract structural skeleton by identifying structural anchors (boundary rows/columns)
    and keeping only k rows/columns around them, removing distant homogeneous regions.
    
    This implementation compares rows WITH EACH OTHER to identify structural changes,
    not the diversity within individual rows.
    """
    
    def rows_are_similar(row1_idx, row2_idx, similarity_threshold=0.8):
        """Check if two rows are structurally similar"""
        row1 = df.iloc[row1_idx].fillna('').astype(str)
        row2 = df.iloc[row2_idx].fillna('').astype(str)
        
        # Count how many positions have the same content
        matches = sum(1 for a, b in zip(row1, row2) if a == b)
        similarity = matches / len(row1)
        return similarity >= similarity_threshold
    
    def cols_are_similar(col1_idx, col2_idx, similarity_threshold=0.8):
        """Check if two columns are structurally similar"""
        col1 = df.iloc[:, col1_idx].fillna('').astype(str)
        col2 = df.iloc[:, col2_idx].fillna('').astype(str)
        
        # Count how many positions have the same content
        matches = sum(1 for a, b in zip(col1, col2) if a == b)
        similarity = matches / len(col1)
        return similarity >= similarity_threshold
    
    # Find structural anchor rows (rows where structure changes)
    row_anchors = set()
    for i in range(df.shape[0]):
        is_boundary = False
        
        # Check if this row is different from adjacent rows (structural boundary)
        if i == 0 or i == df.shape[0] - 1:
            is_boundary = True  # First and last rows are always anchors
        else:
            # Check if current row is significantly different from neighbors
            prev_similar = rows_are_similar(i-1, i)
            next_similar = rows_are_similar(i, i+1) if i+1 < df.shape[0] else False
            
            if not prev_similar and not next_similar:
                is_boundary = True
        
        if is_boundary:
            row_anchors.add(i)
    
    # Find structural anchor columns (columns where structure changes)  
    col_anchors = set()
    for j in range(df.shape[1]):
        is_boundary = False
        
        # Check if this column is different from adjacent columns (structural boundary)
        if j == 0 or j == df.shape[1] - 1:
            is_boundary = True  # First and last columns are always anchors
        else:
            # Check if current column is significantly different from neighbors
            prev_similar = cols_are_similar(j-1, j)
            next_similar = cols_are_similar(j, j+1) if j+1 < df.shape[1] else False
            
            if not prev_similar or not next_similar:
                is_boundary = True
        
        if is_boundary:
            col_anchors.add(j)
    
    # Expand anchors by k (keep k rows/columns around each structural anchor)
    rows_to_keep = set()
    for r in row_anchors:
        rows_to_keep.update(range(max(0, r - k), min(df.shape[0], r + k + 1)))
    
    cols_to_keep = set()
    for c in col_anchors:
        cols_to_keep.update(range(max(0, c - k), min(df.shape[1], c + k + 1)))
    
    # Extract skeleton
    return df.iloc[sorted(rows_to_keep), sorted(cols_to_keep)]


# Sample DataFrame demonstrating structural boundaries
# This shows clear transitions between different table structures
data = {
    # Table 1: Sales Report (rows 0-3) - Distinct structure
    'A': ['Sales Report', 'Product', 'Laptop', 'Phone', 
          # Homogeneous region (rows 4-11) - Repeated similar rows
          'Notes', 'Notes', 'Notes', 'Notes', 'Notes', 'Notes', 'Notes', 'Notes',
          # Table 2: Employee Data (rows 12-15) - Different structure  
          'Employee List', 'Name', 'John Smith', 'Jane Doe',
          # Another homogeneous region (rows 16-23) - Different repeated pattern
          'Summary', 'Summary', 'Summary', 'Summary', 'Summary', 'Summary', 'Summary', 'Summary',
          # Table 3: Financial Data (rows 24-27) - Third distinct structure
          'Q4 Finances', 'Revenue', '$10000', '$15000'],
    
    'B': ['Q4 2024', 'Units', '150', '200',
          # Homogeneous region - Same pattern as column A
          'Details', 'Details', 'Details', 'Details', 'Details', 'Details', 'Details', 'Details',
          # Employee table - Different pattern
          'Department', 'Engineering', 'Engineering', 'Marketing',
          # Homogeneous region - Different repeated pattern  
          'Info', 'Info', 'Info', 'Info', 'Info', 'Info', 'Info', 'Info',
          # Financial table - Third pattern
          'Target', 'Actual', '$12000', '$14000'],
    
    'C': ['Region', 'Price', '$1200', '$800',
          # Homogeneous region - Similar to A and B pattern
          'Extra', 'Extra', 'Extra', 'Extra', 'Extra', 'Extra', 'Extra', 'Extra',
          # Employee table - Matches employee pattern
          'Location', 'Seattle', 'Seattle', 'New York', 
          # Homogeneous region - Matches summary pattern
          'More', 'More', 'More', 'More', 'More', 'More', 'More', 'More',
          # Financial - Matches financial pattern
          'Status', 'Goal Met', 'Yes', 'Yes'],
    
    'D': ['North', 'Count', '5', '8',
          # Homogeneous region - Similar repeated pattern
          'Misc', 'Misc', 'Misc', 'Misc', 'Misc', 'Misc', 'Misc', 'Misc',
          # Employee table - Matches employee pattern
          'Building', 'A', 'A', 'B',
          # Homogeneous region - Matches summary pattern
          'End', 'End', 'End', 'End', 'End', 'End', 'End', 'End',
          # Financial - Matches financial pattern
          'Quarter', 'Q4', 'Complete', 'Complete'],
}
df = pd.DataFrame(data)

print(f"Original DataFrame shape: {df.shape}")
print("\nCORRECTED IMPLEMENTATION:")
print("Instead of looking at diversity WITHIN each row, we now compare rows WITH EACH OTHER")
print("to identify structural boundaries where table structure changes.")
print("\nThis spreadsheet contains multiple tables separated by homogeneous regions:")
print("- Rows 0-3: Sales table (different structure)")
print("- Rows 4-11: Homogeneous region (repeated 'Notes/Details/Extra/Misc' pattern)")  
print("- Rows 12-15: Employee table (different structure)")
print("- Rows 16-23: Homogeneous region (repeated 'Summary/Info/More/End' pattern)")
print("- Rows 24-27: Financial table (different structure)")
print("\nThe algorithm will identify where structure changes and keep 'k' rows around each boundary.")
print()

skeleton = extract_structural_skeleton(df, k=1)

# Display results with compression metrics
print("Original DataFrame:")
print(df)
print(f"\nStructural Anchor Extraction Results:")
print(f"  Original shape: {df.shape} ({df.shape[0] * df.shape[1]} cells)")
print(f"  Skeleton shape: {skeleton.shape} ({skeleton.shape[0] * skeleton.shape[1]} cells)")
compression_ratio = (df.shape[0] * df.shape[1]) / (skeleton.shape[0] * skeleton.shape[1])
print(f"  Compression ratio: {compression_ratio:.2f}x")
print(f"  Space saved: {((df.shape[0] * df.shape[1] - skeleton.shape[0] * skeleton.shape[1]) / (df.shape[0] * df.shape[1]) * 100):.1f}%")
print(f"\nThe algorithm preserved table boundaries and structural anchors while removing")
print(f"distant homogeneous regions that don't contribute to layout understanding.")
print("\nExtracted Structural Skeleton:")
print(skeleton)

print("\n" + "="*60)
print("PARAMETER 'k' DEMONSTRATION")
print("="*60)
print("The parameter 'k' controls how many rows to keep around each structural anchor.")
print("Lower k = more aggressive compression, Higher k = preserve more context")

for k_val in [0, 1, 2]:
    test_skeleton = extract_structural_skeleton(df, k=k_val)
    compression = (df.shape[0] * df.shape[1]) / (test_skeleton.shape[0] * test_skeleton.shape[1])
    space_saved = ((df.shape[0] * df.shape[1] - test_skeleton.shape[0] * test_skeleton.shape[1]) / (df.shape[0] * df.shape[1]) * 100)
    print(f"k={k_val}: {df.shape} -> {test_skeleton.shape}, compression: {compression:.2f}x, space saved: {space_saved:.1f}%")