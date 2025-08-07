import streamlit as st
import streamlit.components.v1 as components
import random
import streamlit as st


st.set_page_config(page_title="可编辑脑图", layout="wide")

# 打开文件
p = open("test.html", encoding="utf-8")

# 使用 100% 宽度来让内容适应容器宽度
# components.html(p.read(), height=1000, width=2000)
# st.container
st.html("./test.html")

choose = st.sidebar.selectbox("是否要进行截图保存", ("是", "否"))
