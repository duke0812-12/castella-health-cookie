
import streamlit as st

st.set_page_config(page_title="健康長崎蛋糕脆餅 AI 模擬器 v5", layout="centered")

st.title("🥚 健康長崎蛋糕脆餅 AI 模擬器 v5")
st.markdown("根據你輸入的原始配方與健康目標，自動分析與推薦優化配方、營養標示與說明（含雙欄式標示）。")

st.subheader("🔧 步驟一：輸入原始配方（比例總和為100）")
with st.expander("範例預設配方："):
    st.markdown("""
- 雞蛋 30%
- 砂糖 40%
- 低筋麵粉 25%
- 麥芽漿 4%
- 水 1%
    """)

default_ingredients = {
    "雞蛋": 30,
    "砂糖": 40,
    "低筋麵粉": 25,
    "麥芽漿": 4,
    "水": 1
}
input_ingredients = {}
total = 0
for name, default in default_ingredients.items():
    input_ingredients[name] = st.number_input(f"{name} (%)", min_value=0.0, max_value=100.0, value=float(default), step=0.1)
    total += input_ingredients[name]

if total != 100:
    st.error(f"目前總和為 {total}%，請確認總和為100%")
    st.stop()

st.subheader("🎯 步驟二：選擇健康優化目標")
goals = st.multiselect(
    "選擇欲強化的健康目標（可複選）",
    options=["減糖", "補蛋白", "補維礦"],
    default=["減糖", "補維礦"]
)
goal_low_sugar = "減糖" in goals
goal_protein = "補蛋白" in goals
goal_vitamins = "補維礦" in goals

st.subheader("⚖️ 步驟三：設定每片餅乾重量")
weight_per_piece = st.number_input("每片重量（g）", value=8.2, min_value=1.0, max_value=100.0)

run_simulation = st.button("🚀 執行模擬")

if run_simulation:
    optimized = dict(input_ingredients)
    output_lines = []
    adjustments = []

    if goal_low_sugar and "砂糖" in optimized:
        reduced = optimized["砂糖"] * 0.5
        optimized["赤藻糖醇"] = reduced
        optimized["砂糖"] = reduced
        adjustments.append("將砂糖減量50%，以赤藻糖醇替代，降低升糖指數與總糖量")

    if goal_protein:
        optimized["濃縮蛋白粉"] = 5
        if "低筋麵粉" in optimized:
            optimized["低筋麵粉"] = max(0, optimized["低筋麵粉"] - 5)
        adjustments.append("添加濃縮蛋白粉 5%，提升蛋白質含量，部分取代低筋麵粉")

    if goal_vitamins:
        optimized["維礦複合粉"] = 2
        if "低筋麵粉" in optimized:
            optimized["低筋麵粉"] = max(0, optimized["低筋麵粉"] - 2)
        adjustments.append("補充 26 種維生素與礦物質，建議每日攝取餅乾約30g 以達補充效果")

    # 模擬營養值 (以每8.2g為基礎)
    base_nutrition = {
        'calories': 35.4,
        'protein': 0.7,
        'fat': 0.7,
        'sugar': 4.1,
        'carbs': 6.5,
        'sodium': 7
    }

    factor_piece = weight_per_piece / 8.2
    factor_100g = 100 / 8.2

    sim_piece = {k: round(v * (0.9 if goal_low_sugar and k in ["calories", "sugar"] else 1.0) *
                          (1.5 if goal_protein and k == "protein" else 1.0) *
                          (factor_piece if k != "sodium" else 1)  # sodium 特別處理
                          , 2) for k, v in base_nutrition.items()}

    sim_100g = {k: round(v * (0.9 if goal_low_sugar and k in ["calories", "sugar"] else 1.0) *
                        (1.5 if goal_protein and k == "protein" else 1.0) *
                        (factor_100g if k != "sodium" else 1)
                        , 2) for k, v in base_nutrition.items()}

    if goal_vitamins:
        sim_piece["sodium"] = round(24 * factor_piece)
        sim_100g["sodium"] = round(24 * factor_100g)

    st.subheader("📄 模擬結果")

    output_lines.append("【優化後建議配方】")
    for k, v in optimized.items():
        output_lines.append(f"- {k}：{round(v, 2)}%")
    st.text("\n".join(output_lines))

    st.subheader("📊 雙欄式預估營養標示")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**每片 {weight_per_piece}g**")
        for k, v in sim_piece.items():
            unit = 'kcal' if k == 'calories' else 'g' if k != 'sodium' else 'mg'
            st.markdown(f"- {k.title()}: {v} {unit}")

    with col2:
        st.markdown("**每 100g**")
        for k, v in sim_100g.items():
            unit = 'kcal' if k == 'calories' else 'g' if k != 'sodium' else 'mg'
            st.markdown(f"- {k.title()}: {v} {unit}")

    st.subheader("🧠 AI 配方建議摘要")
    if adjustments:
        for a in adjustments:
            st.markdown(f"- {a}")
    else:
        st.markdown("- 未啟用健康優化選項，配方保持原樣")
