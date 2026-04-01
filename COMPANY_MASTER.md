# ArgiNex 公司總架構 — COMPANY_MASTER
建立日期：2026-03-26
版本：v5.5（五系統分離版）
最後更新：2026-04-01
用途：唯一主文件。每次開新 Desktop 對話，跟 Claude 說「去桌面讀 COMPANY_MASTER.md」即可開工。
存放位置：/Users/zhongbinghuan/Desktop/COMPANY_MASTER.md + GitHub repo（四份同步）

---

## ㊀ 公司定位與戰略

**一句話定義：** Alex 是農業產品設計師 + 產官學整合者，不是工廠老闆
**商業本質：** 輕資產通路公司，製造全部外包農會
**核心工作：** 設計產品、串聯資源（產官學）、開拓市場
**競爭壁壘：** IOT 綁定農會 + 自動化標籤鎖住客戶 + 系統速度

### 戰略飛輪
```
盤商/客戶說「我缺XX」（需求拉動）
    → 海大開發配方（學術資源）
    → 農會代工生產（IOT 綁定 + 零建廠成本）
    → QC 驗收 → 客製標籤 → 出貨
    → 盤商鋪到 50~100 店家
    → 盤商回饋下一個需求 → 循環啟動
```

### 產官學三角
```
產（盤商/通路）→ 市場需求 + 訂單收入
官（農會/補助）→ 場地 + 人力 + 政府資金
學（海大/研究）→ 技術配方 + 學術背書
Alex = 中間整合者
```

### 三種客戶
| 類型 | 客戶樣貌 | 訂單特性 | 鎖客機制 |
|------|---------|---------|---------|
| 盤商 | 食品經銷商，覆蓋 50~100 店 | 量大、每月回購 | 品牌綁定（自有 Logo） |
| 團購主 | 社群媽媽群組 | 中小量、季節性爆量 | 社群口碑擴散 |
| 企業 | 公司採購/公關 | 一次性大單、高單價 | 採購慣性 + CIS 綁定 |

**50 盤商 × 50~100 店 = 2,500~5,000 店覆蓋**

---

## ㊁ 四大系統總覽

| 系統 | 名稱 | 對象 | Repo | 已建 | 目標 | 狀態 |
|------|------|------|------|------|------|------|
| S1 | ArgiNex 業務系統 | 農產品 CRM + 標籤自動化 | arginex-business | 4 | 8+ | ✅ LINE Bot MVP 上線 |
| S2 | IOT 農會加速器 + 公司會計 | 農會生產+公司財務 | iot-automation | 57 | 57 | ✅ 運行中 |
| S3 | 網路行銷系統 | 品牌行銷+競品情報 | 尚未建 | 0 | 25 | 📋 規劃中 |
| S4 | 秘書記帳系統 | 個人財務 | family-bot | 14 | 14 | ✅ 運行中 |
| S5 | TMO Leverage Model | 生技儀器業務情報 | leverage-model-bot | 3 | 10+ | 🔄 暫停 |
| | | | **合計** | **73** | **103+** | |

**原則：** 每個系統獨立開發/運作/試算表。任一系統壞掉不影響其他三個。系統 3 是跨系統匯流點，只讀取不寫入。

### 完整商業流程（零斷點）
```
主線：競品情報(S3) → 客戶需求(S1) → 產品開發(S1) → 農會生產(S2) → QC驗收(S2) → 標籤+出貨(S1)
行銷線：網紅行銷(S3) → 曝光+詢價(S3) → 新客戶(S1) → 公司收款(S2)
回饋線：客戶回饋 + 競品變動 → 觸發下一輪產品開發
```

---

## ㊂ 知識圖譜 — 21 個節點

（同 v5.2，省略重複。完整內容見各系統章節。）

### 系統 1 — 業務：8 個節點
| 節點 | ID | 主要欄位 | 連結 |
|------|-----|---------|------|
| 客戶 | C_ID | 名稱/類型(盤商・團購・企業)/區域/覆蓋人數/管道 | — |
| 訂單 | O_ID | 數量/金額/狀態/出貨日 | →C_ID →P_ID →F_ID |
| 產品 | P_ID | 品名/規格/售價/開發階段 | →F_ID →R_ID |
| 拜訪記錄 | V_ID | 日期/摘要/需求回饋/下次行動 | →C_ID |
| 產品管線 | PL_ID | 階段/海大進度/預計上市 | →P_ID →C_ID(需求來源) |
| 報價單 | Q_ID | 金額/有效期/狀態 | →C_ID →P_ID |
| 標籤設計 | DG_ID | Logo/風格/Canva連結/包裝規格 | →C_ID →P_ID →O_ID |
| 包裝單 | PK_ID | 刀模/色號/材質/供應商/交期 | →DG_ID →O_ID |

