import pandas as pd
import re
from collections import defaultdict

def create_rule_based_recognizer():
    """
    Create rule-based recognizer for predefined data types:
    Year, Integer, Float, Percentage, Scientific notation, Date, Time, Currency, Email
    """
    
    def recognize_data_type(value):
        """Recognize data type based on cell value using rules"""
        if pd.isna(value) or str(value).strip() == '':
            return 'Empty'
        
        value_str = str(value).strip()
        
        # Year (4-digit number between reasonable range)
        if re.match(r'^(19|20|21)\d{2}$', value_str):
            return 'Year'
        
        # Email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value_str):
            return 'Email'
        
        # Percentage (ends with %)
        if re.match(r'^-?\d+\.?\d*%$', value_str):
            return 'Percentage'
        
        # Currency (starts with currency symbol)
        if re.match(r'^[\$£€¥₹]\s*-?\d{1,3}(,\d{3})*(\.\d{2})?$', value_str):
            return 'Currency'
        
        # Scientific notation
        if re.match(r'^-?\d+\.?\d*[eE][+-]?\d+$', value_str):
            return 'ScientificNotation'
        
        # Date (various formats)
        date_patterns = [
            r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$',  # YYYY-MM-DD or YYYY/MM/DD
            r'^\d{1,2}[-/]\d{1,2}[-/]\d{4}$',  # MM-DD-YYYY or MM/DD/YYYY
            r'^\d{1,2}[-/]\d{1,2}[-/]\d{2}$',  # MM-DD-YY or MM/DD/YY
        ]
        for pattern in date_patterns:
            if re.match(pattern, value_str):
                return 'Date'
        
        # Time (HH:MM or HH:MM:SS)
        if re.match(r'^\d{1,2}:\d{2}(:\d{2})?(\s*(AM|PM))?$', value_str, re.IGNORECASE):
            return 'Time'
        
        # Float (decimal number)
        if re.match(r'^-?\d+\.\d+$', value_str):
            return 'Float'
        
        # Integer (whole number)
        if re.match(r'^-?\d+$', value_str):
            return 'Integer'
        
        # Others (everything else)
        return 'Others'
    
    return recognize_data_type

def aggregate_by_data_format(df):
    """
    Aggregate cells by data format using rule-based recognition
    For well-defined formats, group by type. For text, preserve individual values.
    """
    recognizer = create_rule_based_recognizer()
    
    # Analyze each cell using rule-based recognition
    rule_groups = defaultdict(list)
    
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            value = df.iat[i, j]
            cell_addr = f"{df.columns[j]}{i+1}"
            
            # Rule-based data type recognition
            data_type = recognizer(value)
            
            # For well-defined formats, group by type
            if data_type in ['Year', 'Integer', 'Float', 'Percentage', 'ScientificNotation', 
                           'Date', 'Time', 'Currency', 'Email', 'Empty']:
                rule_groups[data_type].append({
                    'address': cell_addr,
                    'value': value,
                    'type': data_type
                })
            else:
                # For text content (Others), preserve individual values
                # Group by the actual text value to maintain structure
                text_key = f'"{str(value)}"'
                rule_groups[text_key].append({
                    'address': cell_addr,
                    'value': value,
                    'type': 'Text'
                })
    
    return rule_groups

def create_sample_dataframe():
    """Create a sample DataFrame with various data types for demonstration"""
    
    # Sample data with different data types
    data = {
        'Category': ['Date', 'Date', 'Time', 'Time', 'Currency', 'Currency', 
                    'Percentage', 'Percentage', 'Integer', 'Integer', 'Float', 
                    'Float', 'Scientific', 'Year', 'Email', 'Phone', 'Text'],
        'Value': ['2024-01-15', '01/15/2024', '14:30:00', '2:30 PM', '$1,234.56', 
                 '£9,876.54', '75%', '12.5%', '42', '1000', '3.14159', '2.718', 
                 '6.022e23', '2024', 'user@example.com', '+1-555-123-4567', 'Hello World'],
        'Description': ['ISO Date Format', 'US Date Format', '24-hour Time', 
                       '12-hour Time', 'US Dollar', 'British Pound', 'Percentage', 
                       'Percentage (decimal)', 'Whole Number', 'Thousand', 
                       'Pi (5 decimals)', 'e (3 decimals)', 'Avogadro Number', 
                       'Year Format', 'Email Address', 'Phone Number', 'Text String']
    }
    
    return pd.DataFrame(data)

# =============================================================================
# DEMONSTRATION: Data Format Aggregation for Numerical Cells
# =============================================================================

