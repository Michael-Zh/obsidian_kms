> Title: 05-29 | Catch-up J+M Time: May 29, 2026 (Fri) 15:07 - 15:33 (GMT+08) AI notes: [05-29 | Catch-up J+M on May 29, 2026](https://trip.sg.larkenterprise.com/docx/WiZrd7IYKokYCqxPBXBlWKstgAc)

  

@Michael Zhang 00:00:29 对不对？

  

@J Nam 00:00:31 good morning。

  

@Michael Zhang 00:00:33 oh， but why theres no camera let me try again should work there help great。are you ha cool lets tackle this yes。

  

@J Nam 00:00:54 okay。ba。

  

@Michael Zhang 00:01:01 So I talk to Vivi yesterday, so you already know that there's new capabilities rolling out.I think now there.

  

@J Nam 00:01:08 hum。

  

@Michael Zhang 00:01:10 So what they said is they wanna to have a justification of the business case in order to use that artificial, like the business rule, retain the fair.So I kind of build a bit of these hypothesis tree or whatever to just to see what's the logic that we're going after.So background is we found the fees, the bags, plus the flexibility share of the order are significantly lower among the BA compare to the other FSCs, right?Among the gbfob year today.And then the ask is to use the new ability to retain the semi flex frame fair to tackle this issue. So when we propose.Is that the FBU basically said that, well, we're not quite sure that missing these semi flex brand fair is actually the cost leading to these, you know, these significantly lower data.So they wanna to compare the 2025H2 where the new price comparison algorithm is was not rolled out yet.So they assume that the higher frontier fares are not being filter out or.At least is being shown as usual.So then by comparing these two data, then we'll be able to tell them, okay, if the new price comparison algorithm actually filtering out the high brand fair and leading to the low share of the flexibility orders. Is this clear for, so far for the year?

  

@J Nam 00:02:59 so。Filtering out highest tier, were high tier that was not in, that was implemented only this year.

  

@Michael Zhang 00:03:10 So I think that is an, for me, that's an Assumption, right?So, yes, so the new PRI, the new price comparison algorithm only started to roll out from March, right?About 50% of the traffic.And then by end of April is 100%. So by now, the whole month of.May it's in the new algorithm already?And then what are the behavior and or the founding findings when they roll out, when, and they do the test for the new price comparison algorithm is that they're filtered, filtering out higher tier brand fair likely to filter out the higher brand fair. Perfect. Yeah. And the current one, yes.

  

@J Nam 00:03:56 You mean the fair selection logic, right? The fair select.Sheng, when we move from the bucket to the.

  

@Michael Zhang 00:04:03 Yes, and then we can see, I'll give you one data.So this is what I pull from the raw data to look at the, so from we have the coverage data since March, February, sorry, this year until now, right?And then I look at BA only and then looking at the pre price comparison coverage and post price pride post.

  

@Michael Zhang 00:04:31 Price comparison.Well, I'm trying to say coverage and then I group all the flex fair.So semi flex, flex already flex.So everything that is falling into the market that we think is falling short, right?So we can see before the pri, new price comparison algorithm move rollout in February and to March.The pre and post coverage are pretty consistent and relatively high, around like 75 to 80%.

  

@Michael Zhang 00:05:08 And then once the price compares, new compare, new price comparison algorithm rolled, start to rolled out in the May, May at mid March, sorry.And then the coverage, post price comparison coverage rate start to drop.And then by the end of April, where we fully roll out the price.Comparison algorithm, it basically drop to pretty significantly level to let's say 30% for 40.

  

@Michael Zhang 00:05:38 If so that's like how that's how they assume that, you know, by comparing the pre rolled out status and the current status will probably be able to tell that if the higher tier missing the higher tier brand fair is actually the cost for this one.

  

@J Nam 00:05:58 So, this is already proof that the flex.Has been filtered out during the new fair selection rollout, right? They aware of it, where they.

  

@Michael Zhang 00:06:04 Yes.Yes.No, there, I think not specifically for this one.They're aware of it as a overall behavior.So they're aware of there because so the what I'm trying to say, so they're aware of this behavior for the new price comparison algorithm.That's one.

  

@Michael Zhang 00:06:27 Second one is that they think it's in some case.In most of the, in sub mall, they don't know the CA amount of cases.But generally speaking, the reason why these fairs being filtered out is because based on the algorithm, these fares are unreasonably high.Price or not match the price is not justifying the, sorry, the attribute is not just justifying the price that they're did they're selling.So that's why I got filtered out.And then so that's what they aware of. Not in this.Specific case, but just as a general understanding for this specific charts, no, they don't know yet.

  

@J Nam 00:07:06 So this one they don't know yet?

  

@Michael Zhang 00:07:12 I just start to work on it yesterday and today.

  

@J Nam 00:07:16 And then what about the guarantee thing?

  

@Michael Zhang 00:07:20 So the guarantee thing is, so with the, so yeah, so the first one I already mentioned is comparing the before and after the price comparison. And then the second thing is.Is that, so even though we do filter out this higher brand, higher tier brand fair, right?

  

@Michael Zhang 00:07:37 The other ways for the customers to be able to get the same benefits, let's say both back bundle with eh come some kind of true X products for flexibility because they're also in so called in line.I don't know what is the official name of it.They call them RP.Basically means that I have a ace fair of a brand fair and.Then I add one, I replace the flexibility.I say true.com offers free cancellation or free change, for example, that is basically a bundle product, right?And they were saying that even though we don't have the brand fair offering, the flexibility benefits, potentially we offer it as a form of a bundle.So they wanna to see if that's the case. So basically see what.What other options the customer has regarding the flexibility.

  

@J Nam 00:08:35 So we need to, so we need the data for the, our own product, like package self bundle. We need flexibility self bundle.

  

@Michael Zhang 00:08:35 And then, yes, yeah, yeah.So yesterday I ask for this data and then I haven't get back.I haven't hear back from the accelerate team because the table, basically the table that we use for the expat, you remember you shared to me was like, there's all the X products.I think they also include all the bundle products of other sorts as well.But with the facility, but we just need to know which value for other filters we need to get the same.

  

@J Nam 00:09:12 Who you, who did you talk, could you contact?

  

@Michael Zhang 00:09:15 Is the owner of the table.Let me see, what's her name?What's his name?

  

@J Nam 00:09:21 Is it Kelly's team?

  

@Michael Zhang 00:09:23 Oh no, it's in the FBU side. It's not on the FBU side.

  

@J Nam 00:09:33 Are you going to validate in the hive table?

  

@Michael Zhang 00:09:37 Yeah, because the source is in the hive table, right?To understand that table, we need to ask the FBU to people. So this person.

  

@J Nam 00:09:43 No need to do this.We can just contact Data Warehouse to figure it out.

  

@Michael Zhang 00:09:51 You mean Ina, like our IBU1? Okay.

  

@J Nam 00:09:53 Kim, Henry, Kelly's team.Kelly's team. Yeah, IBU team. Kelly's team supposed to fine.Whatever the equivalent one, because FBU hive table may not be hundred percent equal to IPO inquiry.They don't always mirror.Sometimes they don't mirror exactly the same.So sometimes they store in different way.So even though we identify FBU tag, how it store in IPO can be different. So involve Henry.

  

@Michael Zhang 00:10:21 Okay, turn on.I'll ask because I thought we already have the table in on the IPO side. Yeah, yeah.

  

@J Nam 00:10:27 Maybe not, we don't know.Just when we have this kind of data synchronization issue between FBU and IPU, just contact Kelly.

  

@Michael Zhang 00:10:37 Okay, so I guess specifically we said that, okay, we wanna to find out this particular thing and then, you know, ask them to find out with the FBU team. Okay, got it. Yeah, then I'll do that.

  

@J Nam 00:10:46 Yes, yes, yes, yes, yes, yes, yes, yes, yes.So involve.So step is the li involve Lily and then ask Lily, do you want me to just come?Just involve Kelly or you will figure out that's how this suppose to be.

  

@Michael Zhang 00:11:05 Okay, got it. I see. You know.

  

@J Nam 00:11:12 That's their job. You don't have to do their job.

  

@Michael Zhang 00:11:18 So that's another part that they want to check my.I don't know, I have a feeling that this is not gonna be too much of an impact in a sense that one, the.EU team doesn't have the, EU locals doesn't have the guarantee product, right?So they already eliminate that guarantee.

  

@J Nam 00:11:38 No, I think it's different.Guarantee and self bundle is different thing.Guarantee is just a guarantee and self bundle is two different thing.

  

@Michael Zhang 00:11:45 Yes.So the, the what I means that's, yeah.Okay.Well, about so it's an FSC, right?So then we don't know how much of the bundle they do for this FSC. It's more, more mostly for the LCC.

  

@J Nam 00:11:59 Yeah, yeah. So guarantee guaran.Guarantee, we know that it's not in EU, but then guarantee can be packages, pay guarantee can be flexibility, guarantee can be anything, right?But then we need to understand the data structure and then find the right data for us.

  

@Michael Zhang 00:12:20 Okay, so those are the two kind of points that they are kind of looking for.So I think this one just pending for the data for now. We can park it until we have.The data and then the first.

  

@J Nam 00:12:31 No, just yeah, understand.But then it's already Shanghai.3 p.M.Just involve Lily and Kelly, this kind of data synchronization issue.I used to just contact Kelly directly and then he figure out. No more time to waste.

  

@Michael Zhang 00:12:48 Yeah, I see what you mean.The, yeah, so for the first one, so for me, the Assumption like by.Just by comparing their pre and post price comparison algorithm.I'm not quite sure if we can confidently say even before the new price comparison and rolled out, the coverage rate is good.And then the, let's say the supply is good.And then also we're actually, yeah, exposing those to the customer even before the new price comparison algorithm.

  

@J Nam 00:13:28 What do you mean by supply issue? BA? We don't.Have.Csdba is super strict airline. So we only get the official fares.

  

@Michael Zhang 00:13:37 Okay.So then supply shouldn't be an issue in a sense.

  

@J Nam 00:13:42 Yeah, and then your data just data now pre pre agg coverage, it's already high, meaning the sourcing wise, there's no issue.

  

@Michael Zhang 00:13:50 Hum.Okay.So we can say, confidently say that the sourcing is not an issue.And then because we seeing here in this, you know, for in February month that the post algorithm coverage rate at P post price comparison algorithm coverage rate is still high.So that means that before that the coverage should be good.

  

@J Nam 00:14:14 We, we can say, we assume that sourcing from the BA is not an issue because BA is strict airline.And then we only get the official fair.

  

@Michael Zhang 00:14:24 Hum. Yeah.

  

@J Nam 00:14:24 And then looking at the pre coverage, it seems sourcing is not a issue for this specific.But then coverage after the fair selection is decreasing, meaning that we highly suspect that this is coming from the new fair selection algorithm.

  

@Michael Zhang 00:14:39 Okay, so then we're on the same page.So with that, then that, let's look at the numbers itself, right?So this was the number that we provided, right?So the year to day number, if you remember, so we see the 10% versus 44% in long haul, etc.

  

@J Nam 00:14:53 Yes.

  

@Michael Zhang 00:14:56 So when I look at the H2 in 2025, the data trend is actually pretty similar.So when we look at the non BA other FSCs, they actually is even higher f 54% versus BA itself, it's stay around the same 9%.So even before the price comparison algorithm being rolled out with the same, with a good supply.It looks like the flexibility options are still a low percentage.So the the SHO for the short haul, it's actually almost the same. There's no.Will change 24% versus 23%,1% VERSUS 2%.

  

@J Nam 00:15:36 I think this one still cannot be hundred percent justify because so gap is still huge because it means that maybe BA, because it doesn't mean that before the new algorithm were bucket bucket algorithm, it doesn't guarantee the flex will be show displaying to the customer neither.So, gap between the FSC and BA, that is the big DIS, still the discrepancy.

  

@Michael Zhang 00:15:55 Yes.

  

@J Nam 00:16:01 So there is a, the hypothesis, we still believe there is a chance to sell more. What, why? What? Right.

  

@Michael Zhang 00:16:07 Hum, so I think, hum, yeah, yeah, I, I agree.So I think the point here, probably what we're trying to is that we know that there's a issue when it comes to selling.So there's demand at least, right?We can say there's a demand for the both back plus flexibility.It just, for some reasons, BA doesn't sell enough of it, right?I think that's the general consensus that we have.And then now the question is how to solve that or what is the cause of that.So one of the potential we thought will be because the new fair selection algorithm filtering at the highest tier so that they don't even having a chance to be exposed to the customer, right?That's why it's not improving the number.So that's why we wanted to push for this solution. I think what we getting stuck here with the.

  

@J Nam 00:16:59 With we.Still think there is a room to sell, that's what we're saying.

  

@Michael Zhang 00:17:03 Yes, yeah, yes.So then I think the what we're getting start of the FBU team is that they don't necessarily agree that this is the reason that is going to change this.So that might be other layers.And then to, but at least to, we need to find a way.

  

@J Nam 00:17:22 That's also possible.

  

@Michael Zhang 00:17:23 Yeah, so I think then we, what I'm thinking is that, so what kind of proposal, what kind of.Proposal we should push for to address this issue.I mean, we have the general consensus agreement, I think, but we don't know what is the solution to push that.

  

@J Nam 00:17:41 We don't know the solution.We just keep escalating, and then we just have to discuss with the FBU team.

  

@Michael Zhang 00:17:48 Okay.

  

@J Nam 00:17:48 We don't know all the system technical details.Our general hypo is that BA still have room to improve.So one is the really check if the self bundle flexibility was making.

  

@J Nam 00:18:01 シンガポーター。

  

@J Nam 00:18:30 マイクライティミュー。

  

@J Nam 00:18:31 Really need to fix the internet because.Not easy to focus what you say because of the noise.

  

@Michael Zhang 00:18:39 Still the noise, sir? Okay.

  

@Michael Zhang 00:18:50 Okay, and then.

  

@J Nam 00:18:53 And then concept and then other FSC, there's also same chance that it has self bundle flexibility. There's.Equal chance or is there a reason that only da have self bundle?

  

@Michael Zhang 00:19:14 Well, this data only concerning the ticket itself. So it doesn't include any.

  

@J Nam 00:19:21 Ticket it only in the ticket ins itself.But then is there is why is there a reason why Da Order maybe?Under index because of the self and self bundle flexibility is not included here.Why not the rest of the FSC have the same equal chance if the rest of the FSC also have the self bundle product, self fund flexibility, then why flex is still as high as 54%?Is there any good reason?Only self on the flexibility available only for the PA?

  

@Michael Zhang 00:19:55 Yeah, okay.I'm absolutely. So it could be the difference comes from the.Flexibility.But it could also be that because they both have the flexibility bundle, but then even with that, yeah, still not selling, right? That's what you mean.

  

@J Nam 00:20:11 Yeah, there is a equal chance that other FSC also have the self bundle.Then why flex?Other FSA flexibility is selling higher than self on the flexibility.

  

@Michael Zhang 00:20:23 Okay, make sense.

  

@J Nam 00:20:32 So first party is get the data for the self flexible bundle.

  

@Michael Zhang 00:20:37 Okay.

  

@J Nam 00:20:43 And then.

  

@Michael Zhang 00:20:43 And then I just brought, I guess I just brought up with Vivi about this regarding that, okay, we have the general consensus that we know the demand.There should be demand, but for some reason, it's just not selling.Now, Ashley is down to pin down to where the issue is coming from, right? And then we kind of work with the solution.

  

@J Nam 00:21:00 Yes. So one.And one 1 hypo 1.Yeah, so one 1 hypo is the flexibility self bundle.But then if that's the case, then whether my other FSC, Self Bundle Flex, no more flex is selling so good.So maybe there's a less likelihood that Self Bundle was cannibalizing the overall sale, right?

  

@Michael Zhang 00:21:14 Yes, hum.

  

@J Nam 00:21:21 So this is just so we need the data to accurately say yes or no.

  

@Michael Zhang 00:21:26 Okay.And then I think the other one is exposure probably, right? So it.

  

@J Nam 00:21:30 Yeah, if, yeah, yeah, it doesn't mean that in the second half last year, second half, it doesn't mean that flex was having enough exposure.

  

@Michael Zhang 00:21:31 Could be that. Yeah. Yeah. Okay.

  

@Michael Zhang 00:21:42 Okay, alright, then I'll follow up with Lily.And also just to quickly catch up with the this one and then we'll see the next steps for that. Thank you.

  

@J Nam 00:21:55 Can you break down the data into EU reason versus.Can you only filter down to the EU reason?EU reason only.Can you go back to the Google spreadsheet? This GB only.

  

@Michael Zhang 00:22:04 This is the GB only.This is GB only.Yeah, I think, yeah, I only to GB because it's a GB FOB and then it's a GB region only.

  

@J Nam 00:22:16 Okay.

  

@Michael Zhang 00:22:17 And then, anyway, the, I check the orders, I think was it around 90% or even more than 90% of the BA orders actually coming from GB region anyways.

  

@J Nam 00:22:30 Alright.

  

@Michael Zhang 00:22:33 So I think we have a good overview of the GB BA and by itself, and then comparing to the other FSCs that is selling on the GB size GB.

  

@J Nam 00:22:49 Yeah, so share the progress.

  

@Michael Zhang 00:22:53 Okay, got it. Thank you. Then I'll keep you posted.

  

@J Nam 00:23:02 エンディングと遠隔なイージー。

  

@Michael Zhang 00:23:08 Yeah, I've yeah, it's a the tricky one.My, I suppose to get the, no, it's so my internet is actually a different kind of internet.

  

@J Nam 00:23:13 オッテンワイワイサンドリーウィーヘッドディスイッシュビックコースピコースビフォーユディドルヘッドスイシュワイケナディジュチェンジンジャネイビーセントリー。

  

@Michael Zhang 00:23:24 Usually people use the landlines, right?So then they have, you know, they plug into the routers. Mine is.It's actually almost like what's about the 5, using the 5G network.So sometimes the 5G network, it's the not as consistent in an area.So, but the landline is very slow.So this one is already better, but that sometimes it gets not very stable because the maybe the 5G things are going on, I suppose to, yeah, no, it wasn't. It's a supply issue.

  

@J Nam 00:23:53 ビフォー。

  

@J Nam 00:24:00 えらい検水。

  

@J Nam 00:24:01 Eh, that not only your voice, but then the visual, the video, it's also delayed.

  

@Michael Zhang 00:24:04 The image.Yeah, I think it's just the internet is very slow.I think now the speed is not great.Yeah, I'll try to see if I can do something.Otherwise, I have to find a place to. You're good connection.

  

@J Nam 00:24:26 I wish I can record your voice and then share to you how big movie.You have from time to time. It's like a robot, really. So.

  

@Michael Zhang 00:24:33 How broken?Oh, that's really bad.Okay, I hear you.Okay.For some reason, but it's just not the other way around.Maybe it's my headphone.

  

@J Nam 00:24:44 Yang Yi.

  

@Michael Zhang 00:24:45 I don't know.

  

@J Nam 00:24:45 It's like a robot or like you have really bad sore throat, like your voice is really kicking off from time to time.

  

@Michael Zhang 00:24:46 Let me.

  

@Michael Zhang 00:24:53 Oh gosh.Okay, cool.Alright, I will talk to Lily now and then we see. Thank you.

  

@J Nam 00:25:08 Yeah, just say that we think we want to quantify the BA.We see some opportunity to increase the order.So we hope to get some prioritization.And then if Lily is too busy, we can just involve Lily and Kelly to get this sort out very quickly. Thank you.

  

@Michael Zhang 00:25:25 Thank you. Alright, cool. Thank you.