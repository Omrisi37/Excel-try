# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

def main():
    st.title("Lab Experiment Data Collection")

    # Initialize session state to store data
    if 'all_data' not in st.session_state:
        st.session_state.all_data = {}

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
                    df = pd.read_excel(uploaded_file)
                return df
            except Exception as e:
                st.error(f"Error reading {section_title}: {e}")
                return None
        return None

    # 1. Procedure - Settings
    st.subheader("1. Procedure - Settings")
    uploaded_settings = st.file_uploader("Upload Procedure Settings (Excel/CSV)", type=["xlsx", "xls", "csv"])

    # 2. Procedure - Physical Treatments
    st.subheader("2. Procedure - Physical Treatments")
    uploaded_physical = st.file_uploader("Upload Physical Treatments (Excel/CSV)", type=["xlsx", "xls", "csv"])

    # 3. Black box ? + Procedure - Enz Hydro
    st.subheader("3. Black box ? + Procedure - Enz Hydro")
    uploaded_hydro = st.file_uploader("Upload Enz Hydro (Excel/CSV)", type=["xlsx", "xls", "csv"])

    # 4. Procedure - Enz Cross
    st.subheader("4. Procedure - Enz Cross")
    uploaded_cross = st.file_uploader("Upload Enz Cross (Excel/CSV)", type=["xlsx", "xls", "csv"])

    # Collect data
    if st.button("Save Data"):
        # Read settings
        if uploaded_settings is not None:
            try:
                settings_df = pd.read_excel(uploaded_settings)
                st.session_state.all_data['Procedure - Settings'] = settings_df.to_dict('records')
            except Exception as e:
                st.error(f"Error reading Settings data: {e}")
        else:
            st.session_state.all_data['Procedure - Settings'] = {}

        # Read physical data
        if uploaded_physical is not None:
            try:
                physical_df = pd.read_excel(uploaded_physical)
                st.session_state.all_data['Procedure - Physical Treatments'] = physical_df.to_dict('records')
            except Exception as e:
                st.error(f"Error reading Physical data: {e}")
        else:
            st.session_state.all_data['Procedure - Physical Treatments'] = {}

        # Read hydro data
        if uploaded_hydro is not None:
            try:
                hydro_df = pd.read_excel(uploaded_hydro)
                st.session_state.all_data['Black box ? + Procedure - Enz Hydro'] = hydro_df.to_dict('records')
            except Exception as e:
                st.error(f"Error reading Hydro data: {e}")
        else:
            st.session_state.all_data['Black box ? + Procedure - Enz Hydro'] = {}

        # Read cross data
        if uploaded_cross is not None:
            try:
                cross_df = pd.read_excel(uploaded_cross)
                st.session_state.all_data['Procedure - Enz Cross'] = cross_df.to_dict('records')
            except Exception as e:
                st.error(f"Error reading Cross data: {e}")
        else:
            st.session_state.all_data['Procedure - Enz Cross'] = {}

        st.success("Data saved!")

    # Create Combined Excel File and Download
    st.subheader("Create Combined Excel File and Download")
    if st.button("Create and Download Excel File"):
        if st.session_state.all_data:
            try:
                # Read all the data and combine to one long row
                df = pd.DataFrame([data for section, rows in st.session_state.all_data.items() for data in rows])

                # Create an in-memory buffer
                excel_buffer = io.BytesIO()

                # Use Pandas Excel writer and save to buffer
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Combined Data', index=False)

                excel_buffer.seek(0)  # Reset buffer to the beginning

                # Download Button
                st.download_button(
                    label="Download Combined Excel File",
                    data=excel_buffer,
                    file_name="combined_lab_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
        else:
            st.warning("No data saved yet.")

if __name__ == "__main__":
    main()
