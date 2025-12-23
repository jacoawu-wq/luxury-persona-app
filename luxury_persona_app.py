import streamlit as st

# -----------------------------------------------------------------------------
# 1. 頁面基礎設定 (Page Configuration)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="台灣頂級富豪 (Top 50) 人物誌生成器",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 以優化視覺體驗 (High-End Look)
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A; /* Royal Blue */
        color: white;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1e40af;
        border-color: #1e40af;
    }
    h1 {
        color: #0f172a;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2, h3 {
        color: #334155;
    }
    .highlight-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #1E3A8A;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 資料字典 (Domain Knowledge Database)
# -----------------------------------------------------------------------------
# 這裡儲存了四大原型的核心邏輯、標籤與文案模板
PERSONA_DB = {
    "傳產/金融家族掌門人 (The Old Money Patriarch)": {
        "profile": {
            "age": "70歲+",
            "fear": "富不過三代、家族醜聞、健康衰退",
            "trust": "家族辦公室主管、老臣、風水大師",
            "decision_keywords": ["傳承", "隱私", "風水", "稀缺性"]
        },
        "meta_ads": {
            "interests": ["Private banking", "Family office", "Patek Philippe", "Rolls-Royce", "Sotheby's (蘇富比)"],
            "behaviors": ["頻繁的國際旅遊者", "高消費用戶 (台灣)", "豪華渡假村訪客"],
            "exclude": ["折扣優惠券", "平價連鎖餐飲", "手機遊戲"]
        },
        "google_ads": {
            "keywords": ["家族信託設立", "資產傳承稅務規劃", "瑞士抗衰老中心", "蘇富比古董拍賣", "陽明山獨棟別墅"],
            "placements": ["財訊雙週刊", "工商時報", "Classical FM", "高爾夫球賽事直播"]
        },
        "copy_style": {
            "tone": "尊榮、穩重、帶有歷史感",
            "hook_template": "致 {product_name} 的收藏者：有些資產，是為了下一個百年而存在。",
            "body_template": "在動盪的時代，唯有傳承是永恆的課題。{product_name} 坐擁絕佳風水寶地，不僅是隱私的堡壘，更是家族榮耀的基石。專為極少數懂得鑑賞歷史的領袖保留。",
            "cta_template": "預約私人鑑賞 (僅限受邀)"
        }
    },
    "科技業創辦人 (The Tech Titan)": {
        "profile": {
            "age": "55-65歲",
            "fear": "企業資安漏洞、技術落後、無效率的時間浪費",
            "trust": "數據分析報告、科技顧問、同溫層企業主",
            "decision_keywords": ["效率", "隱私安全", "智能整合", "數據"]
        },
        "meta_ads": {
            "interests": ["Tesla", "SpaceX", "Artificial intelligence", "Bloomberg Markets", "The Economist"],
            "behaviors": ["Facebook 專頁管理員 (商業)", "新科技早期採用者", "商務艙旅客"],
            "exclude": ["星座命理", "八卦娛樂新聞", "團購網"]
        },
        "google_ads": {
            "keywords": ["私人飛機租賃服務", "全戶智慧豪宅系統", "全球半導體供應鏈", "內湖/竹北 高端房產", "資安防護系統"],
            "placements": ["TechCrunch", "Bloomberg TV", "WSJ (華爾街日報)", "LinkedIn"]
        },
        "copy_style": {
            "tone": "理性、精準、強調規格與未來性",
            "hook_template": "極致效率，由此定義。{product_name} 獻給掌握未來的決策者。",
            "body_template": "您的時間比黃金更珍貴。{product_name} 導入頂級智慧生態系統，將維安與舒適度量化為最高標準。這不只是資產，更是您全球佈局中最安靜、最聰明的休息站。",
            "cta_template": "索取詳細規格白皮書"
        }
    },
    "隱形冠軍/神秘地主 (The Hidden Billionaire)": {
        "profile": {
            "age": "50-70歲",
            "fear": "通貨膨脹、資產縮水、外人看不起",
            "trust": "同鄉會/商會好友、會計師、土地代書",
            "decision_keywords": ["保值", "地段", "大氣", "實體資產"]
        },
        "meta_ads": {
            "interests": ["Mercedes-Benz S-Class", "土地開發", "黃金投資", "茶藝/普洱茶", "獅子會/扶輪社"],
            "behaviors": ["對房地產感興趣的人", "中小企業主", "經常往返中南部"],
            "exclude": ["虛擬貨幣", "動漫遊戲", "打工度假"]
        },
        "google_ads": {
            "keywords": ["農地工廠法規", "工業用地買賣", "七期/農十六 豪宅", "原木家具訂製", "法拍屋資訊"],
            "placements": ["Mobile01 居家房產版", "591 房屋交易", "股市同學會", "在地新聞網"]
        },
        "copy_style": {
            "tone": "直白、霸氣、強調有土斯有財",
            "hook_template": "真金不怕火煉，地段決定身價。{product_name} —— 王者的眼光。",
            "body_template": "打拚一世人，就是要住最好的。{product_name} 佔據市中心最後一塊帝王軸線，正如您的事業版圖一樣穩如泰山。買這裡，不只是享受，更是把現金變成傳世的資產。",
            "cta_template": "立即了解增值潛力"
        }
    },
    "新貴/接班二代 (The Global Successor)": {
        "profile": {
            "age": "35-45歲",
            "fear": "平庸、被貼標籤(靠爸族)、缺乏影響力",
            "trust": "KOL/網紅、米其林指南、歐美名校校友圈",
            "decision_keywords": ["品味", "ESG", "獨特性", "圈層認同"]
        },
        "meta_ads": {
            "interests": ["Contemporary art (當代藝術)", "Art Basel", "Michelin Guide", "Supercars (Ferrari/Porsche)", "Triathlon (鐵人三項)"],
            "behaviors": ["豪華精品購物者", "Instagram 重度使用者", "留學顧問/移民興趣"],
            "exclude": ["直銷/微商", "低俗迷因專頁", "傳統電視購物"]
        },
        "google_ads": {
            "keywords": ["影響力投資 (Impact Investing)", "限量潮玩藝術品", "遊艇派對策劃", "信義區/大安區 設計宅", "高端留學諮詢"],
            "placements": ["VOGUE/GQ", "Hypebeast", "Instagram Stories", "Podcast (股癌/百靈果)"]
        },
        "copy_style": {
            "tone": "感性、美學導向、強調自我實現",
            "hook_template": "不僅是奢華，更是靈魂的共鳴。在 {product_name} 遇見您的生活哲學。",
            "body_template": "世界很大，但能懂您品味的地方很少。{product_name} 融合國際建築美學與 ESG 永續理念，打造專屬於您的私人藝廊。這裡不是用來炫耀的，是用來獎賞那個努力超越父輩的自己。",
            "cta_template": "預約私人鑑賞 (RSVP Only)"
        }
    }
}

