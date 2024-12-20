from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV file into a DataFrame with delimiter and error handling
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents), sep=",", on_bad_lines='skip')

        # Strip whitespace and standardize column names
        df.columns = df.columns.str.strip().str.lower()
        
        # Check if the required columns exist
        required_columns = {'assignee', 'project', 'lines of code'}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="CSV does not contain the required columns: Assignee, Project, Lines of Code")

        # Processing: Group data by Assignee and Project, and sum the Lines of Code
        result = df.groupby(['assignee', 'project'], as_index=False)['lines of code'].sum()

        # Create an Excel file in memory
        output = BytesIO()
        result.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        # Return the Excel file as a response
        headers = {
            'Content-Disposition': 'attachment; filename="processed_report.xlsx"'
        }
        return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
