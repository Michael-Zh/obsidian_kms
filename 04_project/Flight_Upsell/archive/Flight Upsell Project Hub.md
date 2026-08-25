# Flight Upsell Project Hub

# Project Background \(expand for details\)

## Why Upsell \& Why Upsell as a Strategic Project?

- **Missing fare, missed opportunities**



- EU and AU teams found that we lack fares with \(carry\-on/checked\) baggage \(as Chinese airlines usually include both bags by default\), and higher tier fares are not price\-competitive \(as we traditionally only optimized for the lowest fare\)\. **This led to missed opportunities to upsell suitable fares to customers with relevant needs**\.

- **Address this complex issue with efficiency**



- A missing fare can be caused by many different factors from sourcing to display, each of which can vary by region, airline, and OD\. Various FBU teams need to be involved to address this complex topic, which **can be difficult for individual regions to navigate and tackle alone**\.

- The current working model causes scattered regional requests and FBU updates flying around, **lacking an overview** of the scope and progress of each workstreams

- **\(New in 2026\) **Hence, this year, **more structured collaboration** between FBU and IBU has been set up, and J and Michael will streamline IBU communication to FBU, and Vivi will streamline FBU communication to IBU\.

- **GMV \- focused trend**

- Encouraging customers to buy higher\-tier fares will contribute to GMV growth, which is an added focus to segment growth in 2026, making this project even more relevant\.

## How do we Define an "Upsell"?

1. **Airline perspective upsell**: among official fares, a customer chooses a higher tier fare than an airline defined threshold\. This is considered an "upsell" for the airline

    - E\.g\. for Lufthansa, *Light* and *Classic* are **NOT** considered upsell from the airline perspective\. Only *Green* and *Flex* are\. AKA the definition **could** **vary** by airline

    - Most relevant to airline relationships and VI \(e\.g\. LH only gives incentive to GREEN sales\)

    - Most relevant to sourcing serving direct content \(e\.g\. 1A/NDC/direct API, etc\.\)



