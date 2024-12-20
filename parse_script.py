import pandas as pd
import re

# Define input and output file paths
input_file_path = "parsed_lines_of_code.csv"
output_file_path = "formatted_lines_of_code.csv"

# Read the input file as plain text
with open(input_file_path, 'r') as file:
    lines = file.readlines()

data = []
current_project = None

for line in lines:
    # Detect project lines
    project_match = re.search(r"Processing repository: (\/\S+)", line)
    if project_match:
        current_project = project_match.group(1).split('/')[-1]
        print(f"Found project: {current_project}")  # Debug: print detected project

    # Detect assignee and lines of code
    assignee_match = re.search(r"(\S+@\S+)", line)
    if assignee_match:
        assignee = assignee_match.group(1)
        added_match = re.search(r"added lines:\s*(\d+)", line)
        removed_match = re.search(r"removed lines:\s*(\d+)", line)
        total_match = re.search(r"total lines:\s*(-?\d+)", line)

        if added_match and removed_match and total_match:
            lines_of_code = int(total_match.group(1))
            print(f"Assignee: {assignee}, Project: {current_project}, Lines of Code: {lines_of_code}")  # Debug
            data.append({"Assignee": assignee, "Project": current_project, "Lines of Code": lines_of_code})

# Convert the extracted data to a DataFrame
df = pd.DataFrame(data)
print("Extracted DataFrame:")
print(df)  # Debug: print the DataFrame before saving

# Save the DataFrame to a new CSV file
if not df.empty:
    df.to_csv(output_file_path, index=False)
    print(f"Formatted data saved to {output_file_path}")
else:
    print("No data found to save. Please check the input file.")