### 系統 2 — IOT + 公司會計：6 個節點
| 節點 | ID | 主要欄位 | 連結 |
|------|-----|---------|------|
| 農會 | F_ID | 名稱/區域/總幹事/產能/IOT狀態 | — |
| 生產批次 | B_ID | 投料日/完工日/數量 | →F_ID →O_ID →P_ID |
| 品質紀錄 | QC_ID | 檢驗項目/結果/合格否/處理方式 | →B_ID |
| 配方 | R_ID | 海大計畫編號/原料配比/製程參數/版本 | →P_ID |
| 公司收支 | CT_ID | 日期/金額/分類/應收應付/付款狀態 | →O_ID →B_ID |
| 庫存 | INV_ID | 原料庫存/成品庫存/安全庫存量 | →P_ID →F_ID |

### 系統 3 — 行銷：5 個節點
| 節點 | ID | 主要欄位 | 連結 |
|------|-----|---------|------|
| 詢價紀錄 | L_ID | 來源/聯絡人/需求/轉換狀態 | →C_ID |
| 行銷活動 | M_ID | 管道/內容/日期/曝光/點擊/詢價數 | →L_ID |
| 微網紅 | KOL_ID | 名稱/平台/粉絲數(5K~10K)/互動率/報價/帶貨量 | →M_ID |
| 競品 | CP_ID | 品名/品牌/價格/通路/包裝/行銷策略 | — |
| 社群留言 | SC_ID | 平台/貼文/留言內容/回覆內容/風格/狀態 | — |

### 系統 4 — 個人記帳：2 個節點
| 節點 | ID | 主要欄位 | 連結 |
|------|-----|---------|------|
| 個人收支 | PT_ID | 日期/金額/分類(薪資/生活/投資) | — |
| 個人發票 | PI_ID | 金額/日期/圖檔連結/報帳分類 | →PT_ID |

### 關鍵連線（圖譜的邊）
| 起點 | 關係 | 終點 | 權重 |
|------|------|------|------|
| 客戶 C_ID | 下單 | 訂單 O_ID | 訂單金額 |
| 訂單 O_ID | 指定生產 | 農會 F_ID | 數量 |
| 農會 F_ID | 產出 | 生產批次 B_ID | 產量 |
| 生產批次 B_ID | 驗收 | 品質紀錄 QC_ID | 合格率 |
| 訂單 O_ID | 產生 | 公司收支 CT_ID | 毛利 |
| 客戶 C_ID | 回饋需求 | 產品管線 PL_ID | 預估量 |
| 詢價紀錄 L_ID | 轉換 | 客戶 C_ID | 轉換率 |
| 配方 R_ID | 定義 | 產品 P_ID | 版本數 |
| 微網紅 KOL_ID | 執行 | 行銷活動 M_ID | ROI |
| 標籤設計 DG_ID | 綁定 | 客戶 C_ID | 鎖客強度 |

---

## ㊃ 架構核心準則

### Agent 分類
```
收集型 Agent（input_*）   → 只負責收集數據寫入 Sheet
判斷型 Agent（rules_*）   → 分析數據做決策
執行型 Agent（output_*）  → 執行動作（推播/控制/產生文件）
設計型 Agent              → 產生視覺輸出（標籤/QR Code/PDF）
呈現型 Agent              → 彙整數據（儀表板/報表）
協調型 Agent（core_*）    → 串聯所有 Agent（資料庫/排程/路由）
```

### 核心原則
- **Google Sheet 是神經系統**：所有 Agent 不直接互相呼叫，只透過 Sheet 交換數據
- **system_events 是圖譜的邊**：跨 Agent 串聯透過事件驅動
- **欄位契約**：欄位只能新增，不能改名或刪除
- **三層完全獨立**：收集層只寫入 / 決策層只判斷 / 輸出層只執行
- **時區統一**：ISO 格式含時區 `2026-03-26T14:30:00+08:00`
- **API 限制**：Google Sheet 每分鐘 60 次讀寫，排程錯開
- **MVP 優先**：能用就開始用，邊用邊改
- **Rewrite > Patch**：模組有邏輯問題時整個重寫，不要疊補丁

