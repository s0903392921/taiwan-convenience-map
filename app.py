import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

# 設定頁面
st.set_page_config(
    page_title="台灣生活便利性評分系統",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗺️ 台灣生活便利性評分系統")
st.markdown("選擇縣市和行政區，查看該地區的詳細便利性評分")
st.markdown("---")

# ==================== 數據定義 ====================
# 六都的詳細數據
six_cities_data = {
    "臺北市": {
        "districts": {
            "大安區": {
                "coords": [25.026, 121.543],
                "convenience": {
                    "超商數量": 285,
                    "超市數量": 12,
                    "便利店密度": 23.5,  # 每平方公里
                },
                "transport": {
                    "捷運站": 8,
                    "公車路線": 45,
                    "計程車數量": 320,
                    "交通便利度": 95,  # 1-100
                },
                "medical": {
                    "醫院": 15,
                    "診所": 180,
                    "藥局": 95,
                    "醫療覆蓋度": 92,
                },
                "education": {
                    "國小": 8,
                    "國中": 5,
                    "高中": 3,
                    "大學": 2,
                    "教育資源數": 18,
                }
            },
            "信義區": {
                "coords": [25.033, 121.564],
                "convenience": {
                    "超商數量": 210,
                    "超市數量": 8,
                    "便利店密度": 18.8,
                },
                "transport": {
                    "捷運站": 6,
                    "公車路線": 35,
                    "計程車數量": 250,
                    "交通便利度": 88,
                },
                "medical": {
                    "醫院": 12,
                    "診所": 145,
                    "藥局": 78,
                    "醫療覆蓋度": 85,
                },
                "education": {
                    "國小": 6,
                    "國中": 4,
                    "高中": 2,
                    "大學": 1,
                    "教育資源數": 13,
                }
            },
            "內湖區": {
                "coords": [25.069, 121.589],
                "convenience": {
                    "超商數量": 180,
                    "超市數量": 6,
                    "便利店密度": 5.7,
                },
                "transport": {
                    "捷運站": 5,
                    "公車路線": 28,
                    "計程車數量": 180,
                    "交通便利度": 72,
                },
                "medical": {
                    "醫院": 8,
                    "診所": 110,
                    "藥局": 55,
                    "醫療覆蓋度": 68,
                },
                "education": {
                    "國小": 7,
                    "國中": 3,
                    "高中": 2,
                    "大學": 0,
                    "教育資源數": 12,
                }
            },
            "文山區": {
                "coords": [24.998, 121.570],
                "convenience": {
                    "超商數量": 160,
                    "超市數量": 5,
                    "便利店密度": 5.1,
                },
                "transport": {
                    "捷運站": 4,
                    "公車路線": 22,
                    "計程車數量": 140,
                    "交通便利度": 65,
                },
                "medical": {
                    "醫院": 6,
                    "診所": 95,
                    "藥局": 48,
                    "醫療覆蓋度": 58,
                },
                "education": {
                    "國小": 8,
                    "國中": 4,
                    "高中": 2,
                    "大學": 1,
                    "教育資源數": 15,
                }
            },
        }
    },
    "新北市": {
        "districts": {
            "板橋區": {
                "coords": [25.011, 121.465],
                "convenience": {
                    "超商數量": 320,
                    "超市數量": 15,
                    "便利店密度": 13.8,
                },
                "transport": {
                    "捷運站": 9,
                    "公車路線": 52,
                    "計程車數量": 380,
                    "交通便利度": 92,
                },
                "medical": {
                    "醫院": 18,
                    "診所": 200,
                    "藥局": 105,
                    "醫療覆蓋度": 90,
                },
                "education": {
                    "國小": 12,
                    "國中": 6,
                    "高中": 4,
                    "大學": 1,
                    "教育資源數": 23,
                }
            },
            "三重區": {
                "coords": [25.062, 121.498],
                "convenience": {
                    "超商數量": 240,
                    "超市數量": 10,
                    "便利店密度": 14.7,
                },
                "transport": {
                    "捷運站": 6,
                    "公車路線": 38,
                    "計程車數量": 270,
                    "交通便利度": 82,
                },
                "medical": {
                    "醫院": 12,
                    "診所": 155,
                    "藥局": 80,
                    "醫療覆蓋度": 78,
                },
                "education": {
                    "國小": 10,
                    "國中": 5,
                    "高中": 3,
                    "大學": 0,
                    "教育資源數": 18,
                }
            },
            "淡水區": {
                "coords": [25.170, 121.442],
                "convenience": {
                    "超商數量": 120,
                    "超市數量": 4,
                    "便利店密度": 1.7,
                },
                "transport": {
                    "捷運站": 3,
                    "公車路線": 15,
                    "計程車數量": 95,
                    "交通便利度": 42,
                },
                "medical": {
                    "醫院": 5,
                    "診所": 65,
                    "藥局": 32,
                    "醫療覆蓋度": 38,
                },
                "education": {
                    "國小": 6,
                    "國中": 3,
                    "高中": 1,
                    "大學": 0,
                    "教育資源數": 10,
                }
            },
        }
    },
    "臺中市": {
        "districts": {
            "西屯區": {
                "coords": [24.182, 120.623],
                "convenience": {
                    "超商數量": 250,
                    "超市數量": 12,
                    "便利店密度": 6.3,
                },
                "transport": {
                    "捷運站": 4,
                    "公車路線": 32,
                    "計程車數量": 220,
                    "交通便利度": 72,
                },
                "medical": {
                    "醫院": 14,
                    "診所": 170,
                    "藥局": 88,
                    "醫療覆蓋度": 82,
                },
                "education": {
                    "國小": 9,
                    "國中": 4,
                    "高中": 3,
                    "大學": 1,
                    "教育資源數": 17,
                }
            },
            "北屯區": {
                "coords": [24.181, 120.697],
                "convenience": {
                    "超商數量": 200,
                    "超市數量": 8,
                    "便利店密度": 3.2,
                },
                "transport": {
                    "捷運站": 3,
                    "公車路線": 25,
                    "計程車數量": 180,
                    "交通便利度": 58,
                },
                "medical": {
                    "醫院": 10,
                    "診所": 125,
                    "藥局": 65,
                    "醫療覆蓋度": 65,
                },
                "education": {
                    "國小": 8,
                    "國中": 4,
                    "高中": 2,
                    "大學": 0,
                    "教育資源數": 14,
                }
            },
        }
    },
    "高雄市": {
        "districts": {
            "三民區": {
                "coords": [22.643, 120.328],
                "convenience": {
                    "超商數量": 280,
                    "超市數量": 13,
                    "便利店密度": 14.2,
                },
                "transport": {
                    "捷運站": 7,
                    "公車路線": 40,
                    "計程車數量": 310,
                    "交通便利度": 85,
                },
                "medical": {
                    "醫院": 16,
                    "診所": 185,
                    "藥局": 95,
                    "醫療覆蓋度": 88,
                },
                "education": {
                    "國小": 11,
                    "國中": 5,
                    "高中": 3,
                    "大學": 2,
                    "教育資源數": 21,
                }
            },
            "苓雅區": {
                "coords": [22.621, 120.329],
                "convenience": {
                    "超商數量": 155,
                    "超市數量": 6,
                    "便利店密度": 19.0,
                },
                "transport": {
                    "捷運站": 4,
                    "公車路線": 28,
                    "計程車數量": 180,
                    "交通便利度": 72,
                },
                "medical": {
                    "醫院": 9,
                    "診所": 110,
                    "藥局": 56,
                    "醫療覆蓋度": 68,
                },
                "education": {
                    "國小": 5,
                    "國中": 3,
                    "高中": 1,
                    "大學": 0,
                    "教育資源數": 9,
                }
            },
            "左營區": {
                "coords": [22.690, 120.301],
                "convenience": {
                    "超商數量": 200,
                    "超市數量": 9,
                    "便利店密度": 10.3,
                },
                "transport": {
                    "捷運站": 5,
                    "公車路線": 32,
                    "計程車數量": 240,
                    "交通便利度": 78,
                },
                "medical": {
                    "醫院": 11,
                    "診所": 140,
                    "藥局": 72,
                    "醫療覆蓋度": 75,
                },
                "education": {
                    "國小": 7,
                    "國中": 4,
                    "高中": 2,
                    "大學": 1,
                    "教育資源數": 14,
                }
            },
        }
    },
    "臺南市": {
        "districts": {
            "東區": {
                "coords": [22.989, 120.220],
                "convenience": {
                    "超商數量": 180,
                    "超市數量": 8,
                    "便利店密度": 8.2,
                },
                "transport": {
                    "捷運站": 0,
                    "公車路線": 18,
                    "計程車數量": 120,
                    "交通便利度": 48,
                },
                "medical": {
                    "醫院": 8,
                    "診所": 95,
                    "藥局": 48,
                    "醫療覆蓋度": 58,
                },
                "education": {
                    "國小": 6,
                    "國中": 3,
                    "高中": 1,
                    "大學": 0,
                    "教育資源數": 10,
                }
            },
            "中西區": {
                "coords": [22.994, 120.203],
                "convenience": {
                    "超商數量": 165,
                    "超市數量": 7,
                    "便利店密度": 9.5,
                },
                "transport": {
                    "捷運站": 0,
                    "公車路線": 15,
                    "計程車數量": 110,
                    "交通便利度": 42,
                },
                "medical": {
                    "醫院": 7,
                    "診所": 85,
                    "藥局": 44,
                    "醫療覆蓋度": 52,
                },
                "education": {
                    "國小": 5,
                    "國中": 2,
                    "高中": 1,
                    "大學": 1,
                    "教育資源數": 9,
                }
            },
        }
    },
    "桃園市": {
        "districts": {
            "桃園區": {
                "coords": [25.041, 121.313],
                "convenience": {
                    "超商數量": 220,
                    "超市數量": 10,
                    "便利店密度": 7.8,
                },
                "transport": {
                    "捷運站": 2,
                    "公車路線": 28,
                    "計程車數量": 200,
                    "交通便利度": 65,
                },
                "medical": {
                    "醫院": 11,
                    "診所": 135,
                    "藥局": 70,
                    "醫療覆蓋度": 72,
                },
                "education": {
                    "國小": 9,
                    "國中": 4,
                    "高中": 2,
                    "大學": 0,
                    "教育資源數": 15,
                }
            },
            "中壢區": {
                "coords": [24.960, 121.233],
                "convenience": {
                    "超商數量": 200,
                    "超市數量": 9,
                    "便利店密度": 6.5,
                },
                "transport": {
                    "捷運站": 1,
                    "公車路線": 22,
                    "計程車數量": 170,
                    "交通便利度": 55,
                },
                "medical": {
                    "醫院": 9,
                    "診所": 115,
                    "藥局": 58,
                    "醫療覆蓋度": 62,
                },
                "education": {
                    "國小": 8,
                    "國中": 3,
                    "高中": 2,
                    "大學": 1,
                    "教育資源數": 14,
                }
            },
        }
    },
}

# ==================== 側邊欄選擇 ====================
st.sidebar.header("📍 選擇地區")
county = st.sidebar.selectbox(
    "選擇縣市",
    list(six_cities_data.keys())
)

district = st.sidebar.selectbox(
    "選擇行政區",
    list(six_cities_data[county]["districts"].keys())
)

selected_data = six_cities_data[county]["districts"][district]

# ==================== 主要內容區 ====================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 台灣地圖")
    
    # 建立地圖
    m = folium.Map(
        location=[24.5, 121.2],
        zoom_start=8,
        tiles="CartoDB positron"
    )
    
    # 在地圖上標記所有行政區
    for city_name, city_data in six_cities_data.items():
        for dist_name, dist_data in city_data["districts"].items():
            coords = dist_data["coords"]
            # 檢查是否為選中的行政區
            if city_name == county and dist_name == district:
                color = "red"
                popup_text = f"<b>{city_name} {dist_name}</b><br>（已選中）"
            else:
                color = "blue"
                popup_text = f"{city_name} {dist_name}"
            
            folium.CircleMarker(
                location=coords,
                radius=8,
                popup=popup_text,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)
    
    st_folium(m, width="100%", height=550)

with col2:
    st.subheader("📊 詳細評分")
    
    # 計算評分
    convenience_score = min(100, (selected_data["convenience"]["超商數量"] + 
                                   selected_data["convenience"]["超市數量"] * 2) / 3)
    transport_score = selected_data["transport"]["交通便利度"]
    medical_score = selected_data["medical"]["醫療覆蓋度"]
    education_score = min(100, selected_data["education"]["教育資源數"] * 5)
    
    # 總分（平均）
    total_score = (convenience_score + transport_score + medical_score + education_score) / 4
    
    st.metric("🏆 總體評分", f"{total_score:.1f}", "/ 100")
    st.markdown("---")
    
    st.metric("🏪 生活機能", f"{convenience_score:.1f}", "/ 100")
    st.metric("🚌 交通便利性", f"{transport_score:.1f}", "/ 100")
    st.metric("🏥 醫療資源", f"{medical_score:.1f}", "/ 100")
    st.metric("🎓 教育資源", f"{education_score:.1f}", "/ 100")

# ==================== 詳細資料區 ====================
st.markdown("---")
st.subheader(f"📈 {county} {district} - 詳細數據")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🏪 生活機能")
    st.write(f"超商數量: {selected_data['convenience']['超商數量']} 間")
    st.write(f"超市數量: {selected_data['convenience']['超市數量']} 間")
    st.write(f"便利店密度: {selected_data['convenience']['便利店密度']} / km²")

with col2:
    st.markdown("### 🚌 交通")
    st.write(f"捷運站: {selected_data['transport']['捷運站']} 個")
    st.write(f"公車路線: {selected_data['transport']['公車路線']} 條")
    st.write(f"計程車數量: {selected_data['transport']['計程車數量']} 輛")

with col3:
    st.markdown("### 🏥 醫療")
    st.write(f"醫院: {selected_data['medical']['醫院']} 間")
    st.write(f"診所: {selected_data['medical']['診所']} 間")
    st.write(f"藥局: {selected_data['medical']['藥局']} 間")

with col4:
    st.markdown("### 🎓 教育")
    st.write(f"國小: {selected_data['education']['國小']} 所")
    st.write(f"國中: {selected_data['education']['國中']} 所")
    st.write(f"高中: {selected_data['education']['高中']} 所")
    st.write(f"大學: {selected_data['education']['大學']} 所")