print("=" * 80)
print("DATA FORMAT AGGREGATION DEMONSTRATION")  
print("=" * 80)

print("\nTechnique Description:")
print("Instead of encoding exact numerical values, this method:")
print("- Groups cells by their data format/type (dates, currencies, percentages, etc.)")
print("- Uses rule-based recognition for 9 predefined types:")
print("  Year, Integer, Float, Percentage, Scientific notation, Date, Time, Currency, Email, Others")
print("- Preserves semantic meaning while reducing token usage")

# Create sample DataFrame with various data types
print("\n" + "-" * 60)
print("CREATING SAMPLE DATAFRAME WITH VARIOUS DATA TYPES")
print("-" * 60)

df = create_sample_dataframe()
print(f"DataFrame shape: {df.shape}")
print("\nSample data:")
print(df)

print("\n" + "-" * 60)
print("TRADITIONAL ENCODING (Every Value Individually)")
print("-" * 60)

# Count original tokens (each cell encoded separately)
total_cells = 0
non_empty_cells = 0
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        total_cells += 1
        if pd.notna(df.iat[i, j]) and str(df.iat[i, j]).strip():
            non_empty_cells += 1
            cell_addr = f"{df.columns[j]}{i+1}"
            print(f"  {cell_addr}: '{df.iat[i, j]}'")

print(f"\nTraditional encoding tokens: {non_empty_cells}")

print("\n" + "-" * 60)
print("DATA FORMAT AGGREGATION ANALYSIS")
print("-" * 60)

# Perform aggregation analysis
rule_groups = aggregate_by_data_format(df)

print("RULE-BASED DATA TYPE AGGREGATION:")
print("(Using predefined recognition patterns + individual text preservation)")
for data_type, cells in sorted(rule_groups.items()):
    if data_type != 'Empty' and cells:
        addresses = [cell['address'] for cell in cells]
        
        # For well-defined data types, show type and sample values
        if data_type in ['Year', 'Integer', 'Float', 'Percentage', 'ScientificNotation', 
                        'Date', 'Time', 'Currency', 'Email']:
            sample_values = [str(cell['value']) for cell in cells[:3]]  # Show first 3 values
            sample_text = ', '.join(sample_values)
            if len(cells) > 3:
                sample_text += '...'
            print(f"   Type '{data_type}': {','.join(addresses)} (values: {sample_text})")
        else:
            # For individual text values, show the text and its addresses
            text_value = data_type  # data_type is the quoted text value
            print(f"   {text_value}: {','.join(addresses)}")

# Calculate compression
# Count aggregated groups (format types + individual text values)
aggregated_groups = len([group for group in rule_groups.values() if group and group[0]['type'] != 'Empty'])

compression_ratio = non_empty_cells / aggregated_groups if aggregated_groups > 0 else 1
space_saved = ((non_empty_cells - aggregated_groups) / non_empty_cells * 100) if non_empty_cells > 0 else 0

print(f"\nCOMPRESSION RESULTS:")
print(f"   Original tokens: {non_empty_cells}")
print(f"   Aggregated groups: {aggregated_groups}")
print(f"   Compression ratio: {compression_ratio:.2f}x")
print(f"   Space saved: {space_saved:.1f}%")

print("\n" + "-" * 60)
print("KEY BENEFITS DEMONSTRATED:")
print("-" * 60)
print("1. SEMANTIC PRESERVATION:")
print("   - Values '2024-01-15' and '01/15/2024' both recognized as 'Date'")  
print("   - Different currencies ($1234.56, £9876.54) grouped as 'Currency'")
print("   - Various percentages (75%, 12.5%) unified as 'Percentage'")

print("\n2. INTELLIGENT TYPE RECOGNITION:")
print("   - Rule-based recognizer covers 9 common data types")
print("   - Patterns detect semantic meaning (dates, currencies, emails, etc.)")
print("   - Individual text values preserved to maintain structure")

print("\n3. STRUCTURE UNDERSTANDING:")
print("   - Preserves data type semantics for numerical/formatted data")
print("   - Individual text values maintain spreadsheet structure and headers")
print("   - Enables LLMs to understand both data patterns and content organization")

print("\n4. TOKEN EFFICIENCY:")
print("   - Dramatic reduction in tokens while preserving meaning")
print("   - Groups cells by semantic type rather than exact content")
print("   - Significant compression with minimal information loss")

print("\n" + "=" * 80)
print("This technique enables LLMs to understand spreadsheet data types and")
print("structure without being overwhelmed by exact numerical values.")
print("=" * 80) 