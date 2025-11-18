import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

# === 1. Load model và scaler ===
model = joblib.load("delivery_model.pkl")
scaler = joblib.load("delivery_scaler.pkl")


# === 2. Sidebar nhập thông tin ===
st.sidebar.header("🔧 Nhập thông tin đơn hàng")

# --- Ngày đặt hàng
order_date = st.sidebar.date_input("📅 Ngày đặt hàng", value=datetime.now().date())
# --- Giờ đặt hàng (lấy theo thời gian hiện tại)
order_time = datetime.now().time()
st.sidebar.write("⏰ Thời gian đặt hàng: ", order_time.strftime("%H:%M:%S"))
# --- Giờ pickup (tự động cộng thêm 15 phút)
pickup_time = (datetime.combine(order_date, order_time) + timedelta(minutes=15)).time()
st.sidebar.write("🚚 Giờ pickup (dự kiến): ", pickup_time.strftime("%H:%M:%S"))
# --- Loại đơn hàng
type_of_order = st.sidebar.selectbox("🍽️ Loại đơn hàng", ["Snack", "Meal", "Drinks", "Buffet"])
# --- Số lượng đơn gộp

multiple_deliveries = st.sidebar.selectbox("📦 Số đơn gộp",
                                         options=[0, 1, 2, 3],
                                         help="0: Không gộp đơn\n1: Gộp 1 đơn\n2: Gộp 2 đơn\n3: Gộp 3 đơn")
# --- Tuổi shipper
age = st.sidebar.number_input("Nhập tuổi người giao hàng", min_value=20, max_value=39, value=25)
# --- Rating của người giao hàng
valid_ratings = [1.0, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 
                 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 
                 4.6, 4.7, 4.8, 4.9, 5.0, 6.0] 

ratings = st.sidebar.selectbox("⭐ Chọn đánh giá người giao hàng", valid_ratings, index=valid_ratings.index(4.5))
# --- Tình trạng xe
vehicle_condition = st.sidebar.selectbox("🚗 Tình trạng xe", 
                                       options=[0, 1, 2, 3],
                                       help="0: Rất tốt, 1: Tốt, 2: Trung bình, 3: Kém")
# --- Loại phương tiện
type_of_vehicle = st.sidebar.selectbox("🛵 Loại xe", ["bicycle", "motorcycle", "scooter", "electric_scooter"])
# --- Loại khu vực
area_type = st.sidebar.selectbox("🏙️ Khu vực", ["Urban", "Metropolitian", "Semi-Urban"])
# --- Tên thành phố (City name)
city_list = ["Ludhiana", "Chennai", "Kochi", "Goa", "Aurangabad", "Jaipur",
    "Delhi", "Mumbai", "Agra", "Surat", "Indore", "Pune", "Allahabad", "Mysore",
    "Coimbatore","Hyderabad", "Vadodara", "Ranchi", "Bhopal", "Kolkatta", "Kanpur", "Bangalore"
]

city_name = st.sidebar.selectbox("🏢 Thành phố", city_list)
# --- Khoảng cách giao hàng (tính toán hoặc nhập trực tiếp)
distance_km = st.sidebar.number_input( "📏 Khoảng cách giao hàng (km)", min_value=0.257181737252861, max_value=31.830480783723594, value=18.1407697377135, step=0.1)
# --- Tình trạng giao thông
traffic = st.sidebar.selectbox("🚦 Mật độ giao thông", ["Low", "Medium", "High", "Jam"])
# --- Thời tiết
weather = st.sidebar.selectbox("⛅ Thời tiết", ["Sunny", "Stormy", "Sandstorms", "Cloudy", "Fog", "Windy"])
# --- Festival
is_holiday = 1 if order_date.strftime("%m-%d") in ["01-26", "08-15", "10-02", "12-25"] else 0
st.sidebar.write("🎉 Ngày lễ: ", "✅ Có" if is_holiday else "❌ Không")
# --- Thứ
day_of_week = datetime.combine(order_date, order_time).weekday()  # 0 = Monday
is_weekend = 1 if day_of_week >= 5 else 0
# --- Giờ đặt hàng và pickup
order_hour = order_time.hour
pickup_hour = pickup_time.hour
prepare_time = (datetime.combine(order_date, pickup_time) - datetime.combine(order_date, order_time)).seconds // 60

