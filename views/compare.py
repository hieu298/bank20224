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
chỉ_tiêu_df['Average'] = chỉ_tiêu_df.mean(axis=1)
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

##################################
 


import streamlit as st
import pandas as pd

# Đọc file Excel
file_path = "asset/MergedWorkbook.xlsx"
excel_data = pd.ExcelFile(file_path)

# Lấy tên của các sheet trong file Excel (các mã chứng khoán)
sheet_names = excel_data.sheet_names
# Tạo một selectbox trong Streamlit để chọn mã chứng khoán
df = pd.read_excel(file_path,sheet_name='ACB' )

# Lấy dữ liệu từ dòng thứ 8 trở đi
df.columns=df.iloc[6]
df = df.iloc[7:].reset_index(drop=True)

item1 = df.iloc[0:,0].to_list()
pick1 = st.selectbox('Chọn chỉ tiêu:',item1)


chỉ_tiêu_data1 = {}

for mã in pick2:
    df1= pd.read_excel(file_path,sheet_name=mã )
    df1.columns=df1.iloc[6]
    df1 = df1.iloc[7:].reset_index(drop=True)

    
    chỉ_tiêu_index1 = df[df.iloc[:, 0].str.strip() == pick1].index
    if len(chỉ_tiêu_index1) > 0:
        chỉ_tiêu_values1 = df1.iloc[chỉ_tiêu_index1[0], 1:].dropna().values
        chỉ_tiêu_data1[mã] = chỉ_tiêu_values1

index_length1 = len(list(chỉ_tiêu_data1.values())[0])
# Chuyển dữ liệu thành DataFrame để tiện so sánh
chỉ_tiêu_df1 = pd.DataFrame(chỉ_tiêu_data1, index=df1.columns[1:index_length+1])
chỉ_tiêu_df1 = chỉ_tiêu_df1.transpose()

st.write(chỉ_tiêu_df1)

columnspick1 = st.multiselect('Chọn Quý:', chỉ_tiêu_df1.columns, default=chỉ_tiêu_df1.columns[-1])

if columnspick1:
    pickdf1 = chỉ_tiêu_df1[columnspick1]
    pickdf1 = pickdf1.sort_values(by=columnspick1[0])
    st.write(pickdf1)

    fig1 = go.Figure()

    # Lặp qua từng cột trong pickdf và thêm vào biểu đồ
    for col in pickdf1.columns:
        fig1.add_trace(go.Bar(
            x=pickdf1.index,
            y=pickdf1[col],
            name=col,
            text=[f'{val:.3f}' for val in pickdf1[col]],  # Hiển thị giá trị trên cột
            textposition='outside',
        ))

    # Cập nhật layout của biểu đồ
    fig1.update_layout(
        title=f'So sánh các giá trị của từng mã',
        xaxis_title='Mã ',
        yaxis_title='Giá trị',
        height=600,
    )

    st.write(fig1)
else:
    st.write("Hãy chọn ít nhất một Quý để hiển thị dữ liệu.")

def taodf(pick2, file_path, pick1):
    chỉ_tiêu_data1 = {}

    for mã in pick2:
        df1 = pd.read_excel(file_path, sheet_name=mã)
        df1.columns = df1.iloc[6]  # Đặt tên cột từ dòng thứ 6
        df1 = df1.iloc[7:].reset_index(drop=True)  # Bỏ 7 dòng đầu

        # Tìm dòng có giá trị trùng với pick1
        chỉ_tiêu_index1 = df1[df1.iloc[:, 0].str.strip() == pick1].index
        if len(chỉ_tiêu_index1) > 0:
            chỉ_tiêu_values1 = df1.iloc[chỉ_tiêu_index1[0], 1:].dropna().values
            chỉ_tiêu_data1[mã] = chỉ_tiêu_values1
        else:
            # Trường hợp không tìm thấy chỉ tiêu, thêm giá trị None hoặc xử lý khác
            chỉ_tiêu_data1[mã] = [None] * (len(df1.columns) - 1)

    if chỉ_tiêu_data1:
        index_length1 = len(list(chỉ_tiêu_data1.values())[0])
        chỉ_tiêu_df1 = pd.DataFrame(chỉ_tiêu_data1, index=df1.columns[1:index_length1+1])
        chỉ_tiêu_df1['Average'] = chỉ_tiêu_df1.mean(axis=1)
        return chỉ_tiêu_df1
    else:
        return None

# Gọi hàm taodf để lấy các DataFrame
a = taodf(big4, file_path, pick1)
b = taodf(NHdoanhnghiep, file_path, pick1)
c = taodf(NHcanhan, file_path, pick1)
d = taodf(NHnho, file_path, pick1)
e = taodf(all_banks,file_path, pick1)
# Chỉ lấy cột 'Average'
if a is not None and b is not None and c is not None and d is not None and e is not None:
    a = a['Average']
    b = b['Average']
    c = c['Average']
    d = d['Average']
    e = e['Average']


    # Gộp các DataFrame lại
    merged_df = pd.concat([a, b, c, d, e], axis=1)

    # Đặt tên cho các cột trong DataFrame hợp nhất
    merged_df.columns = ['Big4', 'NH Doanh Nghiệp', 'NH Cá Nhân', 'NH Nhỏ','Toàn Ngành']

    # Hiển thị DataFrame hợp nhất
    st.write(merged_df)

    # Vẽ biểu đồ
    traces = []
    for column in merged_df.columns:
        trace = go.Scatter(
            x=merged_df.index,  # Trục x là index của DataFrame (thường là các chỉ số hoặc thời gian)
            y=merged_df[column],  # Trục y là giá trị của cột tương ứng
            text=merged_df[column],  # Hiển thị giá trị trên các marker
            textposition='top center',  # Vị trí hiển thị số
            marker=dict(size=8),  # Tên của đường, là tên cột
        )
        traces.append(trace)

    # Tạo layout cho biểu đồ
    layout = go.Layout(
        title='Biểu đồ {} của Các Nhóm Ngân Hàng'.format(pick1),
        xaxis=dict(title='Thời gian'),
        yaxis=dict(title='Giá trị'),
    )

    # Tạo figure với các trace
    fig = go.Figure(data=traces, layout=layout)

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig)
else:
    st.write("Không có dữ liệu để hiển thị.")


