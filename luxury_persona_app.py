import streamlit as st

# 嘗試匯入 google.generativeai，如果使用者沒安裝，則顯示提示
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# -----------------------------------------------------------------------------
# 1. 頁面基礎設定 (Page Configuration)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="台灣頂級豪宅受眾深層分析儀 (AI Deep Search)",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 以優化視覺體驗 (High-End Look)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background-color: #0f172a; /* Slate 900 */
        color: white;
        border-radius: 8px;
        height: 3.5em;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #334155;
        border: 1px solid #94a3b8;
        transform: translateY(-2px);
    }
    h1 {
        color: #1e293b;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .highlight-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-top: 5px solid #0f172a;
        margin-bottom: 20px;
    }
    .ai-badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .persona-box {
        background-color: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 4px solid #0ea5e9; /* Sky Blue */
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 資料字典 (Domain Knowledge Database - 規則備用)
# -----------------------------------------------------------------------------
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
st.sidebar.title("💎 頂級豪宅受眾深層分析儀")
st.sidebar.caption("AI-Powered Luxury Real Estate Deep Search")
st.sidebar.divider()

# --- 新增：Gemini API 設定區域 ---
with st.sidebar.expander("🔐 AI 設定 (Gemini API)", expanded=True):
    # 無論是否有安裝套件，都顯示輸入框 (修正輸入欄位消失問題)
    api_key = st.text_input("輸入 Gemini API Key", type="password", help="貼上您的 Google Gemini API Key 以啟用 AI 深度分析功能")

    if not HAS_GENAI:
        st.error("⚠️ 系統偵測到未安裝 `google-generativeai`。即使輸入 Key 也無法使用 AI 功能，僅能使用規則模式。")
    elif api_key:
        st.success("API Key 已輸入，AI 模式就緒")
    else:
        st.warning("未輸入 Key，將使用內建模板模式")

st.sidebar.divider()

# 原有輸入與新功能
selected_archetype = st.sidebar.selectbox(
    "1. 選擇參考原型 (Archetype)",
    list(PERSONA_DB.keys()),
    help="AI 會參考此原型作為基礎，但會延伸出更多元的人物"
)

product_name = st.sidebar.text_input(
    "2. 輸入產品/建案名稱",
    value="信義傳世御邸",
    help="AI 會根據這個名稱進行深度模擬搜尋"
)

# --- 新增：銷售時期選擇 ---
sales_phase = st.sidebar.selectbox(
    "3. 選擇銷售時期 (Sales Phase)",
    ["潛銷期 (VVIP Preview)", "正式公開 (Grand Opening)", "成屋/餘屋銷售 (Legacy Sales)"],
    help="不同時期 AI 會生成不同的行銷切角"
)

generate_btn = st.sidebar.button("✨ 執行 AI 深度人物誌分析")

st.sidebar.divider()
st.sidebar.info("💡 **顧問提示：** \n\nAI 模式將模擬「深度搜尋 (Deep Search)」，為您挖掘 5 種精準的鄰居畫像與對應的廣告受眾設定。")

# -----------------------------------------------------------------------------
# 4. 主要顯示區 (Main Display Area)
# -----------------------------------------------------------------------------

def get_gemini_analysis(api_key, product, archetype, phase, base_data):
    """呼叫 Gemini API 進行深度分析，要求 5 種受眾"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        你是一位頂級房地產行銷顧問，具備市場「深度搜尋 (Deep Search)」的分析能力。
        請針對建案「{product}」進行深度住戶側寫與廣告受眾分析。

        【建案背景參考】
        - 案名：{product}
        - 銷售階段：{phase}
        - 基礎參考原型：{archetype}

        【任務指令】
        請模擬深度市場調查，挖掘會購買此豪宅的真實人物面貌。
        請務必提供「5 種不同的目標受眾類型 (5 Target Audiences)」，並針對每一種受眾提供精準的數位廣告設定。

        【輸出格式要求】
        請使用 Markdown 格式，針對這 5 種受眾，依序輸出以下資訊 (請勿使用程式碼區塊，直接輸出文字)：

        ### 受眾 1：[給予一個生動的代稱，例如：內湖科技新貴家庭]
        - **人物與鄰里刻劃**：(請生動描述他們的背景、職業、為何買這裡？他們在社區電梯裡會聊什麼？)
        - **Meta (FB/IG) 廣告建議**：
          - 興趣標籤：(列出 5-8 個精準興趣)
          - 行為/人口統計：(例如：經常出國、企業主...)
        - **Google 關鍵字建議**：(列出 8-10 個高搜尋意圖的關鍵字)

        ### 受眾 2：[代稱]
        ... (重複以上結構)
        
        ### 受眾 3：[代稱]
        ...
        
        ### 受眾 4：[代稱]
        ...
        
        ### 受眾 5：[代稱]
        ...

        最後，請針對「{phase}」為這群人寫一段通用的行銷短文案 (包含標題與 CTA)。
        """
        
        with st.spinner('🤖 AI 正在進行深度市場搜尋，分析 5 種潛在買家...'):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error: AI 分析失敗。原因：{str(e)}"

if generate_btn:
    # 取得選定原型的基礎資料
    base_data = PERSONA_DB[selected_archetype]
    
    st.title(f"🎯 深度受眾分析報告：{product_name}")
    st.caption(f"分析模式：AI Deep Search | 參考原型：{selected_archetype.split('(')[0]}")
    st.markdown("---")

    # ---------------------------------------
    # 邏輯分流：AI 模式 vs 規則模式
    # ---------------------------------------
    ai_result = None
    if api_key and HAS_GENAI:
        ai_result = get_gemini_analysis(api_key, product_name, selected_archetype, sales_phase, base_data)
        
        if "Error" in ai_result:
            st.error(ai_result)
            ai_result = None # Fallback to normal

    if ai_result:
        # ---------------------------------------
        # AI 模式顯示區：5 種受眾分析
        # ---------------------------------------
        st.markdown("<div class='ai-badge'>✨ AI 模擬深度搜尋結果</div>", unsafe_allow_html=True)
        st.subheader("👥 5 大精準受眾畫像與投放策略")
        st.info("以下是 AI 根據案名與地段屬性，為您挖掘出的 5 種潛在鄰居與廣告設定：")
        
        # 直接顯示 AI 生成的完整 Markdown，因為格式已經要求好了
        st.markdown(ai_result)
        
        st.markdown("---")
        st.success("💡 **顧問建議：** 您可以在 Meta 廣告後台建立 5 個不同的廣告組合 (Ad Sets)，分別測試上述 5 種受眾的成效。")

    else:
        # ---------------------------------------
        # 規則模式顯示區 (Fallback)
        # ---------------------------------------
        st.warning("⚠️ 未偵測到 API Key，切換回「標準規則模式」。(輸入 Key 可解鎖 5 種 AI 受眾分析)")
        
        # 區塊一：人物誌側寫
        st.subheader("1️⃣ 人物誌側寫 (Persona Profile)")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(label="📍 年齡層", value=base_data['profile']['age'])
        with col2: st.metric(label="😨 核心恐懼", value="需化解的抗性", delta=base_data['profile']['fear'], delta_color="inverse")
        with col3: st.metric(label="🤝 信任對象", value="KOL/Influencer", delta=base_data['profile']['trust'], delta_color="normal")
        with col4: 
            st.markdown("**🔑 決策關鍵字**")
            st.write("、".join([f"`{k}`" for k in base_data['profile']['decision_keywords']]))

        st.markdown("---")

        # 區塊二：數位足跡
        st.subheader("2️⃣ 數位足跡設定 (Ad Targeting)")
        ad_col1, ad_col2 = st.columns(2)
        with ad_col1:
            with st.container():
                st.markdown("""<div class="highlight-card"><h3 style="color:#1877F2;">📘 Meta (FB/IG)</h3></div>""", unsafe_allow_html=True)
                st.markdown(f"**包含興趣:** {', '.join(base_data['meta_ads']['interests'])}")
                st.markdown(f"**必須符合:** {', '.join(base_data['meta_ads']['behaviors'])}")
        with ad_col2:
            with st.container():
                st.markdown("""<div class="highlight-card"><h3 style="color:#EA4335;">🔎 Google Ads</h3></div>""", unsafe_allow_html=True)
                st.markdown(f"**搜尋關鍵字:** {', '.join(base_data['google_ads']['keywords'])}")
                st.markdown(f"**建議版位:** {', '.join(base_data['google_ads']['placements'])}")

        # 區塊三：文案模板
        st.subheader("3️⃣ 文案策略 (Template)")
        copy_data = base_data['copy_style']
        hook_text = copy_data['hook_template'].format(product_name=product_name)
        body_text = copy_data['body_template'].format(product_name=product_name)
        
        st.info(f"**🪝 標題:** {hook_text}")
        st.code(f"**📄 內文:** {body_text}", language="text")

else:
    # Welcome Screen
    st.container()
    st.markdown(
        """
        <div style="text-align: center; padding: 50px;">
            <h1>🏛️ 頂級豪宅受眾深層分析儀 (AI Hybrid)</h1>
            <p style="font-size: 1.2em; color: #666;">
                這不僅是人物誌，更是您的數位行銷顧問。<br>
                輸入 <b>Gemini API Key</b>，讓 AI 為您進行「深度市場搜尋」，<br>
                挖掘出 5 種精準的買家畫像與廣告關鍵字。
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.info("**Old Money**\n\n傳承、隱私")
    with col2: st.info("**Tech Titan**\n\n效率、科技")
    with col3: st.info("**Hidden Billionaire**\n\n土地、現金")
    with col4: st.info("**Global Successor**\n\n品味、ESG")