---

## ㊄ 系統 1 — 業務系統（收入引擎）

### 部署資訊
| 項目 | 內容 |
|------|------|
| LINE Bot | LM情報助理 @997qsojr |
| Render URL | https://leverage-model-bot.onrender.com |
| Render 方案 | Free Tier（目前幾乎空的，不需要 always-on） |
| GitHub | alexchung-lm/arginex-business（main） |
| Service Account | leverage-model-bot@leverage-model.iam.gserviceaccount.com |
| Google Sheet ID | 1nN4Wol_tLA--bZdBt0xnKq-lgW7HbKumcmGU8EmKGic |

### 功能模組
- 客戶關係管理 (CRM)：三種客戶統一管理
- 拜訪記錄：語音/文字 → Claude 淬煉 → 自動存檔
- 報價 + 估價單：對話輸入 → 自動帶入客戶資料 → PDF
- 訂單流程追蹤：下單 → 通知農會 → 生產 → 出貨 → 簽收
- 產品開發管線：概念 → 海大開發 → 試產 → 量產
- 自動化標籤設計：LINE 傳 Logo → 出 3 款 → 選定 → 下包裝單

### 包裝設計引擎
三款外盒 × 九種內層搭配 = 27 個模板。外盒庫存品，內層接單客製。
- 初期用 Python Pillow（免費）
- 訂單穩定後切 Canva API
- 切換只改 engine_config.json 一行

### 三 Bot 架構
```
同一台 Render
├── /webhook/boss      → 老闆 Bot（全功能控制台）
├── /webhook/customer  → 客戶 Bot（詢價/下單/客服）
└── /webhook/vendor    → 廠商 Bot（接單/回報/查詢）
```

### 金流：LINE Pay (~2.0~2.75%) 或 綠界 ECPay (~2.75%)

### 排程
- 每日 08:00 待跟進客戶提醒
- 每日 09:00 訂單狀態掃描
- 每週一 08:00 到期報價單提醒
- 超過 30 天未聯繫自動推送跟進

---

## ㊅ 系統 2 — IOT 農會加速器 + 公司會計

**IOT 不是工廠系統，是打開農會大門的敲門磚。**

### 部署資訊
| 項目 | 內容 |
|------|------|
| Render URL | https://iot-automation-s47u.onrender.com |
| Render 方案 | ⚠️ Free Tier（靠 UptimeRobot 維持不休眠，考慮升級付費） |
| 儀表板 | /dashboard |
| 溯源頁 | /trace/B-XXX |
| 品牌官網 | / （五區塊：Hero/Technology/ESG/Product/CTA） |
| GitHub | alexchung-lm/iot-automation |
| LINE Bot | IoT系統 @731qpzdr |
| UptimeRobot | 每 5 分鐘 ping /ping（⚠️ 關鍵：Free Tier 必須保留） |
| 統計 | 57 Agent ・ 45 工作表 ・ 17 排程 ・ 25+ Line Bot 指令 |

### Google Drive 資料夾
| 用途 | Folder ID |
|------|-----------|
| 草莓酒-單據 | 1HhV5_jI6CP0iTby9WfcWfkDvTbkq8eB3 |
| 草莓酒-QRCode | 1p-psA_KPCdus0qRjTG-gd2K77zfndONK |
| 草莓酒-備份 | 1kVF2MJ6VPfk47BIbsZoanKjA1Z5-kGza |

### IOT 模組
- 溫濕度/發酵 IOT 監控、生產數據自動記錄、農會合作管理
- 產能追蹤+排程、海大學術計畫對接、品質驗收 (QC)、批次溯源

### 公司會計模組
- 公司對帳+應收應付、進銷存管理、會計報表、PDF 單據
- 升級路線：簡單對帳 → 進銷存 → 財務報表 → 完整會計系統

### 完整事件清單（system_events）
```
order_created / order_confirmed / order_paid / order_shipped
stock_low / purchase_made / production_needed / production_done
payment_confirmed / payment_overdue / iot_alert
license_expiring / food_safety_fail / email_order_received
```

