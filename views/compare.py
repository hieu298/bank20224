import pandas as pd
import plotly.graph_objects as go
import streamlit as st
# Đọc file Excel và lấy tên các sheet
file_path = "C:\python\multipage\asset\Bankdata.xlsx"
xls = pd.ExcelFile(file_path)


# Lấy danh sách các mã
mã_list = xls.sheet_names[1:] 
filtered_list = [item for item in mã_list if 'TIN' not in item and 'EVF' not in item]

# Danh sách các chỉ tiêu

# Tạo giao diện người dùng trong Streamlit
selected_mã = st.multiselect('Chọn mã:', filtered_list, default=["VPB"])
if filtered_list in selected_mã:
    selected_mã = mã_list  # Nếu "Chọn tất cả" được chọn, chọn hết các mã


sheet_name = pd.ExcelFile(file_path).sheet_names[0]
df = pd.read_excel(file_path, sheet_name=sheet_name)
first_column = df.iloc[3:, 0].to_list()  # Đảm bảo rằng tên cột là 'A'. Nếu không, thay thế bằng tên cột đ
chỉ_tiêu_list = st.selectbox('Chọn chỉ tiêu:',first_column)

# Tạo một dictionary để lưu dữ liệu của chỉ tiêu được chọn
chỉ_tiêu_data = {}

for mã in selected_mã:
    df_sheet = pd.read_excel(file_path, sheet_name= mã)
    df_sheet= df_sheet.fillna(" ")
    df_sheet.columns = df_sheet.iloc[2]  # Đặt dòng thứ 3 làm tiêu đề
      # Xóa 3 dòng đầu tiên (bao gồm dòng tiêu đề cũ)
    
    # Tìm dòng chứa chỉ tiêu được chọn
    chỉ_tiêu_index = df_sheet[df_sheet.iloc[:, 0].str.contains(chỉ_tiêu_list, na=False)].index
    if len(chỉ_tiêu_index) > 0:
        chỉ_tiêu_values = df_sheet.iloc[chỉ_tiêu_index[0], 1:].dropna().values
        chỉ_tiêu_data[mã] = chỉ_tiêu_values

index_length = len(list(chỉ_tiêu_data.values())[0])
# Chuyển dữ liệu thành DataFrame để tiện so sánh
chỉ_tiêu_df = pd.DataFrame(chỉ_tiêu_data, index=df_sheet.columns[1:index_length+1])
chỉ_tiêu_df = chỉ_tiêu_df.transpose()
columnspick = st.multiselect('Chọn Quý:', chỉ_tiêu_df.columns,default=chỉ_tiêu_df.columns[0])
pickdf=chỉ_tiêu_df[columnspick]
pickdf= pickdf[columnspick].sort_values(by=columnspick[0])
st.write(pickdf)


# Vẽ biểu đồ so sánh chỉ tiêu được chọn của từng mã
fig = go.Figure()

for col in pickdf.columns:
    fig.add_trace(go.Bar(
        x=pickdf.index,
        y=pickdf[col],
        name=col,
         text=[f'{val:.2f}' for val in pickdf[col]],  # Hiển thị tên mã trên cột
        textposition='outside',))

# Cập nhật layout của biểu đồ
fig.update_layout(
    title=f'So sánh {chỉ_tiêu_list} của từng mã',
    xaxis_title='Mã ',
    yaxis_title=f'{chỉ_tiêu_list} ',
    xaxis=dict(autorange='reversed')
)
st.write(fig)
