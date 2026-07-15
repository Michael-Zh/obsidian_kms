---
author:
  - "[[Gary Chen]]"
source: YT
url: https://www.youtube.com/watch?v=eKW9ITaltWw&list=PLYQATQ-FupFzf7ApyP8KURMTtn2MhAok-&index=6
saved: 2026-06-17T01:02:53+02:00
tags:
  - YT
published: 2026-05-04
description: 加入我的 Patreon，查看完整文章還有提示詞模板：https://www.patreon.com/posts/157335306--史丹佛兩小時的「Beyond LLM」課程，我用一支影片把核心整理給你。從 base model 的限制講起，一路到 Prompt Engineering、Fine-Tuning、RAG、Agentic Workflow 與 Multi-Agent，把 AI
id: 一部影片看完 Stanford AI 系統課程，從 LLM 到 Agentic Workflow
annotation: full article
summary: "Comprehensive overview of the LLM augmentation stack: vertical axis from raw LLM to multi-agent systems (Prompt Engineering → Fine-Tuning → RAG → Agentic Workflow → Multi-Agent), with detailed discussion of Centaur vs Cyborg AI usage patterns, the Jagged Frontier (uneven AI capability across tasks), BCG consulting experiment results, and practical guidance on when each tier applies."
---
![](https://www.youtube.com/watch?v=eKW9ITaltWw)

加入我的 Patreon，查看完整文章還有提示詞模板：https://www.patreon.com/posts/157335306  
\--  
史丹佛兩小時的「Beyond LLM」課程，我用一支影片把核心整理給你。從 base model 的限制講起，一路到 Prompt Engineering、Fine-Tuning、RAG、Agentic Workflow 與 Multi-Agent，把 AI Builder 該懂的技術地圖一次攤開。看完你會知道每個技術解什麼痛點、什麼時候該用，下一步該往哪走。  
  
📌 時間戳  
0:00 開場：AI Builder 學習困境  
0:50 LLM 的限制與縱軸思維  
3:30 強化單一 LLM 的三大工具  
11:40 Agentic Workflow 系統設計  
17:30 評估系統與客服 Agent 實作  
22:15 Multi-Agent 與學習路線總結  
  
📢 追蹤我的頻道  
👍 覺得有幫助請按讚、訂閱、開小鈴鐺！  
  
史丹佛課程原始影片：https://youtu.be/k1njvbBmfsw?si=qhDgQ-W\_CrDE1k0H  
  
#AI #AIBuilder #Stanford #LLM #AIAgent

## Transcript

### 開場：AI Builder 學習困境

**0:00** · 如果你有在關注 AI 這一兩年最炙手可熱的工作 一定是 AI Engineer，AI Builder 大型語言模型越強，這群人越吃香 他們有能力幫公司打造內部工具 優化運營流程 也已經有一堆人自己動手把想法做成產品 成立了自己的公司 而這種人，現在每間公司都在搶 想學 AI 的人很多 但大多數人都不知道從哪裡下手 市面上的資源不是太破碎，就是太過艱澀

**0:24** · 看完還是不知道自己學到了什麼 或者下一步該往哪走 史丹佛大學有一堂課叫做 Beyond LLM 我認為這是目前最接近那個答案的東西 從大型語言模型的本質講起 一路帶到 Prompt Engineering RAG，Fine-Tuning Agentic Workflow 還有 Multi-Agent 的框架 這堂課時長兩小時 今天我就用一支影片的時間把核心整理給你 你看完之後 會對 AI 在商業領域上的應用有一套完整的認知框架

### LLM 的限制與縱軸思維

**0:51** · 知道這些技術怎麼組合在一起 也能規劃自己接下來的學習路線 那我們廢話不多說，直接開始 首先我們要先知道大型語言模型的限制是什麼 LLM 要變強有兩條路 第一條是橫軸 就是換更強的 base model 比方說從 GPT-4 升級到 GPT-5 但橫軸是 OpenAI 跟 Anthropic 在做的 一般人沒有那個能力 也沒有那個金錢去訓練自己的大型語言模型

**1:18** · 你能施力的地方是縱軸 也就是在現有的 LLM 上面疊各種工程技術 又叫做 Augmenting LLM 也就是想辦法提升這些 base model 的能力 而這整堂課，包括這支影片 講的都是縱軸的事情 如果你只會使用 base model 在商業場景上一定會撞牆 舉個例子，ChatGPT 剛出來的時候 沒有連網功能，沒辦法調用工具 充其量就是一個很聰明的問答機器人 沒辦法實際幫你做完一件事 Stanford 的教授整理了 base model 幾個常見的限制

**1:49** · 第一是缺乏 domain knowledge 比方說有一組學生在做自動化農業設備 要用相機判斷作物有沒有生病 這種農業病害的 dataset 市面上根本找不到 換句話說你的公司資料，內部文件，產品規格 base model 都不知道 它也沒辦法根據這些資料幫你解決問題 第二是資訊落後 模型不可能每幾個月重訓一次 新詞，新事件，新公司它通通不認識

**2:14** · 年輕人在用的網路流行用語 模型大多也聽不懂 第三個，控制很難 LLM 是機率性輸出 同樣的 prompt 兩次跑可能結果不一樣 在 ChatGPT 上聊天當然 OK 但你想想 production 環境 使用者問退費 AI 一下說可以一下說不行，公司就麻煩了 教授說，就連 OpenAI 跟 xAI 這種資金最多

**2:36** · 人才最齊的團隊 都還沒辦法把 LLM 完全控制好 更何況一般公司 第四個，當 context 太長 模型的表現會顯著退步 現在主流模型的 context window 已經拉到 100 萬 token 差不多十幾本書的長度 但在這麼大的 context 裡 還是會出現 lost in the middle 的現象 簡單講 你把一個 Gary 午餐吃了一顆蘋果這樣的小細節

**2:57** · 藏進公司過去一年的會議記錄裡 再問模型 Gary 午餐吃了什麼 雖然這個狀況現在已經顯著改善 但 LLM 有時候還是會答不出來 想做 AI 產品 光換更強的 base model 不夠 你需要在縱軸上施力 接下來這支影片的前半段會告訴你

**3:15** · 強化單一 LLM 的三個工具和觀念 也就是 Prompt Engineering Fine-Tuning，還有 RAG 影片後半段會進到系統設計 介紹 Agentic Workflow 跟 evaluation 評估方法 然後用一個客服 agent 的 case study 把這些東西串起來 最後也會帶到很多人感興趣的 Multi-Agent 那我們直接從 Prompt Engineering 開始講 Stanford 的教授說他不認為 prompt engineer 會是一個職業 因為提示詞工程應該是每個工程師都該會的基本技能

### 強化單一 LLM 的三大工具

**3:42** · 你不會靠 prompt engineering 當飯吃 但這個技能會讓你在職涯裡用一輩子 就像九九乘法表一樣是基本功 我之前有做過一部影片 專門在講 prompt engineering 有興趣的朋友可以去看看 關於 prompt engineering 有一個很有意思的研究我想分享給你 頂級管理顧問公司 BCG 做過一個實驗

**4:00** · 他們把一群顧問分成三組 第一組沒有 AI 第二組可以使用 ChatGPT 第三組則是可以使用 ChatGPT 以外 還有接受撰寫提示詞的訓練 最後研究的結果發現三件事 第一個叫 The Jagged Frontier，鋸齒邊界 意思是 AI 不是在所有任務上都表現得好

**4:19** · 有些任務搭配 AI 顯著加分 但有些任務 AI 反而扯後腿 第二個發現叫 Falling asleep at the wheel 翻成中文就是在方向盤前打瞌睡 當你不知道任務剛好是 AI 不擅長的 卻太信任它把產出直接送出 結果比沒用 AI 還慘 也就是說，你要知道 AI 的邊界在哪

**4:39** · 才不會在它弱的地方踩雷 第三個現象最有趣 他們發現使用 AI 的方式分成兩種 分別是 Centaurs 跟 Cyborgs Centaur 是半人馬，也就是分工委派型 丟一個長 prompt 給 AI 叫它做整份簡報 自己去做別的事 Cyborg 是生化人，是高頻來回型 跟模型一句一句對話協作 Stanford 的教授說 學生的使用習慣會比較像 cyborg 而企業在自動化 workflow 時比較像 centaur 那你應該用哪一種？

**5:06** · 關鍵是看任務性質 重複性高，流程清楚的任務 用 centaur 模式委派出去就好 需要判斷，需要創意，需要來回校正的任務 cyborg 模式才能逼出 AI 的最佳輸出

**5:21** · 兩者沒有好壞之分，實務上兩種都會用 重點是要有意識地切換 接著進到實作 通常一個好 prompt 要有三個東西 給誰看，產出格式，重點是什麼 請幫我總結這篇文章是一個很爛的提示詞 因為什麼資訊都沒給 但如果你寫的是請將這份再生能源論文 整理成 5 個重點摘要 並且聚焦在其背後的政策意涵上

**5:45** · 模型立刻知道對象是政策制定者 長度是 5 個點，重點放在政策意涵上 你的產出品質會立刻提升 但教授說，prompt engineering 裡最常用 最重要的一個技巧不是這些，是 Prompt Chaining 注意，chaining 跟 Chain of Thought 不一樣 Chain of Thought 是叫模型 step by step 思考 Chaining 則是把一個複雜的 prompt 拆成多個獨立的 prompt 前一個的 output 餵給下一個 有用過 n8n 的朋友應該知道我在說什麼 舉個例。

**6:14** · 你要做客戶投訴回信 單一 prompt 寫法是讀這封投訴信 寫一封專業的回應 這就是一個黑盒子 最後的產出如果有問題 你也不會知道該調整哪裡 但如果使用 prompt chaining 拆成三個 prompt 第一個抽出客戶在抱怨什麼 第二個用抽出來的問題起草大綱 第三個用大綱寫完整回信 每一步都可以獨立測試，獨立 debug Chaining 不只讓模型表現更好 也讓你得到 observability 能觀察 LLM 在做什麼，哪個流程出了問題

**6:47** · 講完 Prompt Engineering，下一個是 Fine-Tuning Stanford 教授對 fine-tuning 的立場很簡單 能不做就不做，原因有四個 第一，要大量的優質數據 如果你想要自己 fine-tune 模型 就要有大量高品質的，標注好的資料 要做到這件事情的成本對一般人來說太高了

**7:06** · 第二，容易 overfit 模型容易在你那個特定任務上變很強 但通用問題反而答不出來 就會失去 base model 原本的廣度 第三，時效性差，這應該是最傷的點 你花兩個月 fine-tune 完一個模型上線 下個月新一代 base model 就出來 直接打贏你 fine-tune 的版本 第四，通常用 prompt engineering 也可以達到一樣的效果

**7:29** · 而且成本低很多 你想換新 base model 原本的 prompt 大多都是 portable 的 但 fine-tuning 的模型不行 當然，針對少數情境 fine-tune 還是值得做的 比方說法律，科學那種需要重複高精度輸出的領域 或者 base model 在某個 domain 上表現吃力 這些情況下，fine-tune 都會有幫助 但對大多數的人來說 其實不會有太大的效益 所以，如果你想要把特定的 domain knowledge 塞進模型 單純的提示詞工程可能塞不下 fine-tuning 的成本效益又對不起來 那實作端應該怎麼辦呢？

**8:02** · Stanford 教授給出的答案是 RAG RAG 是 AI 工程師面試最常考的題目之一 面試官常常會請你用 5 歲小孩聽得懂的方式解釋什麼是 RAG 你做 AI Builder 也好，做 AI 工程師也好 這個是你一定要知道的事情 RAG 解的痛點有幾個 context window 太小，長 context 抓不準 資訊有時效性，或者模型會產生幻覺 RAG 的做法很單純 我用藥物副作用這個需要高度準確的醫療場景來說明

**8:31** · 通常 RAG 的做法是這樣的 先把所有的資料，文件用 embedding 模型 把這些資訊轉成向量，存進向量資料庫 英文叫做 vector database 所謂向量，就是把一段文字的語意轉換成一串數字 語意相近的文字 轉出來的數字陣列在數學空間裡距離也會比較近

**8:50** · 所以當使用者問藥物 A 的副作用 我們不是在做關鍵字比對 而是在找語意最接近的文件片段 就算文件裡寫的是不良反應而不是副作用 一樣能找到 使用者的問題也用同個 embedding 模型轉成向量 再用距離 metric 從 vector database 裡 找出最相近的 documents 最後把這些 documents 加上 system prompt 加上 user query，組合成餵給 LLM 的最終 prompt

**9:16** · Prompt template 大概長這樣 根據以下 documents 回答使用者的問題 如果 documents 裡沒有答案，就說『我不知道』 這樣設計是為了把模型鎖在你提供的資料範圍內 避免它自由發揮，憑空捏造 當然，你還可以要求模型回答時附上這個答案來自第幾頁

**9:34** · 第幾章，第幾行加超連結 這樣使用者可以自行回溯資料源進行驗證 但是單純這樣做有時候不夠 比方說一種藥的相關文件可能足足有 50 頁 整份直接轉成向量，那很多細節遺失其中

**9:49** · 所以通常會搭配 chunking 最基本的 chunking 是把文件切成固定大小的片段 每段各自轉成向量 更進階的做法是多層次存儲 同時保留整篇，每章，每段的向量 retrieval 時可以先找到相關的章節 再往下鑽到精確的段落 這樣在大文件裡的命中率會更高 還有一個最近比較多人在討論的話題 有人說，像現在已經有模型支援超長的 context window

**10:14** · 等這個技術成熟，算力夠便宜 base model 直接讀完整個資料庫 RAG 就沒用了 但 Stanford 的教授認為這樣的說法理論上對 實務上錯 因為實際上你還是會遇到很多問題 比方說 Latency，你想想看 每次問問題，模型都要把整個 Google Drive 重讀一次

**10:33** · 沒人等得了 就像搜尋引擎也是靠預先建好的索引來快速定位資料 不可能每次 query 都把整個網路重新爬過一遍 所以 RAG 除了準確度以外 還有檢索效率，可即時更新這類的優勢 而這些優勢在可預見的未來都還是有其存在的價值

**10:50** · 好，到這邊我們講完了影片的第一部分 從 base LLM 的限制出發 我們看了 Prompt Engineering Fine-Tuning 還有 RAG 這三個工具本質上都是在強化單一個 LLM 的能力 但單一個 LLM 再強，還是有它做不到的事 所以接下來進入第二部分 AI 系統設計 我們會講 Agentic Workflow Evaluation 還有 Multi-Agent 這些東西讓你能把 AI 從一個會回答問題的模型 變成一套真正可以運作，實際產出價值的系統

**11:17** · 看到這邊，如果你覺得這支影片對你有幫助 想請你幫我按個讚，點個追蹤 這是我持續創作下去的動力 那我們直接進 Part 2 先講一下 agentic workflow 這個命名 這個詞來自吳恩達 如果你不認識他 吳恩達是 Coursera 的共同創辦人 Google Brain 的創始負責人 前百度首席科學家 是在 AI 領域講話有一定份量的男人 吳恩達用 agentic workflow 這個詞 是因為 AI Agent 已經被用到爛掉了

### Agentic Workflow 系統設計

**11:43** · 有人寫了一個很長的 prompt，叫 agent 有人做了複雜的 multi-agent 系統 也叫 agent 這個詞什麼都能套，反而什麼都說不清楚 所以他用 agentic workflow 來精確描述一件事 把一堆提示詞，外部工具，還有各種元件 組合進一個有結構的工作流程裡，成為一套系統 這就叫做 agentic workflow 還記得我們前面講的 RAG 嗎？

**12:07** · RAG 主要做一件事 給 LLM 外部資料當參考 但 agent 把 RAG 當作工具之一 外加 tool calls，memory，多步驟決策 所以能做到 RAG 單獨做不到的事 舉個例子，使用者說我想退這筆訂單 RAG 只能丟政策文件給你 agent 則是用 RAG retrieve 政策 主動問訂單編號，用 tool 查訂單 確認退費 告訴你 3 到 5 個工作天會處理 RAG 是工具，Agent 是使用 RAG 這個工具的系統

**12:35** · 要打造 agentic workflow 你的工程心態要先翻轉過來 因為傳統 software 跟 agentic AI software 在四個面向都很不一樣 首先是資料 傳統軟體吃結構化資料 JSON，資料庫，表單，格式固定，邊界清楚 Agentic 系統吃的是自由文本 圖片，音訊，沒有固定格式 第二個是邏輯 傳統 software 是 deterministic 同樣的 input，永遠給你同樣的 output

**13:03** · 可預測，可重現 Agentic 系統是 fuzzy 的 意思是同樣的 input 不同時間跑可能給你不同的 output 因為 LLM 本身有隨機性 加上它會根據 context 做判斷 沒有一個固定答案 第三個是架構心態，這個最重要 傳統工程師的思維是寫 microservices 寫 monolith 你精確控制每一步執行路徑 Agentic 系統的思維是 think like a manager 你給 AI 一個目標和限制，讓它自己決定怎麼完成 你管的是方向和邊界，不是每一行程式碼

**13:36** · 第四個是測試 傳統測試是確定性的，跑一百次結果一樣 Agentic 測試是迭代探索式的 因為系統本身是非確定性的 加上它對 context 非常敏感 你沒辦法窮舉所有情況 知道這四件事之後 第一個落地原則就跟著來了 能 deterministic 解的問題，就 deterministic 解 剩下 fuzzy 的部分，加上護欄 教授舉自己的例子 他們做 skills assessment 選擇題，配對題，拖拉題用 deterministic 算分

**14:04** · 因為這些有標準答案，對就是對，錯就是錯 但語音題，語音加 coding 的混合題型 沒有標準答案，沒辦法 deterministic 評分 只能讓 LLM 去判斷 這就是 fuzzy scoring 也就是沒有標準答案的評分 你請 LLM 聽一段語音回答 它要判斷這個人有沒有真的理解這個概念 表達是否清晰，邏輯有沒有跑掉 這些不是對或錯，是一個程度的判斷 LLM 會給你一個分數 但這個分數是它覺得合理的答案，不是算出來的

**14:34** · Fuzzy 的問題是它一定會犯錯 LLM 可能誤判一個正確答案 或是對模稜兩可的回答給出偏低的分數 在考試評分這種高風險的場景，這不可接受 所以他們設計了一個 Appeal feature 受測者可以對 agent 的判分提出申訴 由真人介入審查並糾正 這就是護欄的具體形式 不是試圖讓 AI 零錯誤 而是在它出錯的時候有人接得住 好，原則講完了 要實際打造一個 agent，你需要哪些東西？

**15:02** · 教授用訂機票去巴黎當範例 整理出三個核心要素 第一個是 Prompts 前面講的提示詞工程，在 agent 裡就是這一塊 你怎麼告訴 AI 它的角色是什麼 它能做什麼，不能做什麼 第二個是 Context Management 也就是怎麼管理 agent 在每一個當下看得到的資訊

**15:21** · 這包含幾件事 Memory，對話歷史 也可能有 RAG 撈回來的資料 通通都要塞進有限的 context window 裡 你要決定什麼重要，什麼可以丟，什麼要壓縮 Context Management 本質上只做一件事 那就是把對的資訊在對的時間提供給你的 agent

**15:38** · Memory 本身又分兩層 Working memory 是高頻，要快的 比方說使用者的名字，這次的目的地是巴黎 Archival memory 是低頻，可以慢一點的 比方說使用者過去五年的訂房紀錄 需要的時候再去撈 第三個是 Tools 也就是 agent 能呼叫的外部能力 通常分成兩種 一種是做事的 比方說 Flight Search，Hotel Booking，Payment 一種是查資料的 比方說去 CRM 撈客戶資料 去資料庫查訂單紀錄 另外，課堂上教授把 agent 的自主性分為三層

**16:11** · 最低是 hardcoded steps 步驟全寫死，先識別用戶的意圖 再 lookup history，最後呼叫 API，照順序走 安全，可預測，但很僵硬 遇到預期外的情況就卡住 第二層是 hardcoded tools 但讓 agent 自己決定執行步驟 你給它一組工具，告訴它你是 travel agent 這些是你能用的工具，怎麼用你決定 掌控工具範圍，但給 agent 空間判斷怎麼組合

**16:38** · 這是目前最常見的 production setup 也是教授推薦的起點 第三層是 fully autonomous agent 自己決定步驟，甚至自己創工具 給它 code editor，給它 web search 叫它自己寫 code 解決問題 能力最強，但風險也最高 你沒辦法完全預測它會做什麼 如果 agent 判斷錯誤，自己訂了 100 張機票 你就完蛋了 還有一個關鍵概念是 MCP Model Context Protocol 傳統做法是你要替每一個 API 單獨寫串接邏輯

**17:08** · 教 LLM 這個 API 怎麼用 那個 API 要傳什麼參數 MCP 的做法是在中間放一個協議層 agent 不需要認識每一個 API 它只需要跟 MCP server 溝通 MCP 負責幫它跟後面的服務打交道 你可以把 MCP 想成一個通用插頭 以前每個國家的插座規格不一樣 你要帶一堆轉接頭 有了 MCP，插一個就全通了 Stanford 教授還有提到對 MCP 一個更大的想像

### 評估系統與客服 Agent 實作

**17:33** · 那就是 agent-to-agent communication 你可以把別人做好的 agent 當作一種工具 讓你自己的 agent 去呼叫它 就像現在 agent 呼叫 API 一樣 這是 multi-agent 系統的基礎 我們等一下會講到 不管是單一 agent 還是 multi-agent 上線之前都要先回答同一個問題 怎麼知道它真的有用？

**17:49** · 答案是 eval 也是 production agentic 系統的命脈 教授在課堂上給了一個完整的 eval 框架 是三個維度交叉 第一個維度是 End-to-End 還有 Component-based End-to-end 是看整體 使用者用完給幾分，滿不滿意 Component-based 是拆開每一步看 比方說 這個 tool 老是忘記更新 email 送 email 那一步格式不對 光看整體你知道哪裡壞，但不知道為什麼壞 光看 component 你可能修了細節但整體體驗還是差

**18:20** · 實務上兩個都要做 第二個維度是 Objective 還有 Subjective 也就是客觀和主觀的評價方式 Objective 是可以自動驗證的 使用者說 order ID 是 X LLM 寫進 DB 變成 Y 這種東西你可以寫個 Python script 自動對齊 因為對就是對，錯就是錯 Subjective 是沒有標準答案的 語氣好不好，回答夠不夠有同理心 這種要靠人工評分 或是用另一個額外的 LLM 當作評審 這個等等我會細講 第三個維度是 Quantitative 還有 Qualitative

**18:52** · Quantitative 是數字 改地址成功率幾趴，每個環節的延遲多久 Qualitative 是感覺 在哪裡幻覺，語氣哪裡不對 使用者哪一步卡住 這個要人工一筆一筆看，沒有捷徑 剛剛提到的用 LLM 當作評審 又稱 LLM-as-Judge 這是做 subjective eval 常用的做法 設計上有四種主流玩法 第一種是 Pair-wise comparison 給 judge 兩個答案，問它哪個比較好

**19:20** · 第二種是 Single-answer grading 直接打一到五分 第三種是 Reference-guided pair-wise 多給一個標準答案做對比，讓評分更有依據 第四種是 Rubric-based 你自己定義評分標準 比方說五分等於一百字以內，含三個重點 第一句是 overview 零分等於答非所問，冗長失焦 這四種可以混用 比方說 rubric-based 加上 few-shot examples 讓評審更知道你要什麼 怎麼實際跑一個 subjective eval？

**19:47** · 課堂上教授用 travel agent 的禮貌度評估當例子 共拆成四個步驟 第一步是 error analysis 從一千個使用者裡抽二十個對話，人工讀 你可能就會發現 LLM 講話超短 有點機車，沒同理心 這步不能省，你要先知道問題長什麼樣 才能設計出對的 eval 第二步是設計 eval 用 LLM-as-Judge 加上自己寫的禮貌度 rubric 把你在第一步發現的問題翻譯成評分標準

**20:15** · 第三步是 A/B test 模型 固定 prompt，把底層模型從 GPT 換成 Opus 或者其他模型 然後跑同一批對話，judge 評分 看哪個模型禮貌度最高 第四步是 A-B test prompt 固定模型 把 act like a travel agent 改成 act like a helpful travel agent 看一個詞的差距影響有多大 核心原則只有一個 先人工掃出問題，再設計自動化 eval

**20:41** · 而且模型跟 prompt 這兩個變因一次只動一個 不然不知道是哪個改動造成了差異 講完 eval，教授給了一個完整的 case study 把前面所有東西串起來 題目很簡單 我們要做一個客服 AI agent 使用者可能會說 『我要改 A127 訂單的地址，因為我搬家到建國南路了』 這樣的 AI 客服 agent 你會怎麼做？

**21:02** · 這題目有兩層 表面看是怎麼改地址 本質是怎麼做一個會自己處理客服請求的 agent 課堂上一個學生回答說 我會先去客服旁邊坐一到兩天 看他們實際怎麼處理這種請求 他們日常的工作流是什麼 教授很喜歡這個答案 因為你要先理解人怎麼做這件事 才知道怎麼讓 AI 做 而這就是做 agentic workflow 的第一步 叫做 task decomposition 也就是把大任務拆解成小任務 讓 LLM 可以逐個擊破 觀察之後，你會發現客服處理一個改地址請求

**21:35** · 其實走了五步 第一步，抽出關鍵資訊 包含客戶的 intent 是什麼 order ID 是哪個，新地址是什麼 第二步，去資料庫查客戶紀錄 第三步，查公司政策 像是這筆訂單能不能改地址？是不是已經出貨了？

**21:52** · 第四步，根據前面收集到的資訊起草回信 第五步，送出 email 每一步都明確，這就是 task decomposition 有了拆解，下一步是決定每一步用什麼工具 第一步抽資訊 單純用 LLM 的一次 API 呼叫通常就能解決

**22:08** · 第二步查和改 Database 要 custom tool 或 MCP server 第三步政策檢查，用 RAG 因為政策文件會更新，也需要有效率的檢索 不能讓客戶等太久 第四步是根據前幾步搜集到的資訊 開始撰寫 email 第五步送 email 用 agent 能夠使用的 email 寄送工具

### Multi-Agent 與學習路線總結

**22:28** · 做這些判斷的方式很簡單 先問自己哪些步驟是 fuzzy 哪些是 deterministic 再決定每一步是用 LLM one-shot RAG，tool，還是其他工具 這就是 AI Builder 真實在做的工作 知道每個工具，每種技術的能力和限制 然後炒出一盤你需要的菜 最後是 build evals 把前面講的三個維度全部用上 End-to-end 看最終回覆正確性 語氣，使用者滿意度 Component-based 拆開看每一步 抽資訊的準度，API 錯誤率，政策遵守率

**22:59** · Objective 的部分可以自動驗證 抽出來的 order ID 是否正確 有沒有違反退費政策 Subjective 的部分要靠人工加 LLM-as-Judge 比方說回信是否有禮貌，有沒有同理心 Quantitative 看改地址成功率 latency，退費正確率

**23:17** · Qualitative 看哪裡有幻覺 哪裡語氣不一致 使用者在哪一步感到困惑 到這邊，一個完整的 AI 客服 agent 從零到上線的工程流程就出來了 其實總共就是三個步驟 先把大任務拆解成小任務 再設計工作流程 最後建立評估系統，確保產出穩定

**23:34** · 這堂課的最後一個主題是 Multi-Agent 前面一個 agent 已經能拆步驟 call tool，做 RAG，寫信 看起來夠用了 但 multi-agent 還是有它存在的理由 主要原因是平行處理 有些事沒理由排隊跑 訂機票的時候，找航班，找飯店，查天氣 這三件事完全可以同時進行 如果只有一個 agent，就只能一件一件做 Multi-agent 就是把這幾件可以平行的事 拆給三個 specialized agent 同時跑 速度直接拉起來 次要原因是 reusability，也就是可復用性

**24:07** · 公司裡的 design agent 可以給行銷團隊用 也可以給產品團隊用 不過，multi-agent 聽起來很厲害 但做產品的時候要先問自己真的有需要嗎？

**24:18** · 如果一個 agent 就能解決的任務 硬上 multi-agent 反而增加複雜度 所以還是老話一句，工程設計能簡單就簡單 不要 over design 教授用智慧家庭當 brainstorm 範例 一個完整的智慧家庭 multi-agent 系統可能有溫度控制

**24:33** · 燈光，保全，娛樂，通知 還有能源管理這些 agent 加上一個 Orchestrator 統籌 互動模式有兩種 第一種是 Hierarchical 使用者只跟 orchestrator 講話 由它派工給下面的 agent，指揮鏈清楚 第二種是 Flat agent 之間直接互通，沒有中間人 教授建議智慧家庭以 hierarchical 為主 因為從使用者的角度 你不想同時跟五個 agent 講話 你只想跟一個 assistant 說我要出門了 它就會自己去協調燈光，保全，溫控 但在後台，某些 agent 之間可以有彼此之間水平溝通的連線方式

**25:09** · 比方說溫度控制的 agent 跟能源管理的 agent 直接互通 省掉每次都要過 orchestrator 的溝通成本 當你讓 agent 之間互相溝通 本質上就是 MCP protocol 你把 agent 當作 tool 就跟把 API 當作 tool 一樣 這個心態一旦想通，設計就清楚了 每個 agent 對外暴露一組 tool-like 介面 其他 agent 像呼叫工具一樣呼叫這個 agent 這樣子做結構乾淨，容易 debug 也支援平行處理 Multi-agent 聽起來複雜 但其實只是把你已經懂的東西，多疊一層

**25:39** · 好，那我們最後整理一下這堂課的重點 這支影片我們從基礎模型的限制開始講起 並帶到能夠加強模型表現的技巧和技術 首先是 Prompt Engineering 強化 LLM 輸出，成本最低 重點放在 chaining 跟 testing 第二層是 Fine-Tuning 除非你在處理法律，科學那種需要重複高精度的 domain

**25:58** · 或者興趣使然 否則別沒事找事去調模型 第三層是 RAG 幫模型補足知識的標準解法 做 AI 產品基本上一定會碰到 最後是 Agentic Workflow 從強化單一 LLM 進到系統設計 重點是思維上的心態轉變 從過往的 deterministic engineering 到現在的 fuzzy engineering 以及應對 fuzzy engineering 的 evaluation 系統

**26:22** · 還有在實戰上要如何從拆解任務開始 打造自己的 agentic workflow 第五層是 Multi-Agent 把每個 agent 都當成工具 彼此協作來提升處理速度跟復用性 教授在兩個小時內跑完產業上常見的實作技巧 每個技術的存在理由跟適用情境都交代清楚 有了這樣的認知，你就不會盲目跟風 看到別人在做 multi-agent 就跟著做 看到別人講 fine-tuning 覺得很帥就去玩自己的模型 所以你的下一步是什麼？

**26:48** · 我給你的建議是，從實作中學習 看看你的生活上或者工作上有什麼痛點 從痛點出發去思考解決方法 在這個過程中你就會發現自己需要學會哪些技術 就能夠很有效率的去規劃自己的學習路線 我把這支影片整理成了一篇深度文章 附帶 4 組 prompts 幫你想清楚自己的 workflow 怎麼拆 現有架構有沒有 over-engineering 幫你建立 eval 系統 以及該不該上 multi-agent 有興趣的朋友可以在資訊欄找到連結

**27:15** · 那今天這支影片差不多就講到這邊 如果你喜歡這樣的內容 想請你幫我點個讚 也在底下留言告訴我你們想看什麼樣的內容 那我們下次見