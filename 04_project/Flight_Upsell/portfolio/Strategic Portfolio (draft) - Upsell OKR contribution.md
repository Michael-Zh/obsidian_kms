Tags: 
# Purpose of the document:

- Document the overall background and approach to the project to replicate in the future
    
- Document my contribution to OKR for performance review
    
- Write my career story for CV and future opportunities
    
- Document my thoughts to tackle challenges around the project
    
- Build elevator pitch / conversation for encounters with senior leadership (ref: http://xhslink.com/o/4TcAaWTSqja)
# Why the fare upsell is a complex project

- Fare families vary a lot by airline and routes, hard to have one fits all solution
    
- Fare families change over time often without explicit notification, and rarely have any well-maintained public dataset/mapping (either in written or technically as a database)
    
- Trip as a unique OTA
    
    - works with many different suppliers. Each supplier has their own limitations and restrictions. And to uniformly map different sources to one set of fares is very difficult (technically limited by aviation systems, like not matching exactly in atpco; or comes with different brand names, needed to match the attributes to identify the same ticket)
    
    - Airline fare family's design may not be optimal, and OTAs have the advantage to "construct" or "bundle" new fare options to offer inbetween solutions to complement airline fare families. However, OTAs need to balance the variety and decision load, and build trust to sell non-official fares (fares not on airline official websites). And it also needs to make sure it is still profitable
        
- Trip as a company
    
    - Has its unique org structure, that flight ticketing is its own department (FBU, parallel to hotel, train, etc., and was mostly built on Chinese business and later on expanded to support international growth), and international markets are a separate department (IBU) tasked with providing market insights and strategic decision making. Meaning that IBU doesn't have development resources, and any product changes will need to rely on FBU to act on and approve.
        
    - On top of that, due to data security policies by different markets, IBU needs to "mirror" the FBU data to oversea locations (google big query), while FBU data sits in China (HIVE). The SQL code is not directly applicable to each other and some time syncing the data is a challenge (and costy)
        
    - FBU has a lot of different teams working on air ticketing. They are very technical and go into a lot of details. Since IBU handles all products (flight, hotel, train), no one in IBU can have the same level of knowledge as FBU members. Sometimes IBU and FBU use different lingos for the same thing (and they may be talking about different scope, e.g. FBU talks about all markets, IBU talks about non-Chinese markets; or one use segment one use order to calculate metrics). This makes the communication quite difficult, as FBU may assume IBU knows certain things and gives too much details, and IBU people are too busy/do not have enough knowledge to digest and clarify those details. Same goes the other way around. Whatever IBU makes a request, they may not describe it in a way that makes sense to FBU, and they don't know whom to reach out to since there are so many teams.
        
    - Also in FBU, each team is working more as silo as they only care about their own KPI. To make a specific fare available for the customer to purchase, it requires every process along the supply chain to work seemlessly. But in FBU, no one is responsible for or monitoring this end-to-end process. Every issue will need to dig through all related teams by whoever is raising this issue. Takes a lot of time and knowledge to resolve an issue.
# Main goal is
- to improve the efficiency: efficiently identify the issue (by IBU), IBU efficiently provides the sufficient information to FBU for further investigation or work on resolution, FBU efficiently updates the needed progress to IBU in time and in an understandable language and appropriate amount of details
- to align the same KPI and measurement monitoring between FBU and IBU
- to identify impactful insights to steer the strategic direction to drive upsell improvement (actual business results), especially to prioritize the right areas to focus on back by data insights
# How do we approach this
- me and my manager are the single points of contacts in IBU to the FBU project manager, so we centralize all the related information
- first align with the FBU team what is the scope and expectations. document it as shared OKR.
- we ingest all the different workstreams and map every ongoing works and discussions to this structure, so we have a framework to understand the priority and have an overview of what is going on in each process, and also help us to identify gaps
- based on our understanding from previous step, slim down the information and highlight important and relevant 
- establish a comprehensive communication model:
	- daily standup between vivi and Michael
	- Monthly sync between IBU POC and FBU involved teams
	- leveraging AI to build in-time standardized email updates and group notification for important product changes in plain language and concise message
	- bi-weekly summary of recent and upcoming changes to ensure info are centralized and easily searched for
	- similarly, create a project hub to house all updates, data, glossary, etc.
	- create a request form to collect upsell requests so we can shape IBU teams to collect needed info with business justification of priority (not just shoot a vague request randomly based on a single incidence)
- Build prioritization framework among all airlines globally based on their production volume, market share (external data), current upsell rate, and current data availability. this helps to narrow down the prioritized list of airlines to start the deep dive
- Gain strong understanding of existing data source, and push the building of/initiate/prototype new data sources, such as baggage, x-product, lowest price, flexibility, brand fare, coverage data, front-end trace date. And we enable the market use these data sources in an easy to understand way
- Future projects:

- we've identified 6 workstreams:
	1. **supply coverage**: to check if we are actually sourcing certain kind of fares from any suppliers, and if we have any technical issues in configuration. Ensure all **official brand fares** from airlines are covered/sourced. Focus on **selected airlines** where we have relatively complete brand fare data to analyse. Example issues:
		- Airline stops selling certain fares on certain ODs
		- Airline authorization expires
		- Wrong configuration that blocks fares flowing from distribution system to trip system
		- Bugs occur when we switch one supply to another
	2. **Fare Selection**: To determine which fares (and how many) to display to customers among hundreds of fares from many suppliers. Example issues:
		- Fares with important or relevant attribute combo are not selected due to limitation of the algorithm
		- Fares with very similar attributes and small price differences are both selected
		- Fares with extreme prices and irrelevant attributes (e.g. 3 x 25kg checked bag) are selected
		- Too many fares are selected for customers to choose from
	3. **Ranking**: Research shows that **80%** of users only look at the top three slots on the middle page. To elevate the most relevant fares among the fares selected from step (2), to maximize visibility and CTR. Example issues:
		- Fares with important or relevant attribute combo are not ranked among the top or folded
		- Or the opposite, fares with less relevant attribute combo and/or extreme prices are highly ranked
		- Fares with very similar attribute combo and small price differences are ranked next to each other
	4. **Pure Front-end**: Facilitate customer decision making with clear, complete, relevant information. Example issues:
		- Too much info to digest
		- Difficult to tell the difference between two fares
		- Too many decisions to make at the same time
		- Some fares have brand names; some don't
		- Unclear what is included and what is not
		- Missing included attributes (e.g. meal, seat selection, etc.)
	5. Workstream 5 (airline compliance) and 6 (pricing) are not prioritized for now.

- Specific project contribution:
	1. Coverage:
		- Ideate and prototype coverage data set with FBU
		- Lead the brand fare audit with regions. This audit aims to ensure Trip.com has complete and accurate mapping of airline brand fares across **40 global airlines** and to identify gaps between airline official sites offerings and what we source/sell on our platform. We built auditing material and educated markets to conduct the audit. We aim to insights are pending to be summarized