### 排程
- 每小時：IOT 數據讀取
- 每 10 分鐘：庫存掃描 / 採購通知
- 07:00 灑水 / 08:00 營運摘要 / 08:15 生產排程
- 09:00 財務規則 / 09:05 財務報表
- 每 30 分鐘：系統健康檢查
- 每日 02:00：自動備份 45 張工作表

### 硬體規劃（Raspberry Pi）
- Pi 4B 4GB + DS18B20 溫度感測器 + 單通道繼電器 + 風扇
- 兩層架構：local_safety.py（本地安全）+ data_push.py（雲端 /api/sensor）

---

## ㊆ 系統 3 — 網路行銷系統（品牌放大+情報）

**跨系統匯流點：從 Sheet A/B/D 讀取數據，不寫入其他系統。**

### 25 個 Agent（6 模組群）
```
A. 官網+詢價漏斗（4）：core_website / input_inquiry / rules_inquiry / output_inquiry_notify
B. SEO+內容行銷（4）：input_seo_rank / input_traffic / rules_content / output_content_draft
C. 微網紅合作（5）：input_kol_scout / input_kol_collab / input_kol_metrics / rules_kol_roi / output_kol_report
D. 競品情報（4）：input_competitor / input_comp_monitor / rules_comp_alert / output_comp_notify
E. 社群管理+留言回覆（5）：input_social_metrics / input_social_comment / rules_social_plan / output_social_post / output_social_reply
F. 匯流儀表板（3）：input_dashboard_sync / rules_dashboard / output_dashboard
```

### 社群留言半自動回覆
```
新留言（IG/FB）→ 每10分鐘掃描 → Claude 產生3種回覆（幽默/溫暖/導購）
→ LINE 推播給你選 → 你點選後才發出 → 對 Meta 算人工回覆
```

### 品牌人設 prompt
```
個性：懂農業、幽默但不油膩、親切像鄰居
回覆長度：一句話為主，不超過兩句
禁止：政治、爭議話題、攻擊競品
客訴：不幽默，改成溫暖道歉+私訊處理
```

---

## ㊇ 系統 4 — 秘書記帳系統（個人財務）

**純個人系統，不包含任何公司帳務。永遠輕量。**

### 部署資訊
| 項目 | 內容 |
|------|------|
| GitHub | alexchung-lm/family-bot（Private） |
| Render URL | https://family-bot-r7sg.onrender.com |
| Render 方案 | ✅ 付費版（不會休眠） |
| UptimeRobot | 每 5 分鐘 ping /ping（付費版不需 keep-alive，但保留做 uptime 監控） |
| Google Cloud Project | iot-system-490808 |

### 功能
- 文字記帳（「午餐 120」）/ 圖片辨識（發票/名片/帳單截圖）
- 行事曆 / 旅遊規劃 / 聯絡人 / Gmail 掃描 / 對帳
- 排程：行事曆提醒每5分 / Gmail每15分 / 月報每月底21:00

### 排程架構（v5.1 修復）
- 啟動方式：`python app.py` 單進程（非 gunicorn，避免多 worker 排程重複）
- 防重複：`_scheduler_started` flag
- Keep-alive：`/ping` endpoint 回傳 `pong`

### ⚠️ 環境變數注意
- ADMIN_LINE_USER_ID：✅ 已設定（U4bc068298873ad38a6f8a31d9b2bd8f2）
- Gmail Refresh Token：測試階段可能 7 天過期

---

## ㊇-2 系統 5 — TMO Leverage Model（生技情報）

**Partner 的業務情報中心，跟 ArgiNex 完全獨立。**

### 部署資訊
| 項目 | 內容 |
|------|------|
| LINE Bot | LM情報助理 @997qsojr |
| Render URL | https://leverage-model-bot.onrender.com |
| GitHub | alexchung-lm/leverage-model-bot（main） |
| Service Account | leverage-model-bot@leverage-model.iam.gserviceaccount.com |
| Google Sheet ID | 1nN4Wol_tLA--bZdBt0xnKq-lgW7HbKumcmGU8EmKGic |

### 現有模組
| 模組 | 功能 | 狀態 |
|------|------|------|
| PCC 決標爬蟲 | 爬政府採購網決標公告 | 已建 |
| GRB 研究計畫 | 爬政府研究計畫補助 | 已建 |
| 人物搜尋 | Google 搜教授/官員公開資訊 | 已建 |

