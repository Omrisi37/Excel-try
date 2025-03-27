# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

def main():
    st.title("Lab Experiment Data Collection")

    # Function to upload and process files
    def upload_file(section_name, section_title):
        st.subheader(section_title)
        uploaded_file = st.file_uploader(f"Upload {section_title} (Excel/CSV)", type=["xlsx", "xls", "csv"])
        if uploaded_file:
            try:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                if file_extension == 'csv':
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')  # Specify the engine here
                return df
            except Exception as e:
                st.error(f"Error reading {section_title}: {e}")
                return None
        return None

    # 1. Procedure - Settings
    settings_df = upload_file("Settings", "Procedure - Settings")

    # 2. Procedure - Physical Treatments
    physical_treatments_df = upload_file("Physical Treatments", "Procedure - Physical Treatments")

    # 3. Black box ? + Procedure - Enz Hydro
    enz_hydro_df = upload_file("Enz Hydro", "Black box ? + Procedure - Enz Hydro")

    # 4. Procedure - Enz Cross
    enz_cross_df = upload_file("Enz Cross", "Procedure - Enz Cross")

    # Merge and Download Button
    st.subheader("Merge and Download")
    if st.button("Create Combined Excel File"):
        dfs = {
            "Procedure Settings": settings_df,
            "Physical Treatments": physical_treatments_df,
            "Enz Hydro": enz_hydro_df,
            "Enz Cross": enz_cross_df
        }

        # Remove None dataframes
        valid_dfs = {k: df for k, df in dfs.items() if df is not None}

        if valid_dfs:
            try:
                # Combine all data into a single row
                combined_data = {}
                for name, df in valid_dfs.items():
                    # Ensure each column name is unique
                    df.columns = [f"{name} - {col}" for col in df.columns]
                    combined_data.update(df.iloc[0].to_dict())  # Use the first row of each DataFrame

                # Convert combined data to a DataFrame
                combined_df = pd.DataFrame([combined_data])

                # Create an in-memory buffer
                excel_buffer = io.BytesIO()

                # Use Pandas Excel writer and save to buffer
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    combined_df.to_excel(writer, sheet_name='Combined Data', index=False)

                excel_buffer.seek(0)  # Reset buffer to the beginning

                # Download Button
                st.download_button(
                    label="Download Combined Excel File",
                    data=excel_buffer,
                    file_name="combined_lab_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("Excel file created, download will start automatically.")

            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
        else:
            st.warning("Please upload at least one file to merge.")

if __name__ == "__main__":
    main()
