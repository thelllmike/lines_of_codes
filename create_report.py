import pandas as pd
import re

# File path for the input CSV
input_file_path = "input.csv"

# Read the input file with appropriate error handling and no specific delimiter
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Lists to store parsed data
assignees = []
projects = []
lines_of_code = []
current_project = None

# Iterate through each line to extract relevant data
for line in lines:
    # Debug print for each line
    print("Processing line:", line.strip())
    
    # Check for project lines (repository paths)
    if "Processing repository:" in line:
        current_project = line.split("/")[-1].strip()
        print("Current Project Detected:", current_project)
    
    # Check for assignee lines with added lines information
    if "added lines:" in line:
        parts = line.split(",")
        if len(parts) >= 3:
            assignee = parts[0].strip()
            lines_added_part = parts[1].split("added lines:")[-1].strip()
            lines_added = lines_added_part if lines_added_part.isdigit() else '0'
            
            print("Match Found - Assignee:", assignee, "Lines Added:", lines_added)
            
            # Ensure the current project is not None
            if current_project:
                assignees.append(assignee)
                projects.append(current_project)
                lines_of_code.append(int(lines_added))

# Create a DataFrame with the parsed data
output_df = pd.DataFrame({
    "Assinee": assignees,
    "Project": projects,
    "Lines of Code": lines_of_code
})

# Export the DataFrame to an Excel file
output_file_path = "detected_output.xlsx"
output_df.to_excel(output_file_path, index=False)

print(f"Detected data saved to: {output_file_path}")
