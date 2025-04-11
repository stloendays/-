import streamlit as st
from PIL import Image, ImageEnhance
import os
import pandas as pd
from pathlib import Path

# ✅ 页面配置
st.set_page_config(page_title="Whale兼职平台", page_icon="🐋", layout="wide")

# ✅ 样式美化（CSS 注入）
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">

<style>
body {
    background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
    font-family: 'Helvetica Neue', sans-serif;
    color: #111;
}

/* 标题样式 */
h1, h2, h3 {
    color: #000;
}

/* 玻璃拟态容器 */
.transparent-box {
    background: rgba(255, 255, 255, 0.45);
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease-in-out;
}
.transparent-box:hover {
    background: rgba(255, 255, 255, 0.65);
    box-shadow: 0 12px 42px rgba(0, 0, 0, 0.2);
}

/* 按钮优化 */
.stButton > button {
    background-color: #000000;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    transition: transform 0.2s ease, box-shadow 0.3s;
}
.stButton > button:hover {
    background-color: #333;
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* 输入框 */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
    background-color: rgba(255,255,255,0.7);
    color: #111;
    border-radius: 6px;
    padding: 8px;
}

/* 页脚 */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ✅ 横幅与标题
st.image("assets/banner.jpg","assets/微信图片_20230917224137.jpg", width=400)
st.title("🐋 Whale兼职")
st.markdown("### *让时间自由游动 · Where It Is Here*")
st.markdown("---")

# ✅ 数据加载
data_path = Path("data/jobs.csv")
data_path.parent.mkdir(parents=True, exist_ok=True)
if data_path.exists():
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame(columns=["职位名称", "公司", "薪资", "地点", "详情"])

# ✅ 页面导航
page = st.sidebar.selectbox("导航", ["首页", "查看岗位", "上传简历", "图片美化", "联系我们"])

# ✅ 首页
if page == "首页":
    st.header("🎯 欢迎来到 Whale兼职平台")
    st.markdown("""
    - 🌟 一个极简且互动的兼职发布平台
    - 💼 支持浏览岗位、上传简历、图像处理等功能
    """)

# ✅ 查看岗位
elif page == "查看岗位":
    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="transparent-box">', unsafe_allow_html=True)
        st.subheader("🔍 搜索兼职")
        search = st.text_input("请输入关键词")
        filtered_df = df.copy()
        if search:
            filtered_df = df[df["职位名称"].str.contains(search, case=False)]

        st.subheader("📋 当前兼职列表")
        if filtered_df.empty:
            st.info("没有匹配的岗位，请尝试其他关键词。")
        else:
            for _, row in filtered_df.iterrows():
                with st.expander(f"{row['职位名称']} - {row['公司']}"):
                    st.write(f"📍 地点：{row['地点']}  💰 薪资：{row['薪资']}")
                    st.write(f"📝 {row['详情']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="transparent-box">', unsafe_allow_html=True)
        st.subheader("📢 发布兼职岗位")
        with st.form("post_job"):
            name = st.text_input("职位名称")
            company = st.text_input("公司")
            salary = st.text_input("薪资")
            location = st.text_input("地点")
            desc = st.text_area("详情")
            submitted = st.form_submit_button("发布兼职")
            if submitted:
                if not name or not company:
                    st.warning("请填写完整信息。")
                else:
                    new_row = pd.DataFrame([[name, company, salary, location, desc]],
                                           columns=["职位名称", "公司", "薪资", "地点", "详情"])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(data_path, index=False)
                    st.success("🎉 成功发布兼职！")
        st.markdown('</div>', unsafe_allow_html=True)

# ✅ 上传简历
elif page == "上传简历":
    st.markdown('<div class="transparent-box">', unsafe_allow_html=True)
    st.header("📤 上传你的简历")
    uploaded_resume = st.file_uploader("请选择简历文件（PDF/Word）", type=["pdf", "docx"])
    if uploaded_resume:
        save_path = os.path.join("uploaded_resumes", uploaded_resume.name)
        os.makedirs("uploaded_resumes", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())
        st.success(f"✅ 简历上传成功：{uploaded_resume.name}")
    st.markdown('</div>', unsafe_allow_html=True)

# ✅ 图片美化
elif page == "图片美化":
    st.markdown('<div class="transparent-box">', unsafe_allow_html=True)
    st.header("🎨 上传并美化你的图片")
    uploaded_img = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
    if uploaded_img:
        image = Image.open(uploaded_img)
        st.image(image, caption="原图", use_column_width=True)

        brightness = st.slider("亮度", 0.5, 2.0, 1.0)
        enhancer = ImageEnhance.Brightness(image)
        image_bright = enhancer.enhance(brightness)

        contrast = st.slider("对比度", 0.5, 2.0, 1.0)
        enhancer = ImageEnhance.Contrast(image_bright)
        image_final = enhancer.enhance(contrast)

        st.image(image_final, caption="美化后图像", use_column_width=True)

        if st.button("保存美化图像"):
            os.makedirs("output", exist_ok=True)
            image_final.save("output/enhanced_image.png")
            st.success("🌟 图像已保存至 output/enhanced_image.png")
    st.markdown('</div>', unsafe_allow_html=True)

# ✅ 联系我们
elif page == "联系我们":
    st.markdown('<div class="transparent-box">', unsafe_allow_html=True)
    st.header("📬 留言板")
    name = st.text_input("你的名字")
    email = st.text_input("邮箱")
    message = st.text_area("留言内容")
    if st.button("提交"):
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"姓名: {name}, 邮箱: {email}, 留言: {message}\n")
        st.success("✅ 留言已提交，谢谢反馈！")
    st.markdown('</div>', unsafe_allow_html=True)

# ✅ 页脚
st.markdown("""
---
<div style='text-align:center; font-size:14px; color:gray;'>
    Whale兼职平台 © 2025 · Designed by Tony 🐋<br>
    <i class="bi bi-envelope"></i> 联系邮箱：hnyjt7@nottinghham.edu.cn
</div>
""", unsafe_allow_html=True)