### 待辦（暫停，先做 ArgiNex）
1. ✅ LINE Bot Messaging API 開通
2. [ ] Google Sheet 升級 Service Account 讀寫
3. [ ] 重建 8 node tabs（Apps Script）
4. [ ] 升級 app.py 多 tab 連結查詢 + Claude Haiku 意圖解析
5. [ ] 完成 save_visit() 寫入功能
6. [ ] 語音轉文字 Whisper/Gemini
7. [ ] Claude 自動摘要拜訪重點
8. [ ] 超過 30 天未拜訪自動提醒
9. [ ] 最小摩擦業務回覆（好/等/成）
10. [ ] 外部信號自動充實（標案/補助到期/競品動態）

---

## ㊈ 工作流程 SOP

### 🔴 20 行規則 — Chat 每次動手前的唯一判斷標準

**我（Chat）即將生成的 code 超過 20 行嗎？**

```
YES → 交給 claude -p（Code 來寫，Chat 只翻譯指令，上下文不爆）
NO  → mac-local MCP 直接做（Chat 自己處理，快速完成）
```

| 動作 | Chat 生成多少 code？ | 誰做？ |
|------|---------------------|--------|
| 讀任何檔案 | 0 行 | ✅ Chat + mac-local |
| git push / shell 指令 | 0 行 | ✅ Chat + mac-local |
| 看網頁驗收 | 0 行 | ✅ Chat + Chrome MCP |
| 改 config 一兩行 | 2-3 行 | ✅ Chat + mac-local |
| 修 bug（改幾行） | 5-15 行 | ✅ Chat + mac-local |
| 加一個小 function | 10-20 行 | ✅ Chat + mac-local（剛好在線上） |
| **新建一個 Agent 檔案** | **50-300 行** | ⛔ **claude -p** |
| **重寫 app.py 的一大段** | **100+ 行** | ⛔ **claude -p** |
| **建 core_database.py** | **200+ 行** | ⛔ **claude -p** |

**為什麼這是最重要的規則？**
Chat 用 mac-local 寫一個 200 行檔案 → 這 200 行出現在對話裡 → 上下文爆滿 → 策略討論被擠出去。
Chat 用 claude -p 寫同一個檔案 → Chat 只產出 10 行指令 → Code 在自己的 context 生成 200 行 → 上下文完好。
**同樣的結果，差 190 行的上下文消耗。**

### 🔴 Anti-Continue 規則 — Chat 回覆必須精簡

**Chat 的回覆觸發 Continue 按鈕 = 流程中斷 = Alex 被迫手動介入。**

防止 Continue 的三條規則：
1. **超過 20 行 code → claude -p**（已解決，見上方 20 行規則）
2. **多步驟操作 → 壓縮成單一 shell 指令**（一次 MCP 呼叫完成，不要拆成多次）
3. **回覆先結論後展開**（Alex 沒問就不展開長篇解釋，省上下文也避免 Continue）

```
❌ 錯誤：push 四個 repo 分三次呼叫 + 三段解釋 → 觸發 Continue
✅ 正確：for repo in a b c; do git push; done → 一次搞定 → 不觸發
```

### 🔴 Chat = 翻譯官（不能改的根本前提）

**Alex 是商業架構師，不是工程師。**

Alex 的語言是「我需要管三種客戶」，不是「建 customers 工作表用 gspread，append_row 收兩個參數」。
Chat 的核心價值 = 把商業語言翻譯成精準的技術指令，再交給 Claude Code 執行。
沒有 Chat 翻譯 → Claude Code 只能猜 → 產出不符合 COMPANY_MASTER 的架構。
Cowork / Dispatch / Computer Use 預設使用者能下精準技術指令 → 不適用 Alex 的工作模式。

**2026-03-31 實測結論：** 花了一整天測試 Dispatch、Computer Use、遠端桌面、手機遙控，
結論是沒有任何方案比 Chat + MCP + claude -p 更好。

### ⭐ 架構全貌（v5.4 定案）

```
┌─────────────────────────────────────────────────┐
│  Chat（大腦 + 翻譯官）                             │
│  ・把 Alex 的商業語言翻譯成精準技術指令              │
│  ・戰略討論、架構決策、驗收結果                      │
│  ・⛔ 超過 20 行 code → 交給 claude -p             │
│  ・所有對談都先經過 Chat，由 Chat 發號施令            │
│                                                   │
│  Chat 的兩隻手：                                   │
│  ├── mac-local MCP → ≤20 行的小事直接做             │
│  └── claude -p → >20 行的大事交給 Code 寫           │
│                                                   │
│  Chat 的眼睛：                                     │
│  ├── Chrome MCP → 看網頁、測 API（自動，省 token）   │
│  └── Alex 丟截圖 → Chat 帶脈絡判斷（手動補位）      │
└─────────────────────────────────────────────────┘
```