![Image](https://internal-api-drive-stream-sg.larkenterprise.com/space/api/box/stream/download/authcode/?code=Mzg0ZTc0MzkzOGVhYTgwY2JmMmQzNDIwM2I4MjQ3MmNfNzBlMmM2NjkxM2RjMmViY2I1MjExYWQyMjFiNGZiNDFfSUQ6NzYyNDE0NjcwMDI1Njc0MzEzMl8xNzg0MTI1MDI0OjE3ODQyMTE0MjRfVjM)

2. In this project, however, we use **Trip upsell**: on the middle page, as long as the user chooses the **NON\-CHEAPEST** fare, it is considered an upsell\.

    - Include all fares, e\.g\. airline official brand fares on airline\.com, trip self\-bundle, CSD, or consolidator's non\-official fares

    - Although there are limitations to this metric \(the cheapest fare may not always be the lowest possible tier fare due to sold\-out, promotional fare, etc\.\), this is the most measurable and trackable metric for now

3. **Middle\-page upsell **vs** x\-product upsell \(where and when\)**:

    - **Middle\-page upsell: **same definition as trip upsell\.

    - **X\-product upsell/attachment rate**: consider x\-product \(especially x\-bag\) attachment in later booking steps, such as adding x\-product on the fill\-in page during the booking process or post\-booking before the take\-off\.

        - This project **WILL NOT** actively focus on improving the attachment rate of X\-products as a way to upsell\. But x\-product's supply can still influence middle\-page upsell \(e\.g\. for LCCs heavily rely on self\-bundle to offer fares including baggage, or offer bundle fares tailored to customer needs beyond airline brand fare offerings\)\.

4. **Hotel\+flight cross\-sale upsell** is also **NOT** in the scope

---

# Primary KPI \& Scope \(expand for details\)

**Trip Middle\-Page Upsell Rate**: 33% \(Current\) → 38% \(2026 Target\)

- **Calculation**: \(Primary Order Count Choosing Non\-Cheapest Fares\) / \(Total Primary Order Count\)

- **Guardrails**: no negative impact on CR, user browsing time, and GMV

- **Scope**: Economy/Premium Economy, 1\-Meta tracking, all markets

- **Exclusions**: Premium cabins, X\-product attachment rates, hotel\+flight bundle

---

# Recent Meeting Outcomes

## 2026\-05\-28: Regional Project Sync

[Flight Y/W Upsell Regional Sync 20260528 v2](https://trip.sg.larkenterprise.com/docx/UvwOddqhno41v9xj5GLlXz5lgld)

## 2026\-04\-02: Bi\-weekly FBU\-IBU Project Sync

\(running doc\) [2026 Trip Upsell bi Weekly Sync](https://trip.larkenterprise.com/wiki/VS35wIwFCiNvoaksszGcHhh1nId)

[智能纪要：04\-02 \| Trip Fare Card bi weekly sync 2026年4月2日](https://trip.larkenterprise.com/docx/BcXndxZJkoEBNIxMfgYcobGin4e?dcuId=7502014013750132740&from=vc_assistant_notice#doxcn3hAzJ3GmND9IHREKds6ZHe)

## 2026\-04\-01: Regional Upsell Kick\-off

[AI notes: IBU Upsell Project Kick\-off on Apr 1, 2026](https://trip.sg.larkenterprise.com/docx/EgZ8dnMApoN1EPxC8x7lAOV5gjd)

---

# Workstreams

---

## **Workstream 0: Perf/Health Monitoring/Analysis \& Misculious \(P1 \- Ongoing\)**

**Latest Update: 2026\-06\-16 Tue**

**Current Focus**: Run down the opportunity exploration framework to scout for needle movers

**Progress/Deliverables**:

- Dashboard MVP: https://artnova\.ops\.sgp\.tripws\.com/\#/configuration/dashboard/dcb5a78a\-e311\-47df\-98f3\-563030aa81b5?defaultFirstNotLoad=1

- Regional comms: [Fare Upsell Regional Hub](https://trip.sg.larkenterprise.com/docx/F4OodOBn6oQPQ8x46NYlZ3stgQd)

**Next Steps**:

* [ ] \(park, low impact\) Check with Zhexiu for the upsell metric code excluding restricted fares

### **\(ongoing\) Opportunity Exploration Framework \(2026\-06\-16 Tue\)**

#### Methodology

> start from FSC long haul 1\-meta, Y class
> 
> 

1. Ranked by volume, compare the attribute combo order share, trip upsell rate to all FSC benchmark

2. Run down the list to flag on paper upsell potential, flagged in Yellow

3. Check the fare family and have a high level idea how difficult it is to upsell, and what kind of upsell

    1. \(Reasonable\) No baggage \-\> carry\-on/checked bag or carry\-on only \-\> both bags

    2. \(OK\) one bag or both bag \+ no flexibility or low flexibility \-\> more flexibility **AND** reasonably priced

    3. \(Challenging\) more piece of baggage or weight

4. Go through the Data Foundation, Supply, Fare Selection, Display to see which one has issues \(from the audit and data\)

5. The higher the volume, the more foundational issues we find \(data foundation \> supply\), the higher the priority

6. Ongoing issues are also highlighted in Yellow

    1. If verified and don't see potential, change to Grey

    2. If verified and is being fixed, change to Red

    3. If verified and fixed, change to Green

#### Working Files

- Above table on google sheet https://docs\.google\.com/spreadsheets/d/106HIEhfvPrpBugclLzgPq8h\_m5j8UNZp3QYklQi\_9IY/edit?gid=431286760\#gid=431286760

- Coverage data google sheet https://docs\.google\.com/spreadsheets/d/16E4i8A232HRbtiONfIG4QfNQZkVL80lTXiwPld6i4OU/edit?gid=454033280\#gid=454033280

### **\(ongoing\) IBU QA User Research \(2026\-05\-01 Fri\)**

- User Research to understand why choosing upsell fares [非最低价选择用户研究方案  UR for Non\-Lowest\-Priced Fare Option](https://trip.larkenterprise.com/wiki/LcKcwIY16ibMnBkqRHectyxdnuh)

- 2026 Research objectives collection [「Fare card」\&「MT」用研问题收集\-国际AGG](https://trip.larkenterprise.com/wiki/Dv2cwMK9YiQq8IkkyzLcJcDvnag?sheet=39c331)

- 2025 Research Report [Flight Fare Survey Results](https://trip.larkenterprise.com/wiki/YLOFwtWTBi3vHEkx4Xxcp3xrnNg?from=from_copylink)

### **\(next in line\) Upsell weekly monitoring format**

1. To finalize the format for weekly/monthly health report

### **\(park\) Restricted Fare Topics \(2026\-04\-02 Thu\)**

- Need to add this to the upsell glossary / definition

According to Vivi on **2026\-04\-02 **Thu 1\-1 sync

- Restricted fares are **INCLUDED** in the overall upsell calculation \(baked into the logic of the lowest fare tag we use now\)

- There is separate metric to track upsell excluding restricted fares \(need to check with Zhexiu for the code\)\. But the metric is rarely used and the share of the order is very small\.

- In Fare Selection, restricted fares are PKed like all other fares\. But when considering a non\-restricted fare \(from candidate pool to selected pool\), restricted fares will be **excluded** **from selected fare set** to avoid unfair comparison

- Restricted fares are already folded\. And since the folded section will be ranked by price, they are likely to rank on top 

- Robert shared the example code to pull the student fare share

![Image](https://internal-api-drive-stream-sg.larkenterprise.com/space/api/box/stream/download/authcode/?code=MjU0ZGEyYTBkNTlmODU2Y2RhNTg5MDYwYzg0NDI1N2NfYjZlMDkyOGVhZWQ3ZWYzMzY4NzI0ZDM4MzJjYmUzOTVfSUQ6NzYyNDE1OTg2NTI2MjM2MjMzMV8xNzg0MTI1MDI0OjE3ODQyMTE0MjRfVjM)

```SQL
--using the "passengertype" field
 
SELECT 
  passengertype,
  COUNT(DISTINCT primaryorderid_fill) AS orders,
  SAFE_DIVIDE(
    COUNT(DISTINCT primaryorderid_fill),
    SUM(COUNT(DISTINCT primaryorderid_fill)) OVER ()
  ) AS pct_of_total
FROM `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_ord_flt_order`
WHERE orderdate >= "2026-01-01"
GROUP BY 1
```

### **\(park\) Upsell analysis and health check**

1. To complete core market health check

2. Shortlisted deep dive countries/regions \(GB, FR\) based on limitations, country input \(priority, feasibility\) and size of the market:

    1. Coverage data is only limited to FSC and handful LCC\. We either need to add the LCC \(which asked by HK, KR, Still relevant to EU\)\. Or we need the complete benefit level mapping

    2. We can probably start from the EU as the mapping mostly covers the top LCCs and FSCs

3. Previous notes

    - Alternative presentation for easy reading and understanding \-\> positive or decrease is alarming\.

    - Pick one market first \-\> get learning and then move on to the next market

    - Focus on 1\-Meta, Y\+W

        - \(Meta can be influenced more by external market/pricing strategy\)

        - Meta and 1\-meta should have a similar trend for airline level \(secondary check\)

        - Can not totally ignore Meta \(incl\. In the reporting\)

    - Key question: What does it means to us\. Risk? Not risk? \(from business pov\) Opportunity?  Can we rule out:

        - Seasonality, Domestic vs outbound, outbound and by haul, OD mix, airline mix \(FSC VS LCC\)

    - Next analysis:

        - Middle east \- what's the driver of so strong upsell % 

        - JP HK kind of market \<\-\- check if seasonality matters \- we need to rule out seasonality factor

        - US \- check what's the driver of lower order \(OD/airline/Haul\)

    - Recheck key takeaway from IBU 2026 kick off meeting around "GMV" topic

4. Goals:

    1. Understand core market health \(as part of the regular check maybe monthly or quarterly\) to identify risk and opportunities to deep dive

    2. Based on the mapping availability and feasibility, find airlines and ODs for FBU to find the root cause

5. Identify key risk/opportunity segments from above markets \(defined by POS x Haul\), based on size of the segment, and either low upsell% \(especially stagnated upsell%/order growth\), or high upsell% but seeing upsell%/order decline

6. Check the top 10 airlines in each of the \(2\) segments, see which ones are in the brand data base \(and brand fare accounts for high share\)

7. Check the coverage rate Vs the upsell rate when available

8. For the ones likely to have problems with coverage rate, check the main OD and the fare family\. Understand if they are indeed "easy" to upsell

9. If so, provide to FBU team for investigation

10. Repeat

Insight limitations:

1. Use front end tracing to help detect ranking/display issue

### **\(close\) Prod Change Comms Framework \(2026\-04\-30 Thu\)**

- Aligned comms model[Upsell ABT sharing framework](https://trip.sg.larkenterprise.com/docx/RNdmdXYCRoPWiRxnGrylCM7Dgof)

    - Tempalte [\[Type of Change\] \[Brief Description\] – \[Region/Market\] \(Timeline/Status\)](https://trip.sg.larkenterprise.com/docx/WncDddJ3loei6VxtaXUl3KUTgk0)

    - [Skill link](https://aily.feishu.cn/ai/agents?shared_skill=c2d60fec-ec6d-4bc8-9967-6a86c4cb5326) \(anyone with the link can use it too\)

    - [Regional comms folder](https://trip.larkenterprise.com/drive/folder/NeB0fSPfNlHJYGdx10LcFcPJnnf?from=from_copylink) 

    - ABT calendar reference [Global Farecard UX](https://trip.larkenterprise.com/wiki/N0w1wnDbiiITnzkCBpJc1MYan75?table=ldx7zjdhCyHEzqhx)

According to Vivi on **2026\-04\-02 **Thu 1\-1 sync

- Generally speaking, Vivi has visibility of the "container" level change\. E\.g\. How the guarantee product is shown on middle page, or what kind of product is shown in the guarantee slot

- However, when it comes to specific product changes WITHIN the container, e\.g\. the insurance team changes the pricing and wording of the insurance product, Vivi may not have 100% visibility

### Reference Links

- \(FBU\) H2 upsell draft plan [2026 H2 Trip Upsell 项目文档草稿](https://trip.larkenterprise.com/wiki/R0YNw7Jtbi2AQvkLXhBces3nnVh)

- \(J\) New Flight 101 [Flight 101 by J \(2026 Version\)](https://trip.sg.larkenterprise.com/docx/NTYtd0mTDoYX6tx8qgplZEhIgRf)

- \(FBU\) Fare card upsell project page [2026 Trip Upsell 项目文档](https://trip.larkenterprise.com/wiki/LiEqwVagjiSaYzks8UIcTwzrnHc)

- \(IBU\) Key airlines to focus on [focus airlines 202601\_v5\.xlsx](https://trip.sg.larkenterprise.com/file/Dh7NbPDMGoZfxCxRktDln2WYguo)

- \(FBU\) Fare card upsell opportunity analysis [Upsell 机会点数据分析](https://trip.larkenterprise.com/wiki/XYX5wUbvfinBhEkQEKecuGbMnag)

- \(FBU\) Fare card upsell analysis [Trip中间页运卡分析\(完结）](https://trip.larkenterprise.com/wiki/UGXYwCKOaiNAAjkBfKWcPJIJnyp)

- \(FBU\) Upsell driver report [2025 Q4 Trip upsell 增长归因报告](https://trip.larkenterprise.com/docx/Q4afdNhuJoSvsVxVuWlcowO6nUh)

- \(FBU\) EU Upsell Growth Driver Exploration [欧洲 Upsell Rate 上升因素分析 —— 托运行李报价覆盖率假设验证方案](https://trip.larkenterprise.com/wiki/EBwWwTjHZivdghkffoecR0XDnVe)

#### Archived

- [Fare Card Project Strategic Proposal](https://trip.larkenterprise.com/wiki/JlgWwsWPpiZOHakUEjGcABVNnaf)\(Michael's draft\)

- \(IBU BI\) [Baggage attachment analysis V1\.0 \-EN](https://trip.larkenterprise.com/wiki/HOwrwmyhNifcz1kAgJNcj7xpn2d)

- \(J/M\+IBU BI\) [Upsell discussion Dec 10](https://trip.sg.larkenterprise.com/docx/HXTbdsbBQo7ufQx7QAVlnoy0gRe) \(Main doc on aligned WoW and workstreams\)

- \(J/M\+IBU BI\) [Fare card project sync](https://trip.larkenterprise.com/wiki/KOPMwvYf0igwZik5nPjcbyOOnKe)

### 

---

## **Workstream 1: Supply Coverage \(P1 \- Ongoing\)**

**Latest Update: 2026\-06\-24 Wed**

**Current Focus**: Brand fare coverage audit and improvement for 40 airlines

**Progress/Deliverables**:

- The `internal investigation tool` MVP is expected to be delivered by EoW Jun 26 \(only on supply side, not including fare comparison issues\)\.

- The `automated brand fare mapping` MVP and first batch airlines are expected to be delivered by EoM July

    - Once we have MVP, BE will organize a session to go through route sampling method and attribute parsing as the next iteration

**Next Steps**:

**Parking lot**:

- \(idea, Vivi\) tag each fare with the main benefit details \(beyond brand fares\)

- Ask backend team to backfill the coverage V2 data regarding idx\_dim tags

- Vivi needs to align internally within FBU to define the coverage dashboard responsible, since there are 2B and 2C users with different requirements \(at moment more tailored to BD team\)

### **\(ongoing\) Brand Fare Audit with a focus on Coverage with Regions \(2026\-06\-24 Wed\)**

- **Background \& Goal**:

    - The AGG team can identify high\-level / global coverage issues of certain fares, but they don't have capacity to scallably pinpoint specific problematic routes \(and co\-relate it to the upsell rate?\)

    - To build an efficient way to detect and report issues to FBU via a newly established process and template with all needed info for FBU

- **Method:**

    - \(see the playbook\)

- **Documentation:**

    - Regional playbook [Economy Brand Fare Audit \- Regional Playbook](https://trip.sg.larkenterprise.com/docx/EANKdOhfAoR3EmxoKcLlt0HLgGg)

    - Final Template: [ \[Country\]\[Airline\] Y Class Brand Fare Audit \(template\)](https://trip.sg.larkenterprise.com/docx/CMK6dDHW4oQBR5xc2oilzkx1gkg)

    - J's example case \(MH\): [MH \(Malaysia Airline\) Economy class fare type audit](https://trip.sg.larkenterprise.com/docx/AzFYdqdYWoRXuJxBdZIlXWt2gNO)

    - Raw file folder: https://trip\.larkenterprise\.com/drive/folder/YVwTf0iNqldtBhdJalecWmUNnGh

    - Issue summary and tracker: [Airline Upsell Fare Audit — Issue Summary](https://trip.sg.larkenterprise.com/docx/Gd23dmXgqouvAyxTw1pll1YKgug)

    - \(FBU\) Vivi proposed a template: [\[Template\] Fare Coverage Investigation Guidebook](https://trip.larkenterprise.com/wiki/Oi25wBQJ3iKo2Tkmwrzc1YlVn3e)

- J's notes on different suppliers:

    - CSD \<\-\- remove this in audit scope because we know the exact cause, Regional team can talk to CSD team to improve scraping

    - hybrid \<\-\- only few hybrid airline, and often Sean knows which fare we already get VS not, i think the regional audit part is front end check to find any internal config issue\. me or michael can do summary for this hybrid on behalf of regional team with Sean first, and then ask regional team to do manual audit\.

    - airline with dedicated BD \+ direct commercial \+ direct connection \(1A/2B/GDS/TF/subiata etc\) \<\-\- this is where regional team can do more deep coverage check with BD

    - airline with no dedicated BD nor direct commercial nor direct connection \(rely on oversea supplier\) \<\-\- i think volume must be very small, we can ask oversea supply team to check further, but we can de\-prioritize first\.

### **\(ongoing\) Brand Fare Data Infrastructure Building \(2026\-06\-24 Wed\)**

- **Goal**:

    1. The key focus now is to leverage the manual database to build and refresh all related data products\. And later on, adding additional data sources and airlines

    2. Opportunity to prioritize certain airlines that are important for BD or regions

- **Updates:**

    - \(see above **Progress/Deliverables**\)

- **Documentation:**

    - [Trip航司官网爬虫预计可获取数据页面](https://trip.larkenterprise.com/wiki/Pz2ewoxKpi0uJ5kZB5LcKqWvnsc?from=from_copylink)

    - \(FBU\) Roadmap overview [品牌权益基础信息体系搭建](https://trip.larkenterprise.com/wiki/Mha1wk912i7fsfkiVpXcoM9SnNb?from=from_parent_docx)

    - \(FBU\) Dashboard requirement [携程国际机票中间页upsell运价数据看板需求说明](https://trip.larkenterprise.com/wiki/AWPxwGCU2i6Fh6kFBGvcWX6bnsc)

    - \(FBU\) Vivi's final product doc?

### Reference Links

- \(FBU\) High level coverage analysis \(for MU, CI, etc\.\)[品牌运价覆盖数据问题与数据洞察](https://trip.larkenterprise.com/wiki/CYTFwtvEKioZXpkl4VccDPyGnje?from=from_copylink)

- \(FBU LCC\) U2 carry\-on bundle coverage issue investigation [T手提Bundle流程整理 \- U2手提覆盖调查计划](https://trip.larkenterprise.com/wiki/Kpr1wFsRdi08AekspAKcwv1cnxb?from=auth_notice&hash=6d8d7285801204931e80cddb4137738e)

### Key Learnings

- High upsell rate ≠ no coverage issues \(may still miss higher brand fares\)

- Requiring accurate fare mapping per OD to ensure correctly tracking upsell%

- For FSC, upsell motivation may come from flexibility, seat selection, meal and other attributes\. In some cases, we may also need to look into different weights of baggage

---

## **Workstream 2: Fare Selection \(P2 \- H2 continue\)**

**Latest Update: 2026\-06\-24 Wed**

**Current Focus**: Working on the next iteration \(collecting ideas\)

**Progress/Deliverables**:

- Next step [算法迭代 todo list](https://trip.larkenterprise.com/wiki/W0lTwIOPciQfejkxMUCcoRUbnTd?from=from_copylink)

**Next Steps**:

* [ ] \.\.\.

**Parking lot**:

- \(NA\)

### **\(upcoming\) 旁路表 / Bypassing Table  \(2026\-07\-01 Wed\)**

- New capability focused on the fare selection workstream\.

- Documentation

    【旁路表】产品设计文档 \(link: [【旁路表】产品设计文档](https://trip.larkenterprise.com/wiki/OPzwwU0VDizmJJkEvLpcm84hnih)\)

    旁路验证\-介绍及SOP说明 \(link: [旁路验证\-介绍及SOP说明](https://trip.larkenterprise.com/wiki/KaSIwnVG4iwCL2kUApvctX3Yn0l)\)

    02\. 旁路表 \(link: [02\. 旁路表](https://trip.larkenterprise.com/wiki/ZoQKwxHhZiNi3JkSGeYck4ccnSF)\)

### **\(upcoming\) New Fare Selection Algorithm for C/F \(2026\-06\-24 Wed\)**

- FBU is working on the C and F class fare selection algorithm\.

- The final design is not yet complete; documentation will be added once available\.

- Currently blocked due to service fee display ABT \(more in FE section\)\.

- [【T两舱】验收文档](https://trip.larkenterprise.com/wiki/HUQHwv449iZJK3kdojDc97nqn8p)

### **\(closed\) New Fare Selection Algorithm \(2026\-04\-29 Wed\)**

1. Shift from bucket method to fully automated algorithm

2. Implementation of "small price gap" fare reduction \(V1 \-\> V2\)

3. Communication refinement for regional testing expansion

4. **Documentation**

    [02\. 中间页比价优化项目](https://trip.larkenterprise.com/wiki/GUo3wYCcriCcMBk3KK8cwG53nec?from=auth_notice&hash=b0d9f5fc59ff511cd982ad497075af9e)\(project background and initial algorithm design\)

    [Trip Fare Card Upsell Project\.pptx](https://trip.larkenterprise.com/wiki/A80lwWZvPideUCkkxbjcBVKgnqh?from=from_copylink)

    [07\. AB实验计划与指标 \+ 实际时间线](https://trip.larkenterprise.com/wiki/FVnJwLX6diImNkk16ivcWoXZnjh) \(AB testing and adjustment \+ real time experiment log\)

    [Trip比价算法数据分析报告](https://trip.larkenterprise.com/wiki/CLmgwLG1siShPSkUXFScNdD3nqg) \(experiment report\)

    50% traffic comms [【IBU email】New Fare Selection Algorithm A/B Testing Opens More Traffic](https://trip.larkenterprise.com/wiki/HhOjw3DmNiismZkc8C1cHo7LnVh)

    [【T经济】新比价算法 复盘报告](https://trip.larkenterprise.com/wiki/JTsMwLIgfijq32kSYPfc4qIhnab?from=from_copylink)\(V2 experiment report\)

    100% traffic comms [【IBU email】New Fare Selection Algorithm rollout plan](https://trip.sg.larkenterprise.com/docx/Daokd8QfjopF65xkoUpl9eqfgwg)

    FYI New fare selection algorithm minor update \(V1\-\>V2?\) [比价算法收益\(修正对赌问题）](https://trip.larkenterprise.com/docx/WdKBdYR51oRbqPxnOIwctCc6nMY)

    FYI New fare selection algorithm airline per tier PKed rate [36家重点航司 分tier的比价胜出率](https://trip.larkenterprise.com/wiki/EWjDwlXIjiBNIgkKvDKcpMPZnle?sheet=tJ4OsG)

### Reference Links

### 

---

## **Workstream 3: Ranking \(P3 \- Ongoing\)**

**Latest Update: 2026\-07\-09 Thu**

**Current Focus**: test BI\-powered personalized ranking

**Progress/Deliverables**:

\.\.\.

**Next Steps**:

\.\.\.

### **\(ongoing\) Personalized Ranking \(2026\-07\-09 Thu\)**

1. Use machine learning to personalize the ranking based on signals \(such as ODT, pax, order history\)

2. Expected live on **July 9th**

3. Regions can apply to be added to whitelist: [Ranking Algorithm for Flight Middle Page whitelist](https://trip.larkenterprise.com/wiki/AfXMw4H21iRijXkDv8KcVC0enTf?from=from_copylink)

4. **Documentation**

    - [智能纪要：04\-10 \| 中间页周会 2026年4月10日](https://trip.larkenterprise.com/docx/BgCVdzpipoPvm5x8vGdcLe9CnQg)

    - Current product design for personalization[Trip 中间页运价推荐排序升级项目文档](https://trip.larkenterprise.com/wiki/TQSsw9CNnisjvDkpNJ3cuiMtnyp)

    - Proposed EN version: [Trip Middle Page Fare Recommendation Sorting Upgrade Project](https://trip.sg.larkenterprise.com/docx/ANf6dwmI2oI0WixTcRPlmmTjgbg)

    - FYI Personalized ranking BI rendition: [BI 排序接口参数验证](https://trip.larkenterprise.com/docx/PDTPdRynGootLpxWFZjcBsvPnae?from=from_copylink)

    - [20260703 \[Ranking ABT\] New Personalized Ranking Algorithm for Flight Middle Page \- Global \(July\)](https://trip.sg.larkenterprise.com/docx/SAaIdpTfaoB3Inxn41elDuiQgkh?from=from_copylink)

### **\(closed\) Guarantee Slot Global Test \(2026\-06\-24 Wed\)**

- **Goal:**

    - To test the routes and airlines that are more beneficial to sell more brand fares \(e\.g\. Volume Incentive etc\.\)

- **Experiment design:**

    - [Branded Fare Upsell Test（APP中间页置顶推荐）](https://trip.larkenterprise.com/wiki/J0ZPwuf1CiZCkUktz8CcOq3Dnxc)

    - [智能纪要：推荐位置实验 2026年3月31日](https://trip.larkenterprise.com/docx/USIUdmZDPoRWGHxJj6wcpLajnce)

![Image](https://internal-api-drive-stream-sg.larkenterprise.com/space/api/box/stream/download/authcode/?code=OTAyZmRkMGFmNjYxNTExMDc4NzI5ZjYxNmMxOTI1MWNfMmVjNGE5OGU5ZmQ2NjEzNTA0YTcyNjFiMjY0ZjhlNzNfSUQ6NzYyNjAyMzU2MDY4Mjg1MjA2MV8xNzg0MTI1MDI0OjE3ODQyMTE0MjRfVjM)

- **Scope**:

    - Airline and OD list, test will exclude all EU locales \(e\.g\. Searching for LH flights on TH locale site\) and middle east routes

    - App only

    - The selection of the routes and airlines is based on BD's input \(2B oriented\) \- see the doc for details

- Potential test for new logic to show the guaranteed products[Trip中间页置顶推荐位优化](https://trip.larkenterprise.com/docx/SzbJdq5qgoyoSDx9GBvcYYcdnGg)\- just an idea for now

- **Draft Email Comms**: [20260421\[ABT\] Guarantee Product vs Fare Upgrade – Global excl\. EU \(Apr 2026\)](https://trip.sg.larkenterprise.com/docx/VNevdDKk2oOMW1xLh4elqwM5gng)

- ABT link: http://abtesting\.bdai\.sgp\.tripws\.com/\#/index\-detail?id=90204\&expId=260302\_IBU\_MidPRecomm

- The result is negative and ended early \- need resources from BI to complete the report

- May need to redefine the test to reopen it \(too low traffic\)

### **\(closed \- split to sub projects\) Middle Page Fare Presentation \(2026\-03\-25 Wed\)**

1. FBU is ideating new ways to rank fares in order to reduce the decision load of the customers

2. There are three directions they are thinking about now

    1. Most conservative: maintain and optimize the current business rule based ranking logic \(e\.g\. Ranking based on brand fare family to elevate brand fare exposure\)

    2. \(ongoing\) Relatively Low Effort Experiment: add quick filters reflecting popular attribute combination on top of the middle page \(similar to ctrip design, but on top / between itinerary and the first fare, not by "floors"\)

    3. Most advanced/complex: use machine learning to personalize the ranking based on signals \(such as ODT, pax, order history\)

3. **Documentation**

    1. Details of Middle Page Fare Presentation [Trip中间页产品定位与优化](https://trip.larkenterprise.com/wiki/O3V7w6SrsitoJDkgdEoc5W98nQh)

    2. Discussion memo \(Vivi \+ front\-end \+ BI\): [智能纪要：【占位】T 中间页讨论 3\.0 2026年3月18日](https://trip.larkenterprise.com/docx/NxTldInfuo3c5axup1acPi0enYc?dcuId=7502014013750132740)

### **\(on pause\) Brand Fare Family Based Fare Ranking Algorithm \(2026\-03\-25 Wed\)**

1. In 2025, in order to elevate brand fare and optimize the overall ranking, FBU conducted a series of analyses and ABT to develop a new ranking algorithm based on brand fare family\.

2. The latest is V3

3. This work was paused due to technical limitations preventing concurrent AB testing with Fare Selection algorithm now

4. Will resume when Fare Selection algorithm testing completes

5. This workstream is also likely to merge with the **Middle Page Fare Presentation Discussion**, as this is one of the options\.

6. **Documentation**

    1. Initial ideation[【PRD】严格升级以品牌运价为梯度升级](https://trip.larkenterprise.com/wiki/VCt3wDwOUiRGTvkupv1cNn6Vngd)

    2. V1 experiment report \(2025 Sept\) [9月trip 中间页运价升级实验分析](https://trip.larkenterprise.com/docx/BacidJZjDouUAOxpX04c9fWPnZd)

    3. V2 experiment report \(2025 Oct\)[10月trip 品牌运价升级实验V2分析](https://trip.larkenterprise.com/wiki/YyCewuAVkihupOkZsV7cxqEinJg)

    4. App experiment summary and iteration discussion [2025 APP V1\+V2\+V3品牌运价实验数据分析](https://trip.larkenterprise.com/wiki/Z800wsgh2ijyrpkteRScHSYknRm)[APP品牌运价实验迭代](https://trip.larkenterprise.com/wiki/P0EKwubsJi3ZMikwdYPcofMin2c)

    5. Next steps [品牌运价MVP验收计划](https://trip.larkenterprise.com/wiki/MdPjwjU5aiHzZNkopxZcLvRpnLv)

### **\(closed 2026\-04\-07\) SG reported suspected ongoing Guarantee Slot ABT for MH**

MY reported:

![Image](https://internal-api-drive-stream-sg.larkenterprise.com/space/api/box/stream/download/authcode/?code=NDY5MjFjODg0NmU2MzVkNTNjYzNhNmEyMzRkNWJhZjJfMjY3OTNjYWRlNjI5YzM1MjI0MjZlOTUzYTZiOTIyZjRfSUQ6NzYyNDE3MzczNTU1NDcxNTM2MF8xNzg0MTI1MDI0OjE3ODQyMTE0MjRfVjM)

![Image](https://internal-api-drive-stream-sg.larkenterprise.com/space/api/box/stream/download/authcode/?code=MjQ5OGQ3NDUyNTY2N2ZjYjljZTk5N2FkZjM3ZDQwMDBfZGZkY2ZkNWFjNTAxOTNiNDNjNTZjMzQ3MGRhNDM4OWJfSUQ6NzYyNDE3Mzc1OTQ4MTU5NzY2Ml8xNzg0MTI1MDI0OjE3ODQyMTE0MjRfVjM)

According to Vivi on **2026\-04\-02 **Thu 1\-1 sync

- No ongoing ABT \(but planned\)

- MH is not in the scope

- What product to show in guarantee slot depends on:

    - Availability to this OD/airline

    - The claim rate of insurance \(if too high, may suspend\)

- If can't show insurance, falls back to ticket upgrade

- Get back to Doph



### **\(closed\) EU Removal of Guarantee Slot \(2026\-04\-02 Thu\)**

According to Vivi on **2026\-04\-02 **Thu 1\-1 sync

- What: all guarantee slots are removed for EU locales

- Why: EU complained a lot that this product is not relevant to the market

- When: was done before Vivi Join \- don't know the details

- \(to add more details from J \- TBU\)

### 

---

## **Workstream 4: Pure Front\-end \(P2 \- Ongoing\)**

**Latest Update: ****2026\-07\-02 Thu**

**Current Focus:** Compact itinerary; Visual guide to Luggage; \(\+Middle Page\) BI ranking, quick filter

**Progress/Deliverables**:

- \(see [Fare Upsell Regional Hub](https://trip.sg.larkenterprise.com/docx/F4OodOBn6oQPQ8x46NYlZ3stgQd) for summary and detail links\)

**Alignment**:

- Sirius confirmed that we don't need another round of benchmarking, as this is already included in H5 work \(H5 is the same code/experience as app\)\. Most of the minor issues are already in Sirius' pipeline to resolve \(and address in the H5 bi\-weekly demos coordinated by Erik\.\) Other potentially bigger issues on the middle page, Erik is still summarizing them, but eventually will get to Sirius\.

**Next Steps**:

* [ ] \(\.\.\.\)

### **\(rolled out\) Service Fee Display A/B Test  \(2026\-07\-01 Wed\)**

- Tested the effect of displaying cancellation and change fees together with agency and Ctrip service fees\.

- 

- Documentation

    [【退改服务费】覆盖率和走查截图](https://trip.larkenterprise.com/wiki/O6cqwiognievLLkoMQ1c6TRenOZ)

    \(need details of the design and versions\)

### **\(upcoming\) Compact Itinerary Display V2 — Optional Flight Info Popup \(2026\-07\-02 Thu\)**

**Goal, context, and background**: Building on V1 learnings that completely hiding flight information hurts conversion \(fill page back rate \+3\.84%\), Phase 2 gives users the choice to view flight details via an optional popup on the list page before entering the simplified intermediate page\.

**Main objective**: Maintain or improve upsell rate by giving users choice rather than forcing simplified layouts, while still increasing fare visibility on the intermediate page\.

**Current task and blockers**: Development in progress\. Two design variations being tested: Group B \(subtle "view flight info" area\) and Group E \(prominent "view flight info" area\)\. Launch scheduled for June 30, 2026\. AB test to follow post\-launch\.

**All related document links**:

Design Mockups [https://www\.figma\.com/design/HKalIxpLptJlE6QZqn5YNh/APP](https://www.figma.com/design/HKalIxpLptJlE6QZqn5YNh/APP%E4%B8%AD%E9%97%B4%E9%A1%B5%E8%88%AA%E7%8F%AD%E4%BF%A1%E6%81%AF%E6%96%B9%E6%A1%88?node-id=666-4349)[中间页航班信息方案?node\-id=666\-4349](https://www.figma.com/design/HKalIxpLptJlE6QZqn5YNh/APP%E4%B8%AD%E9%97%B4%E9%A1%B5%E8%88%AA%E7%8F%AD%E4%BF%A1%E6%81%AF%E6%96%B9%E6%A1%88?node-id=666-4349)

Comms [20260703 \[ABT\] Middle Page Compact Flight Info V2 \(Global\)](https://trip.sg.larkenterprise.com/docx/E83FdsjaNondbQxRRkplmTcbgDe)

### **\(upcoming\) Trip Online Layout Adjustment — Vertical Fare Display \(2026\-07\-02 Thu\)**

**Goal, context, and background**: Redesigning the Trip Online intermediate page from horizontal to vertical layout to better align with desktop users' scrolling behavior and improve fare discoverability\.

**Main objective**: Increase fare exposure and upsell potential by displaying fares in a wrap grid with increased popup height, rather than horizontal scrolling cards\.

**Current task and blockers**: Scheduled for July 8, 2026 release\. Phase 1 includes vertical segment layout, wrap grid for fare cards, floating CTA bar, and simplified itinerary \(Group E\)\. Phase 2 will add Economy/Business class toggle tab and "Select" buttons on each fare card\.

**Release will follow below priority:**

1. Vertical display of farecards phase 1 \(release 7\.15\) [Online中间页优化一期\-布局优化](https://trip.larkenterprise.com/wiki/I7Mpw2XBYiot6TkPsfCci3cvnvg)

2. Vertical display phase 2 \(to include the tab to switch class\)

3. Adding button to each fare card https://project\.feishu\.cn/x7mm65/story/detail/7034442800

**All related document links:**

\[Feature Launch\] Trip Online Intermediate Page Layout Adjustment – Global Markets \(Launching July 8, 2026\) [\[Feature Launch\] Trip Online Intermediate Page Layout Adjustment – Global Markets \(Launching July 8, 2026\)](https://www.feishu.cn/docx/RWSXdtQzAoe6jbxSmmWlZ4d2gfd)
Design Mockups [https://www\.figma\.com/design/H6FqMnF5Wj8qeqdfdmHHvH/\-T\-Online\-\-Fares\-in\-Side\-panel](https://www.figma.com/design/H6FqMnF5Wj8qeqdfdmHHvH/-T-Online--Fares-in-Side-panel)

ABT link: http://abtesting\.bdai\.sgp\.tripws\.com/\#/index\-detail?id=108446\&expId=260703\_IBU\_OBJYH

### **\(on hold\) Void / 24\-Hour Free Cancellation Display \(2026\-07\-01 Wed, PM: Oliver Tang\)**

- Recently identified 24\-hour free cancellation display issues\.

- Covers the definition of void and related investigations\.

- The latest is that the FBU frontend team will put this in the H2 roadmap\. This will be considered together with the service fee discussion to decide how to display it properly\.

- Aligned that this is an issue \(covering the long\-term refund policy\) but no aligned solution yet

- Roughly two directions: display both or redirect to the detail page \(based on Doris' hotel experience\)

- Make sure that we focus on the right metrics and scope \-\> weakness is the data

- Documents

    Void definition [废票的定义及适用业务场景](https://trip.larkenterprise.com/docx/VebodqO2bozY8BxE9vQcUDm9nBh)

    [Void/24h, Cancellation/Change Policy SQL \(from Oliver\)](https://trip.sg.larkenterprise.com/docx/ErjBdWw39oMoy6xIpvIlSAw7gKd)

    [Void \& 24hr Free cancellation sync w/ FBU](https://trip.sg.larkenterprise.com/docx/Xh1mdomUeoLtAux7wGrl4Mijgrj)

### **\(closed\) Quick Filter \(2026\-07\-02 Thu\)**

**Goal, context, and background**: Tested adding "checked baggage included" and "carry\-on baggage included" quick filters on the Trip APP intermediate page to improve discoverability of higher bundled fares and boost upsell rate\.

**Main objective**: Evaluate whether baggage inclusion filters drive users toward higher fare options\.

**Decision**: after the 2nd round of 50% traffic version E, uplift is positive and decided to roll out to 100% traffic on **Jul 2nd**\.

1. **Documentation**

    - [智能纪要：04\-10 \| 中间页周会 2026年4月10日](https://trip.larkenterprise.com/docx/BgCVdzpipoPvm5x8vGdcLe9CnQg)

    - Ctrip Quick Filter ABT report: [【实验报告】中文国际中间页分楼层改版\-202510](https://trip.larkenterprise.com/wiki/Ml9Dw4W5ciR0rlkmDW4cVIeJnIg)

    - Most important, impactful attribute analysis[运卡权益组合的转化效率分析](https://trip.larkenterprise.com/docx/TfM5dtv0eovi8WxS7FacoTQBned) I'm not very sure this analysis is helping a ton and actionable yet

    - [20260703 \[ABT\] Middle Page Quick Filter for Baggage Result/Rollout \(Global June\)](https://www.feishu.cn/docx/Y2NudcZThockoDxyel5l8zg8gUh)

    - [「实验分析」Trip APP中间页增加行李筛选项](https://trip.larkenterprise.com/wiki/JsgtwcsuIib4BjkxRi3cQo8znUb)

    - Quick Filter Tracking Events https://trip\.larkenterprise\.com/docx/GoHRdAuMio9hBdxzhVFcayYzn4g 

    - ABT Link [http://abtesting\.bdai\.sgp\.tripws\.com/\#/index\-report?id=99675\&expId=260512\_IBU\_xlsx](http://abtesting.bdai.sgp.tripws.com/#/index-report?id=99675&expId=260512_IBU_xlsx)

### **\(closed\) Compact Itinerary Display V1 — Simplified Flight Info ABT \(2026\-07\-02 Thu\)**

**Goal, context, and background**: Tested simplifying the flight information header on the Trip APP intermediate page to increase exposure of higher fare options\.

**Two variants were tested**: Group B \(simplified header only\) and Group E \(simplified header \+ list page flight itinerary confirmation popup\)\.

**Main objective**: Determine whether reducing flight info visibility increases fare option exposure and upsell conversion\.

**Current task and blockers**: Experiment completed and analyzed\. Group B showed purely negative results\. Group E showed mixed results with positive CR trends \(\+0\.37%\) but decreased upsell rate \(\-2\.50%\)\. Best performance observed in EU core markets and long\-haul LCC segments\. Deep\-dive analysis ongoing\.

**Documentation:**

Comms [20260703 \[ABT\] Middle Page Compact Flight Info V1 Result \(Global\)](https://trip.sg.larkenterprise.com/docx/OqYpdkWu7osM0Tx5mzUlErwrgfe)
Trip Intermediate Page Simplified Experiment Data Analysis [Trip中间页精简实验数据分析](https://trip.larkenterprise.com/wiki/Vaf0wkM51iNW1XkIVJJcV6t3nVf)
Compact Itinerary Experiment Basic Data Exploration [中间页精简实验基础数据探查](https://trip.larkenterprise.com/docx/Lkh1dwm29o1AM2xjYp6ckOaonce)
ABT Link [http://abtesting\.bdai\.sgp\.tripws\.com/\#/index\-detail?id=94285\&expId=260402\_IBU\_TMPSA](http://abtesting.bdai.sgp.tripws.com/#/index-detail?id=94285&expId=260402_IBU_TMPSA)

### Reference Links

- Middle Page Roadmap   Roadmap 2026 H2 [中间页 Roadmap](https://trip.larkenterprise.com/wiki/Ff4RwS4LPiZJd9kg0ODclm7ynVf)

- Middle page X\-Bundle product description [【产品文档】中间页 X Bundle](https://trip.larkenterprise.com/wiki/Qw1ow3fcXiRj8Xkhzq2caN3ynNe)

- Front\-end x Vivi Weekly Minutes

    - [智能纪要：04\-22 \| 中间页周会 2026年4月22日](https://trip.larkenterprise.com/docx/CtmidAICdo81aAxkzirctY33nPc?dcuId=7502014013750132740)

    - [智能纪要：04\-10 \| 中间页周会 2026年4月10日](https://trip.larkenterprise.com/docx/BgCVdzpipoPvm5x8vGdcLe9CnQg)

    - [智能纪要：推荐位置实验 2026年3月31日](https://trip.larkenterprise.com/docx/USIUdmZDPoRWGHxJj6wcpLajnce)

- Front\-end generic hub \(including fare card related changes in the pipeline\) [Global Farecard UX](https://trip.larkenterprise.com/wiki/N0w1wnDbiiITnzkCBpJc1MYan75?table=ldx7zjdhCyHEzqhx)

- 2025 Benchmarking

    - Pain point documentation [Fare\+cards\+\-\+UX\+Benchmarking\.doc](https://trip.sg.larkenterprise.com/file/G8ZQb3qckoD3TAxSmwWlRLQtgIg)

    - Summary and actions [IBU Insights \& FBU Actions](https://trip.larkenterprise.com/docx/D8FHdat5IoXpEtxzN9hcExEbnqg)

- 2026 H5 Full User Journey Benchmarking \(H5 is the same code/experience as app\)

    - [H5 SEO UX Benchmarking Kick\-off \+ Manual](https://trip.larkenterprise.com/wiki/G2gRwPpMri4Z35kHQFzcyZIenph)

    - [H5 Demo Days](https://trip.larkenterprise.com/wiki/UdVUwoeMViGlUDkkfg4cSLBdnsh)

- FBU Front\-end 2026 OKR [机票前台产品 26 年规划和 H1 OKR](https://trip.larkenterprise.com/wiki/M6g3wblqJiSwYukzPQxcaD3inyb)

### 

---

## **Workstream 5: Airline Compliance \(P1 \- Ongoing\)**

**Latest Update: 2026\-06\-24 Wed**

**Current Focus**: Compliance capability is ready and now roll out airlines by phase with BD \(and pending AB testing to evaluate the impact\)

**Progress/Deliverables**:

- AA/DL has implemented the strict fare display from Apr 20th in US locale

- FBU has decided to build the capability and roll out to all relevant airlines in phases

- The product team is working with BD on the specific phasing timeline and list of airlines \- will communicate the details when we have it

**Recent Activities \(internal only\):**

- \(NA\)

**Next Steps**:



### Reference Links

- Airline Compliance Requirement Collection from BD [Fare card display airline request](https://trip.larkenterprise.com/base/XUo9bpoCqaRRyXsmgRucKGXnnCY?table=tblfOr0Mh9x20F1f&view=vewKDoPin3)

- Compliance ABT report [Trip航司分级展示需求影响面估算](https://trip.larkenterprise.com/wiki/X1BFwvPIYiwCCGkyO7OcNX7InEc)

- Compliance capability building prod doc [航司分级合规能力建设 \- 产品需求文档 \(PRD\)](https://trip.larkenterprise.com/wiki/UsJNwijjoivdIvkWBYAcnhFanth)

- AA/DL draft comms: [20260421\[Compliance Update\] DL \& AA Fare Display Changes – US only \(Implemented\)](https://trip.sg.larkenterprise.com/docx/F5BQdra9soYZZExNV8RlztMeg2b)

- FYI Airline compliance AB test / rollout discussion [智能纪要：合规的航司是否AB讨论 2026年6月4日](https://trip.larkenterprise.com/docx/DavDdzfzKo0pwOxfA41cQ3S1nch#doxcnYMr8XEBChuLsDoF4Ou6auh)

- [T航司分级合规记录表](https://trip.larkenterprise.com/wiki/G7XJw55KZiUTtKk5jL7cZE2inNf?from=vcFollow)

### Historical Details \(Collapsed\)

**202****5 Feb**: AF/KL compliance requirements implemented at all locales trip sites \(they are the strictest airline\): brand names must match airline\.com, all attributes must be displayed exactly as on airline\.com \(wording doesn't matter\)\.

### 

---

## **Workstream 6: Pricing \(P4 \- Low Heat\)**

**Latest Update: 2026\-02\-27 Fri**

**Current Focus**: Untangle the pricing rules

**Progress/Deliverables**:

- FBU has decided to build the capability and roll out to all relevant airlines in phases

- The product team is working with BD on the specific phasing timeline and list of airlines \- will communicate the details when we have it

- The most pressing ones are AA \- these would be prioritized and implemented with manual process

**Recent Activities \(internal only\):**

- \(NA\)

**Next Steps**:

* [ ] \(NA\)

### Reference Links

- Fare with baggage price competativeness analysis by Crawler team[含行李价格竞争力\_by航司类型](https://trip.larkenterprise.com/sheets/PaDzs0B5Ghs4qvtXy2Bca6jFnrf?sheet=0ToLsY)

- Real\-time crawler / Seagull Echo tool [AI notes: Flight Real Time Crawler \& Seagull Echo Training on Apr 30, 2026](https://trip.larkenterprise.com/docx/VahldyKzIo765VxESPEcaKBin1d?dcuId=7502014013750132740)

    - crawler issue , lark group is "Crawler\_BI/Data" / Jie

---

## **Regional Collaboration**

### Regional joint workforce \(expand for details\)

|**Region**|**Regional Head / PPM / BA**|
|---|---|
|SEA<br>|@Meng Jun Edmund Ong\(SEA Regional Head\)<br>@Kathy Xu \(徐峪\)\(SEA PGM\)<br>@Shaun Phong\(SEA BA Head\)<br>@Roxy Wen\(TH/PH Country Head\)<br>@Peam Kitsawat\(TH PGM\)<br>@Pat Lazaro\(PH Country Mgr\)<br>@Nikki Nuyda\(PH PGM\)<br>@Amelia Kang\(SG Country Head\)<br>@Doph Goh \(吴颜玉\)\(SG PGM\)<br>@Minh Tuan Dinh\(VN PGM\)<br>@May \(Van Anh\) Nguyen\(VN Campaign Mgr\)<br>@Jayden Purna\(MY Country Mgr\)<br>@Melfani Agnesya\(ID Country Mgr\)<br>@Michael \(ID PGM\)@Kathy Xu \(徐峪\)can you help to tag Michael here? Can't find him in the contact list\)|
|KR<br>|@Joel Namgung\(KR Regional Head\)<br>@Ina Sohn \(손이나\)\(KR PGM\)|
|HK/TW<br>|@Eddy Yip\(HK/TW Regional Head\)<br>@Bowie Chan\(HK Country Head\) \- interim<br>@Sophia Chiang \(江怡萱\)\(TW Country Mgr\) \- interim|
|JP<br>|@Jie Mei \(梅劼\)\(JP Regional Head\)<br>@Juzo Nogami \(野上 十三 \- ノガミ ジュウゾウ\)\(JP BA\)|
|AU<br>|@Roxy Zhou \(周恺盈\)\(AU Regional Head\)<br>@Robert Tonkin\(AU PGM\)|
|EU<br>|@Nithya Ramesh\(EU Regional Head\)<br>@Sagar Patil\(EU BA Head\)<br>@Cristina Cano Fernandez\(EU Flight PGM\)|
|RU<br>|@Jeffers Yin \(殷岳洋\)\(Regional Head/Strategy\)<br>@Dailin Ji \(纪岱霖\)\(RU Country Mgr\)<br>@Dmitrii Amelkin \(Дмитрий Викторович Амелькин\)\(RU PGM\)|
|MENA<br>|@Siddharth Sudhakar\(MENA Regional Head\)<br>@Natasha Shesha\(MENA PGM\)<br>@Amrit Valsraj\(MENA BA\)|
|US|@Alyssa Zhu\(US Regional Head\)|
|BR|@Rafael Silva Cruz Martins\(BR Country Mgr\)|



|**Role**|**Name**|
|---|---|
|IBU Project Sponsor|@Serena Wang \(王思\)|
|IBU Project PoC|@J Nam@Michael Zhang\(Strategy\)|
|FBU Project PoC|@Vivi Ye \(叶静仪\)\(PM\)|

### Upcoming Regional Activities



### Next Steps

* [ ] Michael to compile the regional info hub

* [ ] Michael to compile the upsell Glossary

\(internal tasks\)

* [ ] \(pending feedback, Lily Li\) To share the data source with BAs \(last update 2026\-03\-09 Tue\)

### Regional work/topics

- MH issue case study [MH value运价缺失调查案例学习](https://trip.larkenterprise.com/wiki/ImCrwsylhiTPxJkG4lpcvb0pnsh?from=from_copylink)

- TG issue case study [20260317\-TG Investigation \(via Health Check\)](https://trip.sg.larkenterprise.com/docx/DMrqde8vko0KhlxYOXClxs1Dgsb?from=space_search&previous_navigation_time=1776256009493)

- EU UK issue report [\[Feb 2026\] IBU EU Growth Update ](https://trip.sg.larkenterprise.com/docx/H9FSdrWi4o0G1rxk0qcl1o54gKd?from=from_copylink)

- SEA collaboration nuance\.

    - **Regional Priority:** Upsell is currently a low priority with minimal resource allocation\. However, Kathy is personally committed to supporting you \(as a trusted old friend of hers\!\)

    - **Our Current Needs:** I clarified that we only need regional support for the one\-time audit, feedback on design/ABT, and adherence to the upsell request process for now\.

    - **Market Resistance:** Local teams feel self\-sufficient due to Kathy’s FBU background and training\. Furthermore, urgent "dotted line" manager's demands often need swift turn\-over\.

    - **Integration Challenges:** Ongoing projects like "Counter Agoda" \(brand fare pricing is part of it\) and "Guarantee Bundles" \(which can happend both on middle page and fill\-in page\) are hard to decouple from existing workflows into our specific process\.

    - **Alignment:** Kathy will keep us in the loop as much as possible; we agreed to monitor and resolve issues case\-by\-case\. Kathy added all relevant people to the big group, and those who may have issues to discuss remain in the small group \(so not everyone\)\.

    - Also checked with Vivi, she doesn't think SEA is as "proficient" as they thought\.\.\.

### Reference Links

- Regional kick\-off material[Flight Upsell Project \- Regional Kick\-off](https://trip.sg.larkenterprise.com/docx/E89CdzejSo4w8Ex7DOFlC6aygSb) \(2026\-04\-01 Wed\)

    - [Upsell Kick\-off Follow\-up \(J\+M\)](https://trip.sg.larkenterprise.com/docx/EtbTd1Gtxo4Rq6xFa1Ll2jBWgrh?previous_navigation_time=1775051929357)\(internal version\)

- Regional request process, form, and template \(2026\-04\-01 Wed\)

    - [Regional Request Collection Form](https://trip.sg.larkenterprise.com/docx/OtZ0dSPWxoAa3mxqPbHlJVx2gRg)

- Data source sharing with Lily [Flight Upsell Project \- Sync with Lily](https://trip.sg.larkenterprise.com/docx/GXTjdx69UoesBwxOrSnlEKatgDz) \(2026\-03\-09 Tue\)

- Regional uid for product testing whitelist[Ranking Algorithm for Flight Middle Page whitelist](https://trip.larkenterprise.com/wiki/AfXMw4H21iRijXkDv8KcVC0enTf?sheet=a8ce7f)

---

# Data Sources \& Dashboards

## Data Exploration

### **\(parked\) Guarantee investigation \(2026\-03\-16 Mon\)**

- **Goal**:

    1. Understand the impact of guarantee \(maybe it performs well since we don't have good ranking before, or lack of sourcing\. Is it time to review that?\)

    2. To understand the GMV per order

- **Progress**: obtain the guarantee tag from FBU, waiting to explore the tag

- **Recent Activities**:

    1. obtain the guarantee tag from FBU, waiting to explore the tag

- **Facts**:

    1. Trip flexibility or upgrade products are all possible to be placed at the guarantee slot \(from Vivi\)

    2. It is not always in the first position \(from Vivi\)

## Prioritized airline definition

- There are more than 36\+6 airlines in the list \- it is a legacy term for selected home carriers from FBU

    - **In Scope**: if the data is complete to be included for the audit; if not, why

    - **Coverage**: if it's in the coverage databases

    - **Order count**: 2026 Mar, 1\-Meta, Y/W

    - **Has atpco name:** share of orders have atpco brand name \(first step to be mapped to official brand fare\)

    - **Mapped to official brand name:** share of orders have atpco brand name mapped to official brand name

    - **Assigned an airline brand tier:** share of orders have atpco brand name mapped to official brand name **AND **the official brand name is assigned an airline brand tier

\(parked 2026\-04\-15 Wed\) Clarification with Zhao Yan on brand fare info flow: [36\+6航司范围对齐](https://trip.sg.larkenterprise.com/docx/ZaFBdRd7No6fQwxoZrSlpMHVgbh)

|**Airline   Type**|**Airline Code**|**Airline Name**|**Readiness**|**Coverage**|**Order count**|**has atpco name**|**mapped to official brand name**|**assigned an airline brand tier**|
|---|---|---|---|---|---|---|---|---|
|FSC|MU|China Eastern|1\. Ready to go|Y|118,401|75%|75%|75%|
|FSC|CZ|China Southern|1\. Ready to go|Y|92,965|67%|67%|67%|
|FSC|CX|Cathay Pacific|1\. Ready to go|Y|69,726|57%|57%|57%|
|FSC|PR|Philippine Airlines|1\. Ready to go|Y|65,134|75%|75%|75%|
|FSC|MH|Malaysia Airlines|1\. Ready to go|Y|64,841|51%|51%|51%|
|FSC|CA|Air China|1\. Ready to go|Y|62,027|70%|70%|70%|
|FSC|TG|Thai Airways|1\. Ready to go|Y|53,180|61%|61%|61%|
|FSC|KE|Korean Air|1\. Ready to go|Y|50,987|78%|78%|78%|
|FSC|CI|China Airlines|1\. Ready to go|Y|44,992|84%|84%|84%|
|FSC|SQ|Singapore Airlines|1\. Ready to go|Y|36,383|63%|63%|63%|
|FSC|HX|Hong Kong Airlines|1\. Ready to go|Y|33,195|71%|71%|64%|
|FSC|TK|Turkish Airlines|1\. Ready to go|Y|26,887|75%|75%|75%|
|FSC|EK|Emirates|1\. Ready to go|Y|26,636|70%|70%|70%|
|LCC|FR|Ryanair|1\. Ready to go|Y|21,702|98%|98%|98%|
|FSC|NH|ANA|1\. Ready to go|Y|13,945|67%|67%|67%|
|LCC|TO|Transavia France|1\. Ready to go|Y|13,154|65%|57%|57%|
|FSC|QR|Qatar Airways|1\. Ready to go|Y|13,073|80%|80%|80%|
|LCC|VY|Vueling|1\. Ready to go|Y|12,701|96%|91%|96%|
|FSC|UA|United Airlines|1\. Ready to go|Y|11,700|65%|65%|65%|
|FSC|AC|Air Canada|1\. Ready to go|Y|8,955|69%|69%|69%|
|LCC|W4|Wizz Air Malta|1\. Ready to go|Y|8,879|97%|97%|97%|
|FSC|EY|Etihad Airways|1\. Ready to go|Y|7,849|87%|87%|87%|
|FSC|QF|Qantas|1\. Ready to go|Y|7,770|69%|69%|69%|
|FSC|BA|British Airways|1\. Ready to go|Y|7,480|57%|57%|57%|
|FSC|LH|Lufthansa|1\. Ready to go|Y|6,846|78%|77%|77%|
|LCC|W6|Wizz Air|1\. Ready to go|Y|6,744|97%|97%|97%|
|FSC|AA|American Airlines|1\. Ready to go|Y|6,030|79%|79%|79%|
|FSC|IB|Iberia|1\. Ready to go|Y|5,504|69%|68%|68%|
|LCC|W9|Wizz Air Italy|1\. Ready to go|Y|5,030|95%|95%|95%|
|FSC|KL|KLM|1\. Ready to go|Y|4,469|95%|94%|94%|
|FSC|AF|Air France|1\. Ready to go|Y|4,399|95%|94%|94%|
|FSC|LX|Swiss International|1\. Ready to go|Y|2,037|91%|91%|91%|
|FSC|OS|Austrian Airlines|1\. Ready to go|Y|1,346|91%|90%|90%|
|LCC|VB|VivaAerobus|1\. Ready to go|Y|1,338|96%|96%|94%|
|FSC|PG|Bangkok Airways|2\. Missing coverage||10,207|67%|67%|67%|
|FSC|TP|TAP Air Portugal|2\. Missing coverage||5,697|93%|93%|93%|
|FSC|LA|LATAM Airlines|2\. Missing coverage||5,649|94%|94%|94%|
|LCC|EW|Eurowings|2\. Missing coverage||5,562|98%|97%|97%|
|FSC|UX|Air Europa|2\. Missing coverage||5,337|56%|56%|56%|
|FSC|SK|Scandinavian Airlines|2\. Missing coverage||3,873|81%|79%|79%|
|FSC|A3|Aegean Airlines|2\. Missing coverage||3,566|92%|92%|92%|
|FSC|AY|Finnair|2\. Missing coverage||2,987|81%|80%|75%|
|FSC|LO|LOT Polish Airlines|2\. Missing coverage||2,947|78%|78%|78%|
|FSC|GF|Gulf Air|2\. Missing coverage||1,561|68%|68%|68%|
|FSC|CM|Copa Airlines|3\. Missing coverage/tier||2,030|66%|66%|33%|
|FSC|BR|EVA Air|3\. Missing tier|Y|71,537|63%|63%|0%|
|FSC|JL|Japan Airlines|3\. Missing tier|Y|22,438|74%|49%|0%|
|LCC|VF|Valuair|3\. Missing tier|Y|17,865|97%|94%|47%|
|FSC|DL|Delta Air Lines|3\. Missing tier|Y|7,348|73%|72%|0%|
|FSC|VS|Virgin Atlantic|3\. Missing tier|Y|1,693|68%|67%|0%|
|LCC|FD|Thai AirAsia<br>|3\. Missing official mapping|Y<br>|118,934|94%|30%|30%|
|LCC|VN|Vietnam Airlines|4\. Low brand info|Y|45,767|34%|34%|34%|
|FSC|JX|Starlux Airlines|4\. Low brand info||22,513|17%|17%|17%|
|FSC|GA|Garuda Indonesia|4\. Low brand info|Y|8,653|13%|10%|0%|
|FSC|AS|Alaska Airlines|4\. Low brand info|Y|3,585|9%|8%|8%|
|FSC|AV|Avianca|4\. Low brand info||3,253|10%|10%|10%|
|FSC|HA|Hawaiian Airlines|4\. Low brand info||1,212|10%|10%|6%|

1. Ready to go: 34

2. Missing coverage \(probably easy to add\): 10

3. Missing coverage and/or tier and/or official mapping \(Need manual support from backend to add brand tier mapping\): 7

4. Low brand info \(potentially technical limitations\): 6

## Primary data source

1. **Subset of fare comparison log data** \(2026\-04\-01 Wed\)

    - HIVE:`dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di`[idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/HIVE/dw_fltdb/adm_rsc_engine_airline_route_brand_detail_di)

    - BQ: `trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_adm_rsc_engine_airline_route_brand_detail_di`[idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/BIGQUERY/trip-ibu-bi-dw-etl.ibu_bi_dw_source/dw_fltdb_adm_rsc_engine_airline_route_brand_detail_di)

    - This is a subset of fare comparison log data, adding additional fields such haul type, gambling / lowest price tag etc\.

    - Covers ?? airlines \(FR/TO/VY/Wizz were added from the last week of Jan\), Y\+W/S, 1\-Meta only, flightway S/D, 2026 YTD

    - Source SQL code

    ```SQL
    with base_data as 
    (
        select tmp4.*
              , c1.countrycode as depart_countrycode
              , c2.countrycode as arrival_countrycode
              , c3.countrycode as vc_countrycode
              , tpm.haultype   as haultype
              -- 拆解航班号，提取航司二字码（MC：市场承运航司），生成数组
              , transform(split(regexp_replace(allroutefltno, '\\|', ','), ','), x -> substr(x, 1, 2)) as mc_array
              -- 去重后统计MC航司数量
              , size(array_distinct(transform(split(regexp_replace(allroutefltno, '\\|', ','), ','), x -> substr(x, 1, 2)))) as mc_cnt
              -- 拆解实际承运航班号，提取航司二字码（OC：实际承运航司），生成数组（过滤'NU'）
              , array_remove(transform(split(regexp_replace(allrouteoperatingfltno, '\\|', ','), ','), x -> substr(x, 1, 2)), 'NU') as oc_array
                -- 去重后统计OC航司数量
              , size(array_distinct(array_remove(transform(split(regexp_replace(allrouteoperatingfltno, '\\|', ','), ','), x -> substr(x, 1, 2)), 'NU'))) as oc_cnt
        from (
              -- 多层lateral view拆解：将按分隔符拼接的字符串（品牌、航班号等）拆分为单行
              select distinct dcitycode
                  , acitycode
                  , dairport
                  , aairport
                  , vc
                  , output
                --   , ctripbrandtier
                --   , oribrandname
                  , enginetype
                  , reservationtype
                  , traceid
                  , brandname_part2
                  , atpcobrandname_part2
                  , substr(fltno_part2, 1, 2) as mc
                  , case when optfltno_part2 = 'NULL' then null else substr(optfltno_part2, 1, 2) end as oc
                  , carbin
                  , txid
                  , middlebatchid
                  , allroutefltno
                  , allrouteoperatingfltno
                  , showbrandname
                  , atpcobrandname
                  , seatgrade
                  , brandtier 
                  , triptype
                  , islowprice
                  , orgagentcode
                  , advance_days
                  , pre_load_click_type
              from 
              (
                select distinct brandname_part2
                    , atpcobrandname_part2
                    , fltno_part2
                    , optfltno_part2
                    , dcitycode
                    , acitycode
                    , dairport
                    , aairport
                    , vc
                    , output
                    -- , ctripbrandtier
                    -- , oribrandname
                    , enginetype
                    , reservationtype
                    , traceid
                    , carbin
                    , txid
                    , middlebatchid
                    , allroutefltno
                    , allrouteoperatingfltno
                    , showbrandname
                    , atpcobrandname
                    , seatgrade
                    , brandtier 
                    , triptype
                    , islowprice
                    , orgagentcode
                    , advance_days
                    , pre_load_click_type
                from 
                (
                  select distinct brandname_part1
                        , atpcobrandname_part1
                        , fltno_part1
                        , optfltno_part1
                        , dcitycode
                        , acitycode
                        , dairport
                        , aairport
                        , vc
                        , output
                        -- , ctripbrandtier
                        -- , oribrandname
                        , enginetype
                        , reservationtype
                        , traceid
                        , carbin
                        , txid
                        , middlebatchid
                        , allroutefltno
                        , allrouteoperatingfltno
                        , showbrandname
                        , atpcobrandname
                        , seatgrade
                        , brandtier 
                        , triptype
                        , islowprice
                        , orgagentcode
                        , advance_days
                        , pre_load_click_type
                  from 
                  (
                        select 
                               dcitycode
                               , acitycode
                               , dairport
                               , aairport
                               , vc
                               , output
                               , showbrandname
                               , atpcobrandname
                            --   , ctripbrandtier
                               , enginetype
                               , reservationtype
                               , traceid
                               , txid
                               , middlebatchid
                               , allroutefltno
                               , allrouteoperatingfltno
                               , carbin
                               , seatgrade
                               , brandtier 
                               , triptype
                               , islowprice
                               , orgagentcode
                               , advance_days
                               , pre_load_click_type
                        from 
                        (
                              -- 原始数据源：国际航班比价聚合日志表
                              select split(searchcityroute, '\\|')[0] as dcitycode      -- 出发城市码
                              , split(searchcityroute, '\\|')[1] as acitycode           -- 到达城市码
                              , split(split(allrouteairport, '\\|')[0], ',')[0]              as dairport            -- 出发机场
                              , element_at(split(split(allrouteairport, '\\|')[0], ','), -1) as aairport            -- 到达机场
                              , vc                                                      -- 出票航司
                              , output                                                  -- 比价是否输出（true/false）
                              , lower(showbrandname) as showbrandname                   -- show品牌名称
                              -- Ctrip场景下，优先用brandname填充atpcobrandname（因字段落地不全）
                              , case when enginetype in ('Ctrip', 'CtripNDC') then coalesce(lower(brandname),lower(atpcobrandname)) 
                                     else lower(atpcobrandname) end as atpcobrandname   -- atpco品牌名
                            --   , ctripbrandtier                                       -- 携程品牌层级
                              , enginetype                                              -- 引擎
                              , reservationtype                                         -- 预订类/报价来源
                              , coalesce(middlebatchid,traceid) as traceid               -- 唯一追踪ID（优先middlebatchid）
                              , txid
                              , middlebatchid
                              , brandtier                                               --待定，品牌等级
                              -- 舱位等级映射（数字转字符）
                              , CASE
                                WHEN seatgrade = 1 THEN 'Y'
                                WHEN seatgrade = 2 THEN 'W'
                                WHEN seatgrade = 3 THEN 'Y,W'
                                WHEN seatgrade = 4 THEN 'C'
                                WHEN seatgrade = 5 THEN 'Y,C'
                                WHEN seatgrade = 6 THEN 'W,C'
                                WHEN seatgrade = 8 THEN 'F'
                                WHEN seatgrade = 9 THEN 'Y,F'
                                WHEN seatgrade = 10 THEN 'W,F'
                                WHEN seatgrade = 12 THEN 'C,F'
                                ELSE ''
                                END AS seatgrade
                              , allrouteairport             -- 机场信息
                              , allroutefltno               -- 全航线市场承运航班号
                              , allrouteoperatingfltno      -- 全航线实际承运航班号
                              , triptype                    -- 行程类型
                              , islowprice                  -- 是否最低价
                              , orgagentcode                -- orgagentcode不为空就是对赌
                              , datediff(cast(substr(allrouteddate,1,10) as date),cast(substr(requestdate,1,10) as date)) as advance_days -- 提前期
                              , pre_load_click_type
                              from dw_fltlogdata.flight_intl_agg_analysis_compareresult_log_etl 
                              where d = '${pre_date}' 
                            --   where d = '2026-02-01'  
                              and upper(channel) = 'ENGLISHSITE' -- 仅处理英文站点
                              and enginetype <> 'CombinedPU' -- 排除多票场景
                              and triptype <> 4  -- 排除多程
                              and length(searchcityroute) = 7 -- 仅单程/往返
                              and pre_load_click_type <> 'unclicked' -- 排除预加载
                              and ((subchannel >= 0) AND (subchannel < 20) OR (subchannel >= 1000)) -- 主站
                              -- 重点航司过滤
                            --   and vc in ('BR','CA','CI','CX','CZ','GA','HX','JL','MH','MU','NH','OZ','PR','QF','SQ','TG','VN','AF','BA','IB','KL','LH','LX','OS','TK','VS','AS','EK','EY','QR','AA','AC','DL','UA','KE','AZ')
                        ) tmp0
                        -- 拆解舱位（将Y,W拆分为单行）
                        lateral view explode(split(seatgrade,',')) cabins as carbin
                      ) tmp1
                  -- 拆解展示品牌、实际品牌、市场承运航班号、实际承运航班号（按分隔符拆分）
                  lateral view posexplode(split(showbrandname,';')) brand as pos1, brandname_part1
                  lateral view posexplode(split(atpcobrandname,';')) atpcobrand as pos2, atpcobrandname_part1
                  lateral view posexplode(split(allroutefltno,'\\|')) fltno as pos3, fltno_part1
                  lateral view posexplode(split(allrouteoperatingfltno,'\\|')) optfltno as pos4, optfltno_part1
                  -- 保证拆分后字段的位置匹配（避免错位）
                  where pos1 = pos2 and pos3 = pos4 and (showbrandname = '' or atpcobrandname = '' or pos1 = pos3 or pos2 = pos3)
                ) tmp2
            -- 二次拆解（处理多层拼接的字符串）
            lateral view posexplode(split(brandname_part1,'\\|')) brand as pos1, brandname_part2
            lateral view posexplode(split(atpcobrandname_part1,'\\|')) brand as pos2, atpcobrandname_part2
            lateral view posexplode(split(fltno_part1,',')) fltno as pos3, fltno_part2
            lateral view posexplode(split(optfltno_part1,',')) optfltno as pos4, optfltno_part2
            where pos1 = pos2 and pos3 = pos4 and (showbrandname = '' or atpcobrandname = '' or pos1 = pos3 or pos2 = pos3)
          ) tmp3
        ) tmp4
        -- 关联城市维度表，获取出发/到达国家码
        left join dim_fltdb.dimcity c1 
        on c1.citycode = tmp4.dcitycode
        left join dim_fltdb.dimcity c2 
        on c2.citycode = tmp4.acitycode
        left join dim_fltdb.dimtpm tpm 
        on tpm.dcitycode = tmp4.dcitycode and tpm.acitycode = tmp4.acitycode 
        left join dim_fltdb.dimairline c3   --获取航司所在国家
        on tmp4.vc = c3.airline
    ),
    compareresult_log_etl_result as (
        select t1.*
             , case when depart_countrycode = arrival_countrycode and  depart_countrycode = vc_countrycode and arrival_countrycode = vc_countrycode then 'Dom'
                    when depart_countrycode <> arrival_countrycode or depart_countrycode <> vc_countrycode or arrival_countrycode <> vc_countrycode then 'Intl'
                    else 'Unknown' 
                    end as airline_type
            --  , case when oc is null and mc = vc and mc_cnt = 1 then 'T'
            --         when oc is not null and mc = vc and mc = oc and vc = oc then 'T'
            --         -- 汉莎集团（LH/LX/OS/4Y）的报价
            --         when  vc in ('LH','LX','OS','4Y') AND mc in ('LH','LX','OS','4Y') and (oc in ('LH','LX','OS','4Y','null') or oc is null) then 'T'
            --         else 'F' end as is_own
             , case when ((vc = mc and mc_cnt = 1 and oc_cnt = 0) or (vc in ('LH','LX','OS','4Y') AND mc in ('LH','LX','OS','4Y') and (oc in ('LH','LX','OS','4Y','null') or oc is null))) then 'T' else 'F' end as is_own
             , case when orgagentcode is not null and trim(orgagentcode) <> '' then 'T' else 'F' 
                    end as is_gambling
             , case when triptype = '1' then 'OW'
                    when triptype = '2' then 'RT'
                    when triptype = '4' then 'MT'
                 end as triptype_str
             , t2.brandname
             , t2.enname 
             , t2.routeattributes
             , t2.airlinebrandtier
        from base_data t1
        left join
        (
            select brandname, enname, carrier, applicablecabin, routeattributes, airlinebrandtier
            from ods_fltairtickets_mysql_fltresourcedb.tb_brandname_unified
            where d = '${pre_date}' and officialBrandname = '1'
            group by brandname, enname, carrier, applicablecabin, routeattributes, airlinebrandtier
        ) t2
        on t1.vc  = t2.carrier 
        and upper(t1.carbin) = upper(t2.applicablecabin)
        and replace(t1.atpcobrandname_part2, ' ', '') = replace(lower(t2.brandname), ' ', '')
    )
    insert overwrite dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di partition(d = '${pre_date}')
    select traceid                -- 用户查询的id
           , vc                   -- 出票航司
           , atpcobrandname_part2 as atpcobrandname       -- 资源侧的品牌名
           , showbrandname        -- 对客的品牌名
           , brandtier            -- 品牌等级
           , carbin               -- 舱等
           , enginetype           -- 引擎
           , reservationtype      -- 订位类型
           , dairport             -- 出发机场
           , aairport                 -- 到达机场
           , dcitycode            -- 出发城市
           , acitycode            -- 到达城市码
           , depart_countrycode
           , arrival_countrycode
           , haultype
           , airline_type
           , advance_days
           , triptype_str
           , is_own
           , case when islowprice = '1' then 'T' when islowprice = '0' then 'F' else null end as is_low_price
           , is_gambling
           , brandname
           , enname
           , case when output = 'true' then 'T' when output = 'false' then 'F' else null end as is_output
           , routeattributes
           , airlinebrandtier
    from compareresult_log_etl_result
    ```

    - This is at trace id level\. Each row = one trace id and one of the fares under this trace id\. E\.g\. If there are 2 traceid, each has 10 fares, then we will get 20 rows\.

2. **Brand fare high\-level coverage database** \(2026\-04\-01 Wed\)

    - HIVE:`dw_fltdb.adm_rsc_engine_airline_route_brand_cover_di`[idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/HIVE/dw_fltdb/adm_rsc_engine_airline_route_brand_cover_di)

    - BQ: not sync yet

    - Source SQL code

    ```SQL
    -- 聚合表，包含22个指标
    -- 比价前后:总查询量,vc=mc=oc 查询量,有品牌报价的查询量,vc=mc=oc有品牌报价的查询量,品牌为最低价的查询量,品牌是对赌产品的查询量
    -- 品牌覆盖率,vc=mc=oc 场景的品牌覆盖率,品牌是最低价的比例, 品牌是对赌的比例, 品牌是最低价且是对赌的比例
    -- 理论航线范围: 历史一段时间内出现过指定品牌名报价的航线范围，按照航司+atpco品牌名+atpco转换后+机场对聚合
    WITH routes AS (
        SELECT 
            vc, 
            class, 
            atpco_brand_name, 
            standard_brand_name as brandname, 
            standard_display_brand_name as enname, 
            dep_airport_code, 
            arr_airport_code
        FROM dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di
        where d >= '${pre_90date}' 
        and atpco_brand_name is not null
        -- standard_brand_name is not null and standard_display_brand_name is not null
        GROUP BY vc, class, atpco_brand_name, standard_brand_name, standard_display_brand_name, dep_airport_code, arr_airport_code
    ),
    -- 近90天内出现的品牌和其对应的航线的映射关系
    brand_route_res as (
      select carrier
            , brandname
            , enname 
            , applicablecabin
            , dep_airport_code
            , arr_airport_code
            from 
            (
              select t1.*
                     , t2.dep_airport_code
                     , t2.arr_airport_code
              from 
              (
                select carrier, brandname,enname, applicablecabin
                from ods_fltairtickets_mysql_fltresourcedb.tb_brandname_unified
                where d = '${pre_date}' and officialBrandname = '1'
                group by brandname, enname, carrier, applicablecabin
              ) t1
              left join 
              (
                select vc
                      -- , atpco_brand_name
                      , class
                      , brandname
                      , enname
                      , dep_airport_code
                      , arr_airport_code
                from routes
              ) t2
              on replace(lower(t1.brandname), ' ', '') = replace(lower(t2.brandname), ' ', '')
            --   on t1.brandname = t2.brandname
              and replace(lower(t1.enname), ' ', '') = replace(lower(t2.enname), ' ', '')
            --   and t1.enname = t2.enname
              and t1.carrier = t2.vc
              and t1.applicablecabin = t2.class
            ) 
            group by carrier, brandname, enname, applicablecabin, dep_airport_code, arr_airport_code
    )
    -- select * from brand_route_res
    insert overwrite dw_fltdb.adm_rsc_engine_airline_route_brand_cover_di partition(d = '${pre_date}')
    select vc
            , class
            , brandname
            , total_cnt 
            , has_brand_name_cnt
            , own_cnt
            , own_has_brand_name_cnt
            , lowest_has_brand_name_cnt
            , vam_has_brand_name_cnt
            , vam_has_brand_name_lowest_cnt
            , has_brand_name_cnt / total_cnt as brand_coverage                       -- 品牌覆盖率
            , own_has_brand_name_cnt / own_cnt as own_brand_coverage                 -- 自营品牌的覆盖率
            , lowest_has_brand_name_cnt / has_brand_name_cnt as lowest_brand_coverage -- 品牌是最低价的比例
            , vam_has_brand_name_cnt / has_brand_name_cnt    as vam_brand_coverage    -- 品牌是对赌的比例
            , vam_has_brand_name_lowest_cnt /  has_brand_name_cnt as vam_brand_lowest_coverage -- 品牌是对赌且最低价的比例
            --比价后
            , output_total_cnt
            , output_has_brand_name_cnt
            , output_own_cnt
            , output_own_has_brand_name_cnt
            , output_lowest_has_brand_name_cnt
            , output_vam_has_brand_name_cnt
            , output_vam_has_brand_name_lowest_cnt
            , output_has_brand_name_cnt / output_total_cnt as output_brand_coverage                       -- 品牌覆盖率
            , output_own_has_brand_name_cnt / output_own_cnt as output_own_brand_coverage                 -- 自营品牌的覆盖率
            , output_lowest_has_brand_name_cnt / output_has_brand_name_cnt as output_lowest_brand_coverage -- 品牌是最低价的比例
            , output_vam_has_brand_name_cnt / output_has_brand_name_cnt    as output_vam_brand_coverage     -- 品牌是对赌的比例
            , output_vam_has_brand_name_lowest_cnt /  output_has_brand_name_cnt as output_vam_brand_lowest_coverage -- 品牌是对赌且最低价的比例
            , null
            , airline_brand_tier
            , engine_type
            , rsv_type
    from 
    (
      select vc, class, brandname,
            select vc, class, brandname,
           -- 比价前
            count(DISTINCT traceid) as total_cnt, -- 总查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as has_brand_name_cnt, -- 有品牌报价的查询量
            count(DISTINCT case when is_own = 'T' then traceid end) as own_cnt, -- vc=mc=oc 查询量
            count(DISTINCT case when is_own = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as own_has_brand_name_cnt,  -- vc=mc=oc有品牌报价的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and  is_lowest_price = 'T' then traceid end) as lowest_has_brand_name_cnt,   -- 品牌为最低价的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' then traceid end) as vam_has_brand_name_cnt,                         -- 品牌是对赌产品的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' and is_lowest_price = 'T'  then traceid end) as vam_has_brand_name_lowest_cnt,                         -- 品牌是对赌产品且是最低价的查询量
            
            --比价后
            count(DISTINCT case when is_output = 'T' then traceid end) as output_total_cnt, -- 总查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as output_has_brand_name_cnt, -- 有品牌报价的查询量
            count(DISTINCT case when is_output = 'T' and is_own = 'T' then traceid end) as output_own_cnt, -- vc=mc=oc 查询量
            count(DISTINCT case when is_output = 'T' and is_own = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as output_own_has_brand_name_cnt,  -- vc=mc=oc有品牌报价的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and  is_lowest_price = 'T' then traceid end) as output_lowest_has_brand_name_cnt,   -- 品牌为最低价的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' then traceid end) as output_vam_has_brand_name_cnt,                         -- 品牌是对赌产品的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' and is_lowest_price = 'T'  then traceid end) as output_vam_has_brand_name_lowest_cnt
      from 
          (
            select t2.*, t1.enname as brandname
            from brand_route_res  t1
            left join dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di t2
            on t2.vc = t1.carrier
            -- and t1.standard_brand_name = t2.brandname
            -- and t1.standard_display_brand_name = t2.enname
            and t2.class = t1.applicablecabin
            and t1.dep_airport_code = t2.dep_airport_code
            and t1.arr_airport_code = t2.arr_airport_code
            AND t2.d = '${pre_date}'
          )
      group by vc, class, brandname, engine_type, rsv_type, airline_brand_tier
    )
    union all 
    
    --预订时间间隔范围（一周，一个月，三个月+）查询覆盖率
    select vc
            , class
            , brandname
            , total_cnt 
            , has_brand_name_cnt
            , own_cnt
            , own_has_brand_name_cnt
            , lowest_has_brand_name_cnt
            , vam_has_brand_name_cnt
            , vam_has_brand_name_lowest_cnt
            , has_brand_name_cnt / total_cnt as brand_coverage                       -- 品牌覆盖率
            , own_has_brand_name_cnt / own_cnt as own_brand_coverage                 -- 自营品牌的覆盖率
            , lowest_has_brand_name_cnt / has_brand_name_cnt as lowest_brand_coverage -- 品牌是最低价的比例
            , vam_has_brand_name_cnt / has_brand_name_cnt    as vam_brand_coverage    -- 品牌是对赌的比例
            , vam_has_brand_name_lowest_cnt /  has_brand_name_cnt as vam_brand_lowest_coverage -- 品牌是对赌且最低价的比例
            --比价后
            , output_total_cnt
            , output_has_brand_name_cnt
            , output_own_cnt
            , output_own_has_brand_name_cnt
            , output_lowest_has_brand_name_cnt
            , output_vam_has_brand_name_cnt
            , output_vam_has_brand_name_lowest_cnt
            , output_has_brand_name_cnt / output_total_cnt as output_brand_coverage                       -- 品牌覆盖率
            , output_own_has_brand_name_cnt / output_own_cnt as output_own_brand_coverage                 -- 自营品牌的覆盖率
            , output_lowest_has_brand_name_cnt / output_has_brand_name_cnt as output_lowest_brand_coverage -- 品牌是最低价的比例
            , output_vam_has_brand_name_cnt / output_has_brand_name_cnt    as output_vam_brand_coverage     -- 品牌是对赌的比例
            , output_vam_has_brand_name_lowest_cnt /  output_has_brand_name_cnt as output_vam_brand_lowest_coverage -- 品牌是对赌且最低价的比例
            , airline_brand_tier
            , sch_advance_type
            , engine_type
            , rsv_type
    from 
    (
      select vc, class, brandname,
           -- 比价前
            count(DISTINCT traceid) as total_cnt, -- 总查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as has_brand_name_cnt, -- 有品牌报价的查询量
            count(DISTINCT case when is_own = 'T' then traceid end) as own_cnt, -- vc=mc=oc 查询量
            count(DISTINCT case when is_own = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as own_has_brand_name_cnt,  -- vc=mc=oc有品牌报价的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and  is_lowest_price = 'T' then traceid end) as lowest_has_brand_name_cnt,   -- 品牌为最低价的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' then traceid end) as vam_has_brand_name_cnt,                         -- 品牌是对赌产品的查询量
            count(DISTINCT case when replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' and is_lowest_price = 'T'  then traceid end) as vam_has_brand_name_lowest_cnt,                         -- 品牌是对赌产品且是最低价的查询量
            
            --比价后
            count(DISTINCT case when is_output = 'T' then traceid end) as output_total_cnt, -- 总查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as output_has_brand_name_cnt, -- 有品牌报价的查询量
            count(DISTINCT case when is_output = 'T' and is_own = 'T' then traceid end) as output_own_cnt, -- vc=mc=oc 查询量
            count(DISTINCT case when is_output = 'T' and is_own = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') then traceid end) as output_own_has_brand_name_cnt,  -- vc=mc=oc有品牌报价的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and  is_lowest_price = 'T' then traceid end) as output_lowest_has_brand_name_cnt,   -- 品牌为最低价的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' then traceid end) as output_vam_has_brand_name_cnt,                         -- 品牌是对赌产品的查询量
            count(DISTINCT case when is_output = 'T' and replace(lower(standard_display_brand_name), ' ', '') = replace(lower(brandname), ' ', '') and is_vam = 'T' and is_lowest_price = 'T'  then traceid end) as output_vam_has_brand_name_lowest_cnt,
            sch_advance_type
            -- , airline_brand_tier
            -- , engine_type
            -- , rsv_type
      from 
          (
            select t2.*, t1.enname as brandname,
            case when t2.sch_advance_day = 7 then '7天'
                 when t2.sch_advance_day = 30 then '30天'
                 when t2.sch_advance_day > 90 then '90+天'
                 else 'unknown'
                 end as sch_advance_type
            from brand_route_res  t1
            left join dw_fltdb.adm_rsc_engine_airline_route_brand_detail_di t2
            on t2.vc = t1.carrier
            -- and t1.standard_brand_name = t2.brandname
            -- and t1.standard_display_brand_name = t2.enname
            and t2.class = t1.applicablecabin
            and t1.dep_airport_code = t2.dep_airport_code
            and t1.arr_airport_code = t2.arr_airport_code
            and (t2.sch_advance_day = 7 or t2.sch_advance_day = 30 or t2.sch_advance_day > 90)
            AND t2.d = '${pre_date}'
            
          )
      group by vc, class, brandname, sch_advance_type, engine_type
            , rsv_type, airline_brand_tier
    )
    ```

    - Dashboard: https://nova\.ops\.ctripcorp\.com/\#/dashboard/ee58ad8d\-c1e8\-420e\-8e7f\-39f7a5201fc9

3. **Brand fare granular coverage database** \(2026\-03\-26 Thu\)

    - HIVE:

    - BQ:`trip-ibu-bi-dw-etl.ibu_bi_dw_source.dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di` [idata link](https://metadata.ops.sgp.tripws.com/#/metadata/BIGQUERY/trip-ibu-bi-dw-etl.ibu_bi_dw_source/dw_fltdb_adm_rsc_engine_airline_route_brand_cover_v2_di)

    - Source SQL code \(TBU\)

    - Almost the same as above but with more granular dimension aggregations \(at airport, country, reservation type, and engine type level\)\.

    - Data available from 2026\-01\-31

    1. Filter to the right aggregation level before pulling any data using `idx_dim`

        1. \(2026\-04\-01 Wed\) Request to back fill the idx\_dim data

4. **Brand Fare Mapping/Profile Database**

    - HIVE: `ods_fltairtickets_mysql_fltresourcedb.tb_brandname_unified` [idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/HIVE/ods_fltairtickets_mysql_fltresourcedb/tb_brandname_unified)

    - BQ: `trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`[idata link](https://metadata.ops.sgp.tripws.com/#/metadata/BIGQUERY/trip-ibu-bi-dw-etl.ibu_bi_dw_source/ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified)

    - According to **Miao** **2026\-04\-02**

        > `tb_brandname_unified`覆盖生产所有航司的品牌数据，但是对于品牌的airlinebrandtier等属性定义，只有部分航司做了手工梳理，这部分和飞书文档中的航司基本是对齐的。
        > 
        > 对于BR航司有点特殊，在之前手工梳理的时候，BR还没授权给携程，所以当时没法做梳理，后来做了tier的补齐。
        > 
        > 

    - Namely, this table has two mappings: brand name to ennames \- 

    - Coverage: \~50 airlines \(TBU\), they were selected by Lyrics\. The exact criteria is unknown\. Can refer to [B03\.Fare Family](https://trip.larkenterprise.com/docx/I02Jd6NhRo60v2xTObgcXQSVn3g)

    - One\-time manually map atpco brand names to airline official website brand name if attribute matches, and assign an airline brand tier to each official website brand name

    - No plan to expand the scope of the airlines unless we requested \(due to capability restrictions and priority\)

    - Detailed attributes per fare can be found here [航司品牌运价与选座权益](https://trip.larkenterprise.com/base/ZZxMbp7I1aZ4disN2AgcHOEAnjd?table=tbluVPbpkK5Rftm1&view=vewBHLaAGe)

    - Note that

        - official brand fare, airline brand tier doesn't seem to be very consistently tagged \(maybe due to rush work\)\. Use active = '1' as filter to get all the possible brand name \<\> enname mapping

        - In order data, use atpco name to map to brand fare database, the airline tier is not reliable in the segment order table

5. **Order \(segment\) level Brand Data ****\(\(2026\-04\-01 Wed TBU\)**

    - HIVE: `systemdataflowanalysisdb.dim_log_other_order_seg_detail_with_brand_di` [idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/HIVE/systemdataflowanalysisdb/dim_log_other_order_seg_detail_with_brand_di) and several other data sources \(see the HIVE code below\)

    ```SQL
    ----------------------------------------------------------------
    --comment auto generated by zeus
    --名称：宽表
    --功能描述：品牌订单明细表
    --创建人：sunyh
    --创建时间：2025-06-25
    --运行类型： 
    --注意事项：
    --修改历史：修改人    / 修改时间  / 主要改动说明
    --      1. SUN YIHUI / 2025-06-25 / 创建流程
    ----------------------------------------------------------------
    USE systemdataflowanalysisdb;
    
    INSERT OVERWRITE TABLE systemdataflowanalysisdb.dim_log_other_order_seg_detail_with_brand_di PARTITION(d='${pre1_date}') 
    SELECT 
      substr(b.orderdate,1,10) AS date
      ,b.orderid
      ,b.bookingchannel
      ,b.subchannel
      ,b.realreservationtype
      ,b.ownerairline
      ,e.sequence
      ,if(e.sequence = 1, b.quantity, 0) AS order_quantity          -- 订单维度的航段量
      ,b.persons AS tier_quantity
      ,if(AddtionalInfo.orderid is not null,1,0) as is_repricing
      ,e.tripbrandtier
      ,''
      ,e.dport
      ,e.aport
      ,e.flightno
      ,e.classname
      ,b.source
      ,e.brandname
      ,e.attributeid_list
      ,e.service_name_list
      ,e.atpco_level_list
      ,e.service_group_list
      ,ma.market
      ,e.data_src
      ,e.abt
      -- 公布转HO——DIRCT（262144），2025-08-21，接口不是NDC标准，因此排除在NDC reservationtype以外
      ,if(b.realreservationtype in (1024,4096,8192,32768,256,1048576)
        AND b.bookingChannel in ('TSK-NDC','SCD-WS','PROS-WS','TF-WS','MUC-NDC','MUT-NDC','MFN-WS','CZD-WS','GDS-WS','1A-WS','1T-WS'),1,0) as is_ndc_order
      ,if(e.abt is not null and abt != 0 and abt > brand.airlinebrandtier,1,0) as is_upsell
      -- 加入oversea表信息2025-08-25(为对齐oversea表)
      -- ,if(e.sequence = 1, overseasteam_orderdetail.segments, 0) as oversea_quantity
      -- ,if(e.sequence = 1, overseasteam_orderdetail.bookinggds, 0) as oversea_bookinggds
      -- ,if(e.sequence = 1, overseasteam_orderdetail.orderbrand, 0) as oversea_orderbrand
      -- ,if(e.sequence = 1, overseasteam_orderdetail.brandname, 0) as oversea_brandname
      -- ,if(e.sequence = 1, overseasteam_orderdetail.class, 0) as oversea_class
      -- ,if(e.sequence = 1, overseasteam_orderdetail.tpm, 0) as oversea_tpm
      -- ,b.orderstatus
      -- ,b.is_except_order
      -- ,overseasteam_orderdetail.orderdate as oversea_orderdate
      ,brand.airlinebrandtier as airlinebrandtier
      ,e.sbn as sbn
      ,e.obn as obn
      ,e.abn as abn
      ,'' as oversea_class
      ,'' as oversea_tpm
      ,'' as orderstatus
      ,'' as is_except_order
      ,'' as oversea_orderdate
    FROM 
    (
      select orderid,
              orderdate,
              quantity,
              persons,
              bookingchannel,
              flightclass,
              uid,
              orderstatus,
              manualset,
              realreservationtype,
              source,
              subchannel,
              ownerairline
      from flt_bidb.v_ffo
    ) as b
    -- 加入航段表
    INNER JOIN 
    (
        SELECT fa.orderid,
                    fa.tripbrandtier,
                    fa.brandname,
                    fa.abt,
                    fa.sbn,
                    fa.obn,
                    fa.abn,
                    fa.sequence,
                    fa.dport,
                    fa.aport,
                    fa.flightno,
                    fa.classname,
                    fa.data_src,
                    fa.d,
                    case when fa.classname = '头等舱' then 'F'
              when fa.classname = '超级经济舱' then 'W'
              when fa.classname = '公务舱' then 'C'
              when fa.classname = '经济舱' then 'Y' end cabin,
            concat_ws(',', collect_list(get_json_object(fa.attributeid, '$.id'))) as attributeid_list,
            concat_ws(',', collect_list(fb.service_name)) as service_name_list,
            concat_ws(',', collect_list(fb.atpco_level)) as atpco_level_list,
            concat_ws(',', collect_list(fb.service_group)) as service_group_list
        FROM
        (
          SELECT orderid
            ,tripbrandtier
            ,brandname
            ,abt,sbn,obn,abn
            ,sequence
                    ,dport
                    ,aport
                    ,flightno
                    ,classname
                    ,data_src
            ,d
            ,explode_outer(split(replace(replace(brandattributes,'[',''),']',''),',')) as attributeid 
          FROM 
          (
            SELECT orderid,
                    get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.ctripbrandtier') as tripbrandtier,
                    get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.attributes') as brandattributes,
                    get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.brandname') as brandname,
                    get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.abt') as abt,
                    get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.sbn') as sbn,
                get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.obn') as obn,
                get_json_object(substr(interestsattribute,2,length(interestsattribute)-2), '$.abn') as abn,
                    sequence,
                            dport,
                            aport,
                            flightno,
                            classname,
                            data_src,
                            d 
            FROM flt_bidb.dw_factfltsegment
            WHERE d = date_sub(current_date,1) 
                    AND flightclass = 'I'
          )
        ) fa
        left join 
        (
          SELECT id,service_name,atpco_level,service_group 
          FROM ods_fltairtickets_mysql_fltintlenginedb.tb_service_mapping 
          WHERE d = date_sub(current_date,1) 
          AND is_delete = 0
        ) fb
        on get_json_object(fa.attributeid, '$.id') = [fb.id](http://fb.id)
        group by orderid,tripbrandtier,brandname,abt,sbn,obn,abn,sequence,dport,aport,flightno,classname,data_src,d
    ) as e
    ON b.orderid = e.orderid
    -- 加入Market
    LEFT JOIN
    (
      SELECT distinct upper(channel) as channel,subchannel,market 
      FROM ods_fltairtickets_mysql_fltbasedatadb.bd_channelconfiginfo
      WHERE d = date_sub(current_date,1) 
      AND isactivated = 1
    ) as ma
    ON ma.channel = b.source
    AND ma.subchannel = b.subchannel
    -- 加入Addtional
    LEFT JOIN 
    (
      SELECT orderid
      FROM ods_fltairtickets_mysql_fltintlbookingdb.flightadditionalinfo
      WHERE d = date_sub(current_date,1) 
      AND additionaltype = 'recommendprdtype2'
      AND ((CAST(additionalvalue AS BIGINT) & 35184372088832 = 35184372088832) OR 
        (CAST(additionalvalue AS BIGINT) & 4503599627370496 = 4503599627370496))
    ) as AddtionalInfo 
    ON b.orderid = AddtionalInfo.orderid
    -- add airlinebrandtier
    LEFT JOIN
    (
        SELECT carrier
            ,applicablecabin
            ,max(airlinebrandtier) as airlinebrandtier
        FROM ods_fltairtickets_mysql_fltresourcedb.tb_brandname_unified
        WHERE d = date_sub(current_date,1) 
        AND actived = '1'
        AND airlinebrandtier IS NOT NULL
        and upsell = 0
        group by carrier,applicablecabin
    ) as brand
    ON b.ownerairline = brand.carrier
    AND e.cabin = brand.applicablecabin
    WHERE b.flightclass = 'I'
    AND b.uid NOT IN ('HuaMeiYiDa','M351274275','M2555541076','M117699353','_U2662303168')
    AND b.orderstatus IN ('S', 'T', 'R')
    AND b.manualset = 'F'
    AND NOT (b.source = 'Affiliate' AND b.subchannel IN ('778105','108352','777122'))
    AND substr(b.orderdate,1,10) >= '2025-01-01' -- date_sub(current_date,120)
    ```

    ```SQL
    SELECT mocktable.odate AS d_0, SUM(mocktable.order_quantity) AS m_0, SUM(mocktable.brandtier_of_rate) AS m_1
            , SUM(mocktable.service_rate) AS m_2, SUM(mocktable.upsell_of_brandtier_rate) AS m_3
    FROM (
            SELECT odate, SUM(order_quantity) AS order_quantity
                    , SUM(if(tripbrandtier IS NOT NULL, tier_quantity, 0)) / SUM(order_quantity) AS brandtier_of_rate
                    , SUM(if(tripbrandtier IS NOT NULL
                            AND is_upsell = 1, tier_quantity, 0)) / SUM(if(tripbrandtier IS NOT NULL, tier_quantity, 0)) AS upsell_of_brandtier_rate
                    , AVG(CASE 
                            WHEN '0' != '0' THEN IF(service_group_list != ''
                                            AND instr(service_group_list, '0') > 0, 1, 0)
                            ELSE IF(service_group_list != '', 1, 0)
                    END) AS service_rate
            FROM systemdataflowanalysisdb.dim_log_other_order_seg_detail_with_brand_di a
                    INNER JOIN dim_fltdb.dimairline air ON a.ownerairline = air.airline
            WHERE d = date_sub(CURRENT_DATE, 1)
                    AND flight != ''
                    AND odate <= date_sub(CURRENT_DATE, 1)
                    AND 1 = 1
                    AND 1 = 1
                    AND 1 = 1
                    AND 1 = 1
                    AND 1 = 1
                    AND 1 = 1
                    AND 1 = 1
                    AND data_src IN ('sha', 'sgp')
            GROUP BY odate
    ) mocktable
    GROUP BY mocktable.odate
    ORDER BY d_0
    ```

    - BQ: `trip-ibu-bi-dw-etl.ibu_bi_dw_cdw.edw_prd_flt_factfltsegment_eng`[idata link](https://new.metadata.ops.ctripcorp.com/#/metadata/BIGQUERY/trip-ibu-bi-dw-etl.ibu_bi_dw_cdw/edw_prd_flt_factfltsegment_eng)

        - Note: IBU flattens the brand info directly on the seg table itself, rather than creating a new table like FBU did\. See the SQL below

    ```SQL
    
    ```

For detailed explanation of the above datasets, please refer to [Brand Fare Info Explain](https://trip.sg.larkenterprise.com/docx/J2yVdgkR3oxchyxTswwl3fiKgad) \(TBU\)\. It explains:

- Definition of different fields in each \(and related\) datasets

- Clarify the relationship of related fields \(same data may have different names in different datasets\)



Coverage data documentation from FBU: [航司品牌名航线查询覆盖](https://trip.larkenterprise.com/wiki/YNu2wJ9JXi0rMkkwGPVcKDFfnne)

4. **Front\-end Trace Database ****\(TBU\)**

    - HIVE:

    - BQ: `trip-ibu-bi-dw-etl.ibu_bi_dw_source.ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified`[idata link](https://metadata.ops.sgp.tripws.com/#/metadata/BIGQUERY/trip-ibu-bi-dw-etl.ibu_bi_dw_source/ods_fltairtickets_mysql_fltresourcedb_tb_brandname_unified)



- Raw refund/rebook data source

    - BQ: trip\-ibu\-bi\-dw\-etl\.ibu\_bi\_dw\_source\.flt\_bidb\_edw\_deal\_ref\_rbk\_intl\_info

- 

## Secondary data source \(good to know\)

1. **Fare comparison log data**

    - HIVE:`dw_fltlogdata.flight_intl_agg_analysis_compareresult_log_etl`

    - The "raw" table to build coverage database, includes all fares at traced and fare level for both meta and 1\-meta

2. **Crawler Data**** \(TBU\)**

    - Table: \[Table name from Fact Sheet\]

    - Purpose: Competitor fare comparison, coverage gap identification

## Others

- Data tables and dashboards collected by Vivi [Trip Upsell  —Analytics Framework \& Dataset Collection](https://trip.larkenterprise.com/wiki/AnxmwInO1iYkc1kWbzicOrt4njc)

- IBU Flight order data collection [机票订单数据](https://trip.larkenterprise.com/wiki/NCsCwdYD6ikBEZkdVxOcxOBSnvf)

- FBU x\-product data collection [辅营核心表](https://trip.larkenterprise.com/wiki/VzTkwVXT3iCmURkrFVRcgtmSnAh)

- **Middle page upsell rate dashboard**

    - https://artnova\.ops\.sgp\.tripws\.com/\#/dashboard/c30870d7\-6511\-429d\-820a\-acd9928b30cc

    - FBU's source of truth to track upsell rate \(incl\. meta \+ 1\-meta, all POS\)

    - Our upsell rate calculation matches their definition \(same filters, except ibu = 1\-meta vs fbu = both\)

- \(From Vivi\) https://artnova\.ops\.sgp\.tripws\.com/\#/configuration/dashboard/c6cdad1d\-3da6\-4ec3\-b6db\-d4e46a851fd1?defaultFirstNotLoad=1 \(by airline middle page performance\)

## Data Process \& Access

- Dataflow usage [上下云需求处理流程说明](https://trip.larkenterprise.com/wiki/A1cJwVNe2ihxS7kjLcJcYFg6nHf)

- Dataflow usage  [【数据同步】一键上云（Hive → BigQuery）](https://trip.larkenterprise.com/wiki/IyK9wRtPRiSqagkLo0Hc9tXqnYe)

- IBU data query tool access [2\.0 \[For All\] 新员工数据查询权限申请 \(中文\)](https://trip.larkenterprise.com/wiki/LTkKwg3DriynT4kLBVcc90Xdnye)

### [Brand fare coverage rate at middle page](https://nova.ops.ctripcorp.com/#/portal/FLT/FltIntlgdsws/5a43b3b4-d800-40ec-8476-719258c528b4) dashboard \(update: 2026013 from Miao\)

- Base: all fares after price comparison

- Brand fare coverage = brand fare count / base

- Brand name \& attribute coverage = brand fares showing brand name and exact brand attributes count / base \(e\.g\. brand name of some brand fares are not shown due to gambling\)

# Key Learnings

- To keep an eye on the lower hanging fruit to bring quick wins

- Start small

- Whatever root cause we found, we should think about a universal solution so we don't need to report it over and over again

