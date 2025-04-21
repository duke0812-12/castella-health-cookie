
import streamlit as st

st.set_page_config(page_title="健康長崎蛋糕脆餅 AI 模擬器", layout="centered")

st.title("🥚 健康長崎蛋糕脆餅 AI 模擬器 v2")
st.markdown("輸入你的原始配方與目標需求，系統將以 AI 模擬方式提供優化建議配方與預估營養標示。")

st.subheader("🔧 步驟一：輸入原始配方（比例總和為100）")
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
    input_ingredients[name] = st.number_input(f"{name} (%)", min_value=0.0, max_value=100.0, value=float(default))
    total += input_ingredients[name]

if total != 100:
    st.error(f"目前總和為 {total}%，請確認總和為100%")
    st.stop()

st.subheader("🎯 步驟二：選擇模擬目標")
goal_low_sugar = st.checkbox("減糖（赤藻糖醇替代50%砂糖）", value=True)
goal_protein = st.checkbox("補充蛋白質（添加濃縮蛋白粉）", value=True)
goal_vitamins = st.checkbox("補充26種維生素與礦物質", value=True)

st.subheader("⚙️ 步驟三：設定每片餅乾重量")
weight_per_piece = st.number_input("每片重量（g）", value=8.2, min_value=1.0, max_value=100.0)

# AI 模擬建議邏輯（簡化規則基礎上）
optimized = dict(input_ingredients)
output_lines = []

if goal_low_sugar and "砂糖" in optimized:
    reduced = optimized["砂糖"] * 0.5
    optimized["赤藻糖醇"] = reduced
    optimized["砂糖"] = reduced

if goal_protein:
    optimized["濃縮蛋白粉"] = 5
    optimized["低筋麵粉"] -= 5

if goal_vitamins:
    optimized["維礦複合粉"] = 2
    optimized["低筋麵粉"] -= 2

# 修正低筋麵粉不為負
if optimized["低筋麵粉"] < 0:
    optimized["低筋麵粉"] = 0

# 計算營養預估值（簡化估算）
base_nutrition = {
    'calories': 35.4,
    'protein': 0.7,
    'fat': 0.7,
    'sugar': 4.1,
    'carbs': 6.5,
    'sodium': 7
}
sim_nutrition = {
    'calories': round(base_nutrition['calories'] * 0.9, 1),
    'protein': round(base_nutrition['protein'] * 1.4, 2) if goal_protein else base_nutrition['protein'],
    'fat': 0.6,
    'sugar': round(base_nutrition['sugar'] * 0.5, 2) if goal_low_sugar else base_nutrition['sugar'],
    'carbs': 5.1,
    'sodium': 24 if goal_vitamins else base_nutrition['sodium']
}

st.subheader("📄 模擬結果輸出")

output_lines.append("【優化後建議配方】")
for k, v in optimized.items():
    output_lines.append(f"- {k}：{round(v, 2)}%")

output_lines.append("\n【營養補強說明】")
if goal_vitamins:
    output_lines.append("已添加每日所需 26 種維生素與礦物質，建議每日攝取量 30g（約3～4片）")
else:
    output_lines.append("未添加維生素礦物質補充成分")

output_lines.append(f"\n【預估營養標示（每片 {weight_per_piece}g）】")
for k, v in sim_nutrition.items():
    unit = 'kcal' if k == 'calories' else 'g' if k != 'sodium' else 'mg'
    output_lines.append(f"- {k.title()}: {v} {unit}")

output_lines.append("\n【AI 配方調整摘要】")
if goal_low_sugar:
    output_lines.append("- 砂糖減量50%，以赤藻糖醇替代")
if goal_protein:
    output_lines.append("- 添加濃縮蛋白粉 5%，減少部分低筋麵粉")
if goal_vitamins:
    output_lines.append("- 添加維礦複合粉 2%，補足日常營養素需求")
if not any([goal_low_sugar, goal_protein, goal_vitamins]):
    output_lines.append("- 無進行配方優化")

# 輸出結果
st.text("\n".join(output_lines))