### 🔧 claude -p 橋（v5.3 發現，2026-03-31 測試成功）

Chat 透過 mac-local MCP 呼叫 `claude -p` 直接指揮 Claude Code 寫程式。
Alex 不需要手動切 tab 複製貼上。

```
Chat 討論完架構 → 翻譯成精準技術指令
  → mac-local 執行：cd ~/repo && claude -p "指令" --allowedTools "Read,Write,Bash"
  → Code 寫程式 → Chat 用 mac-local 讀結果驗收 → Chat 用 Chrome 看網頁驗收
```

```bash
# 技術細節
/opt/homebrew/bin/claude (v2.1.81)
--allowedTools "Read,Write,Bash"   # 授權讀寫 + 跑指令
--allowedTools "Read,Write"        # 只授權讀寫（更安全）
# 每次呼叫獨立 session，指令必須精準（Chat 的翻譯工作很重要）
# 大型任務 timeout 設 300 秒
```

### 標準工作流程
```
步驟 1：Chat 討論架構和策略（只文字，⛔ 超過 20 行 code 就交 claude -p）
步驟 2a（≤20行）：Chat 透過 mac-local MCP 直接寫檔案 / git push
步驟 2b（>20行）：Chat 透過 claude -p 指揮 Code 寫整個模組
步驟 3：Chat 透過 Chrome MCP + mac-local 驗收結果
步驟 4：Chat 更新 COMPANY_MASTER.md → push 四個 repo
```

### 每次開新對話的 SOP
```
你：「去桌面讀 COMPANY_MASTER.md，我們繼續」
Claude：透過 MCP 讀取 → 掌握全局 → 開工
做完：Claude 透過 MCP 更新 COMPANY_MASTER.md → push 四個 repo
```

### 出門在外的正確做法
```
桌前（出門前）：跟 Chat 討論策略、確認 MD 內容
出門中：手機開 Chat 對話 → 繼續討論 MD 修訂（純文字，不需要 MCP）
回桌前：「照我們討論的更新 MD 並執行」→ MCP + claude -p 一次搞定
```

**思考不需要工具，執行才需要。**

### MCP 連線確認（桌前 Checklist）
```
□ Claude Desktop app 開著
□ Chrome 開著 + Claude in Chrome 擴充功能藍色開關
□ Mac 不休眠（已設定 sleep 0）
□ 在 Chat 打「測試 MCP」→ 兩個 ✅ 就代表正常
```

設定檔：`~/Library/Application Support/Claude/claude_desktop_config.json`
Server：`~/.mcp/mac_mcp_server.py`
Claude Code CLI：`/opt/homebrew/bin/claude`（v2.1.81）

### ⛔ 已測試並排除的替代方案（2026-03-31）
| 方案 | 為什麼不用 |
|------|-----------|
| Dispatch | 大腦和手混在同一 thread → 上下文秒爆 |
| Computer Use 取代 Chat | 沒有商業脈絡 → 等於讓新人做決策 |
| 手機開同一對話操作 MCP | MCP 綁 Claude Desktop → 手機端無 MCP |
| 遠端桌面 | 手機螢幕太小，操作桌面 GUI 體驗差 |
| Chat → Cowork MCP | Cowork 沒有 CLI 或 API，無法程式化呼叫 |
| `claude -p --chrome` | Code 自己驗收 = 沒有商業脈絡的 QC，不如 Chat 驗收 |

### 雙眼策略
| 工具 | 場景 | 優點 | 缺點 |
|------|------|------|------|
| Claude in Chrome | 看網頁、測 API | 快、省 token | 只看瀏覽器、會斷線 |
| Computer Use | 多應用、操作桌面 app | 看全貌 | Token 消耗大、Research Preview |
| Alex 截圖 | 看螢幕上的任何東西 | 最靈活、Chat 帶脈絡判斷 | 手動 |

---

## ㊉ 待辦清單

