J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

Hi Yi, I have 2 role in IBU. 1 as BR MX TR regional director and 1 as special project. i am working on global flight upsell with Vivi as main project for my another role. Me and Michael has been appointed as IBU represetative with agreement of Nikki and Serena yearly this year.

As you know flight upsell is complicated one and has been talking with Vivi and Sirius entire this half year. BTW one of my OKR also set as upsell %, exact same target, same as few FBU PMs.

I've noticed that front end owner has been changed from Sirius to Doris.

I have 1 painpoint and 1 thing that I would like to explore further.

- Painpoint, we have been asking to Sirius and Doris to share any AB testing plans regarding upsell at least with us, so that we can get combined feedback from IBU regional team from mock upstage, and so far this has not been so smooth. Is it very big workload to share big AB test plans? I know there are many AB testing going on, what I look for is big AB testing such as middle page filter which many regional team has been request and also showing intersted to learn more and add their input. we can discuss more but so far no update from Front end team is the painpoint.
    
- 1 thing that I would like to explore further. As you know in the middle page, some fare cards has 24 hour free cancel text and is overwriting original ticket policy. I started to notice how we display is a bit misleading. I am working on data how big this issue is, and still working with one FBU colleague to figure out the scope. I've asking Doris if this switch is on FBU front end side and the answer I got is 'i don't know'. I notice Doris could be junior PM, so I decided to reach out to you directly, in order to establish some good work relationships and also find some common KPI/ground so that we can do something together that moves needle for flight upsell % this year.
    

Group Chat History

Michael Zhang:

