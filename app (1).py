
import streamlit as st

# 匯入模擬函式
from healthy_castella_cookie_simulator_v1_clean import simulate_healthy_castella_cookie

st.set_page_config(page_title="健康長崎蛋糕脆餅模擬器", layout="centered")

st.title("🥚 健康長崎蛋糕脆餅模擬器")
st.markdown("本模擬器以經典長崎蛋糕脆餅配方為基礎，優化為低糖、營養強化版本，包含 26 種維生素與礦物質。")

st.subheader("📦 模擬結果")
st.caption("預設每片重量為 8.2g")

# 執行模擬
result = simulate_healthy_castella_cookie()
st.text(result)

st.divider()
st.markdown("👨‍🍳 由 AI 營養配方模型驅動 · 金格食品研發測試用")