### 系統 2（IOT）— 現有待辦
- [ ] /dashboard 加密碼保護（品牌官網 / 維持公開）
- [ ] 官網加 IG/FB 社群連結
- [ ] 提交 Google Search Console
- [ ] 儀表板鑽取/搜尋面板
- [ ] Line Bot 搜尋指令
- [ ] PDF 單據系統（報價單/出貨單/收據）
- [ ] QR Code 溯源系統
- [ ] Canva Pro 整合（output_canva.py）
- [ ] Raspberry Pi 硬體採購與設定
- [ ] ⚠️ 評估是否升級 Render 付費版（57 Agent + 17 排程，Free Tier 有風險）

### 系統 2（IOT）— 複式簿記 + 會計自動化（v5.5 新增，~20hr）
- [ ] chart_of_accounts 工作表 + input_chart.py（會計科目表）
- [ ] journal_entries 工作表 + input_journal.py（事件→複式分錄自動翻譯）
- [ ] account_balances 工作表 + rules_accounting.py（每月結帳+科目餘額+借貸平衡）
- [ ] output_statements.py（損益表 / 資產負債表 / 現金流量表 + PDF 輸出）
- [ ] LINE Bot 會計指令（「損益表」「資產負債表」「現金流」「應收明細」「逾期30天」）
- [ ] input_vendor_email.py（Gmail 掃描廠商請款/報價/發票 → Claude Haiku 辨識 → 自動建分錄 → LINE 推播確認）
- [ ] output_tax_report.py（台灣營業稅/營所稅格式，以後再做）

### 系統 1（ArgiNex 業務）待辦
- [x] arginex-business repo 已建立 + Render 部署完成
- [ ] core_database.py + app.py 骨架
- [ ] 8 個節點 worksheet 建立
- [ ] 三 Bot 架構實作（老闆/客戶/廠商）
- [ ] 金流串接（LINE Pay 或綠界）

### 系統 1（ArgiNex）— 標籤自動化引擎（v5.5 新增）
- [x] Gemini 生成酒標模板 + 意象圖（label_A.png, showcase_A.png）
- [x] Banana Pro 生成公版意象圖（3D 瓶身情境）驗證成功
- [x] label_engine.py — Pillow 替換引擎（合併模板 + 行楷字體 + Logo 置中）
- [x] Gemini API 串接 — gemini-2.5-flash-image 示意圖自動生成（gemini_showcase.py）
- [x] LINE Bot 標籤流程 MVP（客戶傳公司名 → 傳 Logo → 自動生成酒標 → 回傳預覽 → 確認/重做）
- [ ] 印刷輸出（PDF 刀模檔，送印刷廠）

### 系統 3（行銷）待辦
- [ ] 開 FB/IG 商業帳號
- [ ] 申請 Meta Graph API
- [ ] 建 output_social.py（FB/IG/Threads 自動化）
- [ ] 建 knowledge_base 系統（Google Drive Word → AI 客服）
- [ ] 25 個 Agent 逐步開發

### 系統 4（記帳）待辦
- [x] 排程修復（v5.1：改 python 單進程 + /ping + _scheduler_started）
- [x] HSBC 角括號修復（input_gmail.py regex 預解析）
- [x] UptimeRobot 監控（每 5 分鐘 ping）
- [x] Gmail 重複記帳修復（v5.5：processed_ids 即時更新）
- [x] rules_audit.py 資料品質巡檢（金額/欄位/日期/重複，每日 22:00 自動排程 + LINE 推播）
- [ ] 多幣別記帳（日幣/美金）

### 系統 5（TMO Leverage Model）待辦
- 🔄 全部暫停，先做 ArgiNex（GitHub Actions 已 disabled）

### 未來規劃 — 自動列印
- [ ] 評估辦公室印表機型號（需支援 Wi-Fi + CUPS/API）
- [ ] macOS lp 指令列印（出貨單/報價單 PDF → 直接印）
- [ ] 標籤專用印表機評估（Brother QL / Zebra，量大後再買）
- [ ] 自動寄 Email 給印刷廠（量產酒標）

### 其他
- [ ] 收集 NTOU 產品文件
- [ ] Ziwei 網站已部署於 /ziwei（朋友的紫微斗數）

---

## ㊊ 技術備忘