Hi @Doris Xie (谢丹) , hope you are doing well! Recently we found that many fare cards have "24h free cancellation" or "24h cancellation with small fee" attribute overwriting the cancellation policy (in the screenshot it's a non-refundable ticket af 24h). we are wondering if we are able to do AB testing to show full cancellation policies / explore other ways to display cancellation.the hypo is that user got confused what's the difference between two fares looking very similar but different in price; or at least don't know what happens after 24h (not everyone knows clicking on the policy shows the details)[Image]

J Nam:

this was actually one of thing BR regional team was also asking. not sure how the internal discussion went. @Doris Xie (谢丹)

Doris Xie (谢丹):

I remember this was something discussed in a group chat before?

Doris Xie (谢丹):

@Michael Zhang How would you like to display it?

I am sharing some chat from Doris FYI. I know you are busy, I am also busy. AGG upsell is complicated one, but i think if we do 24 hour free display well, it can be helpful for both CR% and upsell%.

![](native-resource://sdk/image?resource_type=image&key=img_v3_0212n_685fa287-92f1-488e-9511-4ab1d89e8ahu_MIDDLE_WEBP&message_id=7651814386411047888&fs_unit=larksgaws-cdn&crypto=CAESMgog7I2BrN88Aum%2BjlpBIJGY3pY%2BRFdZxEL8TZLOJmvjXZgSDJgF5nc%2FhBp%2BJISFaxoA&width=359&height=1500&gif_optimize=true)

As you can see this airline, all fare card cancellation policy look exactly the same because 24 hour free cancel text is overriding original cancellation policy.

all I want to know at this moment is, who has switch for AB testing and how we can work together.

Please let me know if you prefer to have casual chat over some video call. I would be happy to explain where I am coming from more!

Thank you!

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

Hi @Michael Hu (胡晓光) this is the group that has been created this morning.

Reply to Sirius Zhou (周鸿昇)'s topic: 

A quick clarification regarding the background of 24-hour free refund: - Regarding the Background of 24-hour free refunds, I know of two possibilities. The first is a regional regulation, such as in the US market, where airlines or agencies are required by the government to offer 24-hour free refunds. The second is a policy packaged by airlines, the purpose of which is more or less to cover up their original refund policy (we all know that users who opt for 24-hour refunds are a minority). - Regarding the Switch, since this policy is usually created by airlines or agencies, there's no switch on the front end, and I doubt there is one on the back end either (needs confirmation). - Regarding the Solution, we initially planned to present both the 24-hour free refund policy and the basic policy after 24 hours, but this would make the copy very long and reduce readability; it was a trade-off. Since Doris is currently OOO, I will discuss the solution with her when she returns.

@Michael Hu (胡晓光) this is what we have so far

Vivi Ye (叶静仪)_提需填写➡️[国际Agg查询组｜需求收集表单](https://trip.larkenterprise.com/share/base/form/shrcn8GZWxzyw7PVfBvJtzXrsYf)​_

Add more context for 24 free refunds, we (@Oliver Tang (汤健) 's team) has a config to set which airline and agency could have this policy

We do have some concerns about this configuration, which this policy will hide the real refund details, and not sure the user preference for this free refund

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

Reply to Vivi Ye (叶静仪): 

Add more context for 24 free refunds, we (@Oliver Tang (汤健) 's team) has a config to set which airline and agency could have this policy

@Vivi Ye (叶静仪) Thank you Vivi, could you help share which region/airline we have this on? I can do quick data check how broad this is. now with help of Oliver we have code to run which order is supporting 24 hour/void.

I personally think this is two side sword, and two different perk.

- 24 hour free cancel can improve CR%
    
- but user may miss original policy, so don't know how refund will look like after 24 hour is passed, so can cause confusion + miss upsell opportunity.
    

![](native-resource://sdk/image?resource_type=image&key=img_v3_0212n_beeac1b0-6551-4280-b4e5-ac5ded5c8ahu_MIDDLE_WEBP&message_id=7651894130083171535&fs_unit=larksgaws-cdn&crypto=CAESMgog7I2BrN88Aum%2BjlpBIJGY3pY%2BRFdZxEL8TZLOJmvjXZgSDJgF5nc%2FhBp%2BJISFaxoA&width=359&height=1500&gif_optimize=true)

Michael Hu (胡晓光)

I've checked, and I understand that the general direction is to display the refund rules for freight rates, and we've already reached an agreement. Now we're looking at how to implement it, right?

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

Reply to J Nam: 

![](native-resource://sdk/image?resource_type=image&key=img_v3_0212n_beeac1b0-6551-4280-b4e5-ac5ded5c8ahu_MIDDLE_WEBP&message_id=7651894130083171535&fs_unit=larksgaws-cdn&crypto=CAESMgog7I2BrN88Aum%2BjlpBIJGY3pY%2BRFdZxEL8TZLOJmvjXZgSDJgF5nc%2FhBp%2BJISFaxoA&width=359&height=1500&gif_optimize=true)

this is extreme case.

Michael Hu (胡晓光)

Both parts of this information are helpful to guests. A 24-hour free cancellation is equivalent to a product advantage, while the refund policy represents the difference between products.

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

Reply to Michael Hu (胡晓光): 

I've checked, and I understand that the general direction is to display the refund rules for freight rates, and we've already reached an agreement. Now we're looking at how to implement it, right?

@Michael Hu (胡晓光) @Yi Ding (丁一) @Vivi Ye (叶静仪) are we one the same page?

Best is to do AB testing, right? Can we do AB testing?

Yi Ding (丁一)_Be User Centric; Be Value Driven; Do the Right Thing; Succeed Together!_

As long as the backend gives us info, we may conduct frontend AB tests. But depending on data about the coverage and severity of this scenario, priority can vary.

Michael Hu (胡晓光)

Reply to Yi Ding (丁一): 

As long as the backend gives us info, we may conduct frontend AB tests. But depending on data about the coverage and severity of this scenario, priority can vary.

@Yi Ding (丁一) What information is still missing now? The backend can provide it.

Yi Ding (丁一)_Be User Centric; Be Value Driven; Do the Right Thing; Succeed Together!_

Reply to Michael Hu (胡晓光): 

@Yi Ding (丁一) What information is still missing now? The backend can provide it.

@Michael Hu (胡晓光) I'd suppose none. It's just a hypothetical statement.

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

With help of Oliver, we have data which airline/supply/region support 24 hour free cancel/void. but we don't know which airline/region this display is on. @Vivi Ye (叶静仪) can you provide config so that we can check how broadly this is being impacted in front end please?


Vivi Ye (叶静仪)_提需填写➡️[国际Agg查询组｜需求收集表单](https://trip.larkenterprise.com/share/base/form/shrcn8GZWxzyw7PVfBvJtzXrsYf)​_

Reply to J Nam: 

With help of Oliver, we have data which airline/supply/region support 24 hour free cancel/void. but we don't know which airline/region this display is on. @Vivi Ye (叶静仪) can you provide config so that we can check how broadly this is being impacted in front end please?

@Oliver Tang (汤健) Could you share which airline and region have 24 free refund? （废票目前在哪些航司、航线、票台有配置）

Translate

Agg will use the same config with Oliver's config, no extra config

*But I'd use this config to double check

J Nam_What would you do if you are not afraid [UID: _TSKR672ujsvi3a0 ]_

![](native-resource://sdk/image?resource_type=image&key=img_v3_0212n_b3aa34ce-eec2-4175-9b05-fe099f97ebhu_MIDDLE&message_id=7651900132698361574&fs_unit=larksgaws-cdn&crypto=CAESMgogH63nYdRtQ%2BCIAr74Jos6BHkiyaravqql6iEGv4%2BW9J4SDEL4RcBc5rI9XD4fnBoA&width=830&height=145&gif_optimize=true)

This is total flight order break down by ticket operation type. same code from Oliver. FSC, 54% support 24hour free cancel/VOID right now. but just order perspective, not based on actual front end display.

Yi Ding (丁一)_Be User Centric; Be Value Driven; Do the Right Thing; Succeed Together!_

Reply to J Nam: 

This is total flight order break down by ticket operation type. same code from Oliver. FSC, 54% support 24hour free cancel/VOID right now. but just order perspective, not based on actual front end display.

@J Nam may i learn what does "void" mean?

Vivi Ye (叶静仪)CN version from AI: [https://trip.larkenterprise.com/docx/VebodqO2bozY8BxE9vQcUDm9nBh?source=share_lark](https://trip.larkenterprise.com/docx/VebodqO2bozY8BxE9vQcUDm9nBh?source=share_lark)