# Mapping dictionary
weather_dict = {"Cloudy": 0, "Fog": 1, "Sandstorms": 2, "Stormy": 3, "Sunny": 4, "Windy": 5}
traffic_dict = {"High": 0, "Jam": 1, "Low": 2, "Medium": 3}
order_dict = {"Buffet": 0, "Drinks": 1, "Meal": 2, "Snack": 3}
vehicle_dict = {"bicycle": 0, "electric_scooter": 1, "motorcycle": 2, "scooter": 3}
festival_dict = {"No": 0, "Yes": 1}
area_dict = {"Metropolitian": 0, "Semi-Urban": 1, "Urban": 2}
city_dict = {
    "Agra": 0, "Allahabad": 1, "Aurangabad": 2, "Bangalore": 3, "Bhopal": 4, "Chennai": 5, "Coimbatore": 6,
    "Delhi": 7, "Goa": 8, "Hyderabad": 9, "Indore": 10, "Jaipur": 11, "Kanpur": 12, "Kochi": 13,
    "Kolkatta": 14, "Ludhiana": 15, "Mumbai": 16, "Mysore": 17, "Pune": 18, "Ranchi": 19, "Surat": 20, "Vadodara": 21
}

# --- Tạo DataFrame đầu vào (ÁP DỤNG MAPPING TRƯỚC KHI TẠO DF)
input_dict = {
    "Delivery_person_Age": age,
    "Delivery_person_Ratings": ratings,
    "Weatherconditions": weather_dict[weather],  # Áp dụng mapping
    "Road_traffic_density": traffic_dict[traffic],  # Áp dụng mapping
    "Vehicle_condition": vehicle_condition,
    "Type_of_order": order_dict[type_of_order],  # Áp dụng mapping
    "Type_of_vehicle": vehicle_dict[type_of_vehicle],  # Áp dụng mapping
    "multiple_deliveries": multiple_deliveries,
    "Festival": is_holiday,
    "Area_Type": area_dict[area_type],  # Áp dụng mapping
    "City_name": city_dict[city_name],  # Áp dụng mapping
    "Distance_km": distance_km,
    "Order_Hour": order_hour,
    "Hour_Pickup": pickup_hour,
    "Order_Prepare_Time": prepare_time,
    "Day_of_Week": day_of_week,
    "Weekend": is_weekend,
    "month_intervals": order_date.month,
}
input_df = pd.DataFrame([input_dict])

# --- Tiền xử lý: scaler (đảm bảo tất cả đã là số)
input_scaled = scaler.transform(input_df)

# MAIN: Giao diện chính
st.markdown("# 🚀 Dự đoán thời gian giao hàng")
st.markdown("Ứng dụng sử dụng mô hình học máy để dự đoán thời gian giao hàng dựa trên thông tin đơn hàng, tài xế và điều kiện giao thông. Hãy nhập thông tin ở thanh bên trái để bắt đầu!")

st.image("https://cdn-icons-png.flaticon.com/512/3595/3595455.png", width=150)

# Thông tin nhanh
st.markdown("### 🔍 Tóm tắt đơn hàng")
col1, col2 = st.columns(2)
with col1:
    st.metric("📦 Đơn hàng", type_of_order)
    st.metric("🚗 Phương tiện", type_of_vehicle)
    st.metric("🌤️ Thời tiết", weather)
with col2:
    st.metric("🏙️ Thành phố", city_name)
    st.metric("🚦 Giao thông", traffic)
    st.metric("📏 Khoảng cách", f"{distance_km} km")

st.markdown("---")

# Nút dự đoán với hiệu ứng
if all([isinstance(age, (int, float)), 
        isinstance(ratings, (int, float)), 
        isinstance(distance_km, (int, float)), 
        isinstance(multiple_deliveries, (int))]):  
    if st.button("📊 Dự đoán thời gian giao hàng", key="predict_button", help="Nhấn để dự đoán"):
        prediction = model.predict(input_scaled)[0]
        st.markdown(f"""
            <div style='background: linear-gradient(45deg, #e6f3ff, #d1e9ff); padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
                <h3 style='color: #FF4B4B;'>⏱️ Thời gian dự đoán: <b>{round(prediction, 2)} phút</b></h3>
                <img src="https://cdn-icons-png.flaticon.com/512/190/190606.png" width="80" style="margin-top: 10px;">
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #fff3cd, #ffeeba); padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
            <p style='color: #856404; text-align: center;'>👉 Vui lòng điền đầy đủ thông tin ở thanh bên trái để bắt đầu dự đoán!</p>
            <img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" width="50" style="display: block; margin: 10px auto;">
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)