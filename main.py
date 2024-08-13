import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import time

st.title('Streamlit 超入門')

st.write('progress bar')
'Start!!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration{i + 1}')
    bar.progress(i + 1)
    time.sleep(0.05)

'Done!!!!!!!!!!!!!!!!'


st.write('DataFrame')

df = pd.DataFrame({
    '1列目': [1, 2, 3, 4],
    '2列目': [10, 20, 30, 40],
})

st.dataframe(df.style.highlight_max(axis=0))
st.table(df.style.highlight_max(axis=0))


df = pd.DataFrame(
    np.random.rand(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

df = pd.DataFrame(
    np.random.rand(100, 2)/[50, 50] + [35.69, 139.70],
    columns=['lat', 'lon']
)

st.map(df)


# st.write('Display Image')

# if st.checkbox('Show Image'):
#     img = Image.open('./sample.jpg')
#     st.image(img, caption='Fantasy Disney', use_column_width=True)


# st.write('Interactive Widgets')

# option = st.selectbox(
#     '好きな数字を教えてください',
#     list(range(1, 11))
# )

# 'あなたの好きな数着は', option, 'です。'

# text = st.text_input('あなたの趣味を教えてください。')
# 'あなたの趣味：', text

# condition = st.slider('あなたの今の調子は？', 0, 10, 5)
# 'あなたのコンディション：', condition

# text = st.sidebar.text_input('あなたの趣味を教えてください。')
# condition = st.sidebar.slider('あなたの今の調子は？', 0, 10, 5)
# 'あなたの趣味：', text
# 'あなたのコンディション：', condition

# left_column, right_column = st.columns(2)
# button = left_column.button('右から無に文字を表示')
# if button:
#     right_column.write('ここは右から無です')

# expander = st.expander('問い合わせ1')
# expander.write('問い合わせ内容を書く1')
# expander.write('問い合わせ内容を書く2')
# expander = st.expander('問い合わせ2')
# expander.write('問い合わせ内容を書く1')
# expander.write('問い合わせ内容を書く2')
# expander = st.expander('問い合わせ3')
# expander.write('問い合わせ内容を書く1')
# expander.write('問い合わせ内容を書く2')
