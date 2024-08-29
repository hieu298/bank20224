import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go

file_path = 'asset/Bankdata.xlsx'
df = pd.ExcelFile(file_path)

# Lấy danh sách các mã
mã_list = df.sheet_names[1:] 
filtered_list = [item for item in mã_list if 'TIN' not in item and 'EVF' not in item]
big4 = ['BID','CTG','VCB']
NHdoanhnghiep = ['MBB','TCB','SHB','HDB','LPB','MSB','OCB','SSB']
NHcanhan=['ACB','VPB','STB','VIB','TPB']
NHnho=['NAB','PGB','ABB','VAB','EIB','SGB','KLB','BVB','BAB','NVB','VBB']
toannganh =['All']

all_banks = big4 + NHdoanhnghiep + NHcanhan + NHnho
bank_category = ['BIG 4','NGÂN HÀNG CHO VAY CÁ NHÂN','NGÂN HÀNG CHO VAY DOANH NGHIỆP','NGÂN HÀNG NHỎ','TOÀN NGÀNH',"ALL"]
pick1 = st.selectbox('Chọn danh mục:', bank_category)

# Xử lý chọn danh mục
def taolisst(pick1):
    if pick1 == 'BIG 4':
        pick2 = st.multiselect('Chọn mã:', big4,default=big4)
    elif pick1 == 'NGÂN HÀNG CHO VAY DOANH NGHIỆP':
        pick2 = st.multiselect('Chọn mã:', NHdoanhnghiep,default=NHdoanhnghiep)
    elif pick1 == 'NGÂN HÀNG CHO VAY CÁ NHÂN':
        pick2 = st.multiselect('Chọn mã:', NHcanhan,default=NHcanhan)
    elif pick1 == 'NGÂN HÀNG NHỎ':
        pick2 = st.multiselect('Chọn mã:', NHnho,default=NHnho)    
    elif pick1 == 'TOÀN NGÀNH':
        pick2 = st.multiselect('Chọn mã:', all_banks,default=all_banks)
    elif pick1 =='ALL':
        pick2 = st.multiselect('Chọn mã:', toannganh,default=toannganh)    
    return pick2

pick2 = taolisst(pick1)

# taodataframe so sanh
sheet_name = pd.ExcelFile(file_path).sheet_names[0]
df = pd.read_excel(file_path, sheet_name=sheet_name)
first_column = df.iloc[3:, 0].to_list()

item = st.selectbox('Chon tiêu chí:',first_column)

chỉ_tiêu_data = {}

for mã in pick2:
    df_sheet = pd.read_excel(file_path, sheet_name= mã)
    df_sheet= df_sheet.fillna(" ")
    df_sheet.columns = df_sheet.iloc[2]  # Đặt dòng thứ 3 làm tiêu đề
      # Xóa 3 dòng đầu tiên (bao gồm dòng tiêu đề cũ)
    
    # Tìm dòng chứa chỉ tiêu được chọn
    chỉ_tiêu_index = df_sheet[df_sheet.iloc[:, 0].str.contains(item, na=False)].index
    if len(chỉ_tiêu_index) > 0:
        chỉ_tiêu_values = df_sheet.iloc[chỉ_tiêu_index[0], 1:].dropna().values
        chỉ_tiêu_data[mã] = chỉ_tiêu_values
index_length = len(list(chỉ_tiêu_data.values())[0])
# Chuyển dữ liệu thành DataFrame để tiện so sánh
chỉ_tiêu_df = pd.DataFrame(chỉ_tiêu_data, index=df_sheet.columns[1:index_length+1])
chỉ_tiêu_df['All'] = chỉ_tiêu_df.sum(axis=1)
chỉ_tiêu_df = chỉ_tiêu_df.transpose()

st.write(chỉ_tiêu_df)

columnspick = st.multiselect('Chọn Quý:', chỉ_tiêu_df.columns, default=chỉ_tiêu_df.columns[0])

if columnspick:
    pickdf = chỉ_tiêu_df[columnspick]
    pickdf = pickdf.sort_values(by=columnspick[0])
    st.write(pickdf)

    fig = go.Figure()

    # Lặp qua từng cột trong pickdf và thêm vào biểu đồ
    for col in pickdf.columns:
        fig.add_trace(go.Bar(
            x=pickdf.index,
            y=pickdf[col],
            name=col,
            text=[f'{val:.2f}' for val in pickdf[col]],  # Hiển thị giá trị trên cột
            textposition='outside',
        ))

    # Cập nhật layout của biểu đồ
    fig.update_layout(
        title=f'So sánh các giá trị của từng mã',
        xaxis_title='Mã ',
        yaxis_title='Giá trị',
        xaxis=dict(autorange='reversed'),
        height=600,
    )

    st.write(fig)
else:
    st.write("Hãy chọn ít nhất một Quý để hiển thị dữ liệu.")