# -----------------------------------------------------------------------------
# 3. 側邊欄輸入區 (Sidebar Inputs)
# -----------------------------------------------------------------------------
st.sidebar.title("💎 頂級人物誌產生器")
st.sidebar.markdown("專為 MarTech 與 高端房產行銷 設計")
st.sidebar.divider()

selected_archetype = st.sidebar.selectbox(
    "1. 選擇富豪原型 (Archetype)",
    list(PERSONA_DB.keys())
)

product_name = st.sidebar.text_input(
    "2. 輸入產品/建案名稱",
    value="信義傳世御邸",
    help="這個名稱將會被代入 AI 文案模板中"
)

generate_btn = st.sidebar.button("✨ 生成人物誌與投放策略")

st.sidebar.divider()
st.sidebar.info("💡 **顧問提示：** \n\n不同原型的「信任貨幣」不同。\n老錢看關係，新貴看品味，科技看數據，地主看實體。")

# -----------------------------------------------------------------------------
# 4. 主要顯示區 (Main Display Area)
# -----------------------------------------------------------------------------
if generate_btn:
    # 取得選定原型的資料
    data = PERSONA_DB[selected_archetype]
    
    st.title(f"🎯 目標受眾分析報告：{selected_archetype.split('(')[0]}")
    st.markdown(f"**針對產品：** `{product_name}` 的完整行銷策略")
    st.markdown("---")

    # ---------------------------------------
    # 區塊一：人物誌側寫 (Persona Card)
    # ---------------------------------------
    st.subheader("1️⃣ 人物誌側寫 (Persona Profile)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📍 年齡層", value=data['profile']['age'])
    with col2:
        st.metric(label="😨 核心恐懼", value="需化解的抗性", delta=data['profile']['fear'], delta_color="inverse")
    with col3:
        st.metric(label="🤝 信任對象", value="KOL/Influencer", delta=data['profile']['trust'], delta_color="normal")
    with col4:
        st.markdown("**🔑 決策關鍵字**")
        st.write("、".join([f"`{k}`" for k in data['profile']['decision_keywords']]))

    st.markdown("---")

    # ---------------------------------------
    # 區塊二：數位足跡與廣告設定 (Ad Targeting)
    # ---------------------------------------
    st.subheader("2️⃣ 數位足跡與廣告設定 (Ad Targeting)")
    
    ad_col1, ad_col2 = st.columns(2)

    with ad_col1:
        with st.container():
            st.markdown(
                """
                <div class="highlight-card">
                    <h3 style="color:#1877F2;">📘 Meta (FB/IG) 設定建議</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown("**🎯 包含興趣 (Interests):**")
            st.success(" OR ".join(data['meta_ads']['interests']))
            
            st.markdown("**✅ 必須符合 (Behaviors):**")
            st.info(" AND ".join(data['meta_ads']['behaviors']))
            
            st.markdown("**🚫 建議排除 (Exclude):**")
            st.error(", ".join(data['meta_ads']['exclude']))

    with ad_col2:
        with st.container():
            st.markdown(
                """
                <div class="highlight-card">
                    <h3 style="color:#EA4335;">🔎 Google Ads 關鍵字佈局</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown("**🔍 高搜尋意圖關鍵字 (High Intent Keywords):**")
            # 使用 Chips 風格顯示
            keywords_html = " ".join([f"<span style='background-color:#eee; padding:5px 10px; border-radius:15px; margin-right:5px; display:inline-block; margin-bottom:5px;'>{k}</span>" for k in data['google_ads']['keywords']])
            st.markdown(keywords_html, unsafe_allow_html=True)
            
            st.markdown("") # Spacer
            st.markdown("**📺 建議投遞版位/頻道 (Placements):**")
            st.write(", ".join(data['google_ads']['placements']))

    st.markdown("---")

    # ---------------------------------------
    # 區塊三：AI 文案建議 (Copywriting)
    # ---------------------------------------
    st.subheader("3️⃣ AI 文案策略建議 (Copywriting)")
    
    copy_data = data['copy_style']
    
    # 填入產品名稱
    hook_text = copy_data['hook_template'].format(product_name=product_name)
    body_text = copy_data['body_template'].format(product_name=product_name)
    cta_text = copy_data['cta_template']

    with st.expander("📝 點擊查看文案策略邏輯", expanded=True):
        st.markdown(f"**🎨 文案風格 (Tone & Voice):** {copy_data['tone']}")
        
        st.divider()
        
        col_copy1, col_copy2 = st.columns([1, 2])
        
        with col_copy1:
            st.markdown("### 🪝 廣告標題 (Hook)")
            st.info(hook_text)
            
            st.markdown("### 👆 呼籲行動 (CTA)")
            st.warning(cta_text)

        with col_copy2:
            st.markdown("### 📄 廣告內文 (Body)")
            st.code(body_text, language="text")
            st.caption("*提示：請點擊右上角複製按鈕，並根據實際坪數與公設細節進行微調。*")

else:
    # 初始歡迎畫面
    st.container()
    st.markdown(
        """
        <div style="text-align: center; padding: 50px;">
            <h1>🏛️ 歡迎使用頂級資產行銷系統</h1>
            <p style="font-size: 1.2em; color: #666;">
                這是一套結合數據科學與消費心理學的工具。<br>
                請從左側欄位選擇您的目標客群原型，以生成精準的行銷策略。
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 顯示四大原型簡介
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("**Old Money**\n\n傳承、隱私、信託")
    with col2:
        st.info("**Tech Titan**\n\n效率、科技、數據")
    with col3:
        st.info("**Hidden Billionaire**\n\n土地、現金、增值")
    with col4:
        st.info("**Global Successor**\n\n品味、藝術、ESG")

# -----------------------------------------------------------------------------
# End of App
# -----------------------------------------------------------------------------