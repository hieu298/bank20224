import pandas as pd
import plotly.graph_objects as go
import streamlit as st



#///////////////////////////////////////////
from openpyxl import load_workbook
file_path = 'asset/Bankdata.xlsx'
workbook = load_workbook(file_path)
sheet = workbook["Summary"]
st.write(f"Giá trị hiện tại của ô A2: {sheet['A2'].value}")
# Nhận giá trị mới từ người dùng
new_value = st.text_input("Nhập dữ liệu mới cho ô A2:")

# Khi người dùng nhập dữ liệu mới và nhấn Enter
if new_value:
    # Cập nhật giá trị mới vào ô A2
    sheet["A2"].value = new_value
    
    # Lưu lại file Excel
    workbook.save(file_path)
    
    st.write("Dữ liệu đã được cập nhật!")

# Đóng workbook
workbook.close()