### 部署模式
| 系統 | Render 方案 | 啟動方式 | Keep-alive |
|------|------------|---------|------------|
| S1 ArgiNex 業務 | ✅ Free Tier（srv-d76dsdh4tr6s738pnlog） | python app.py | UptimeRobot /ping |
| S5 TMO Leverage | Free Tier | — | UptimeRobot（需要時再加） |
| S2 IOT | ⚠️ Free Tier | python app.py | UptimeRobot /ping（必須） |
| S4 記帳 | ✅ 付費版 | python app.py | UptimeRobot /ping（選用，做監控） |

- GitHub push → Render 自動部署
- 系統驗證：`python3 system_check.py` + regex scan + py_compile

### claude -p 橋技術細節
```bash
# 基本用法：Chat 透過 mac-local 呼叫
cd ~/目標repo && claude -p "精準技術指令" --allowedTools "Read,Write,Bash"

# 常用參數
--allowedTools "Read,Write,Bash"   # 授權讀寫檔案 + 跑指令
--allowedTools "Read,Write"        # 只授權讀寫，不跑指令（更安全）
--allowedTools "Read"              # 只讀，用於查詢

# CLI 位置
/opt/homebrew/bin/claude (v2.1.81)

# 注意
- 每次呼叫是獨立 session，不會記住之前的對話
- 指令要足夠精準（Chat 的翻譯工作很重要）
- 大型任務建議加 timeout：mac-local timeout 設 300 秒
```

### Render 排程注意事項
- Free Tier 15 分鐘無外部 HTTP 請求就休眠，排程全部停止
- APScheduler 是 app 進程的一部分，app 休眠 = 排程死
- UptimeRobot 每 5 分鐘 ping /ping → 維持不休眠
- 付費版不會休眠，排程穩定
- 啟動方式必須用 `python app.py`（單進程），不用 gunicorn（多 worker 會排程重複）

### 關鍵 API 模式
- `core_database.py`：`append_row(sheet_name, data_dict)` 只收 2 參數
- `get_worksheet(sheet_name).get_all_records()` 讀取數據
- `send_line_push(user_id, message)` 推播通知
- Google Sheet 建工作表：每個 `add_worksheet` 之間 `time.sleep(2)`
- 大檔案傳輸：寫 Python 生成腳本 → mac-local:write_file → run_command

### Git 操作
- 正常 push：`git add . && git commit -m "msg" && git push origin main`
- 衝突解決：`git pull --rebase origin main && git push origin main`

### LINE 短網址（lin.ee）
- 桌面需 QR modal（Google Charts API）
- 手機直接開 LINE app

### 歷史錯誤教訓（29 條）
架構類：公司帳歸錯系統 / IOT 定位錯誤 / 農會風險誤判 / 盤商節點太窄
爬蟲類：政府採購反爬 / g0v 網域變更 / JSON 當 HTML 解 / data.gov.tw 無即時 API
部署類：Render Port / LINE Token I/l / ADMIN_LINE_USER_ID / API Key 額度 / Model 名稱
程式類：append_row 參數數 / GitHub Actions 路徑 / requirements.txt / config.json 路徑 / markdown fences / HSBC 角括號被當 HTML 刪除
流程類：Chrome 燒 token / Chrome 斷線 / 上下文爆滿
**v5.1：** gunicorn 多 worker 殺排程 → 改 python app.py 單進程
**v5.2：** Dispatch/Computer Use/遠端桌面 全部不適用本架構
**v5.3 新增（2026-03-31）：**
- 以為 Chat 無法連線 Claude Code → 實測 `claude -p` 完全可行（差點錯過最重要的橋）
- Cowork 沒有 CLI → Chat 無法程式化呼叫 Cowork（這是真的做不到）
- `--chrome` 讓 Code 自己驗收 → 不如 Chat 驗收（Code 沒有商業脈絡）

### MCP 連線注意事項
- mac-local：由 Claude Desktop app 管理，app 開著就不會斷
- Claude in Chrome：Chrome 擴充功能，Chrome 閒置太久會斷線
- MCP 綁 Claude Desktop app → 手機端無法使用 MCP
- 斷線恢復：回桌面重新整理 Claude Desktop 的對話頁面

### 資料庫升級路線
```
現在：Google Sheet（4 張獨立試算表）
第二階段：Supabase（資料量超過 500 筆時）
第三階段：Neo4j（需要知識圖譜推理時）
```

---

**5 系統 ・ 5 試算表 ・ 21+ 節點 ・ 73 已建 Agent ・ 103+ 目標 ・ 4 Repo 同步**
