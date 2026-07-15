---
author:
  - "[[Bart Slodyczka]]"
source: YT
url: https://www.youtube.com/watch?v=OOCioZC4tk0&list=PLYQATQ-FupFzf7ApyP8KURMTtn2MhAok-&index=3
saved: 2026-06-17T00:59:39+02:00
tags:
  - YT
published: 2026-05-04
description: Local AI is getting insane. This video shows you exactly how to run free, private AI models on your own computer using LM Studio — no internet needed, no monthly fees, your data never leaves your devi
id: LM Studio Is Getting Insane — Start Using It Now
annotation: reference to build my local LLM
summary: "Tutorial on running local AI models with LM Studio: download and run open-source models (Llama, Mistral, Phi) completely offline on your own machine. Key features include no API costs, full privacy, model comparison, and local server mode for API-compatible apps. Positioned as the primary alternative to cloud AI for personal/private use cases."
---
![](https://www.youtube.com/watch?v=OOCioZC4tk0)

Local AI is getting insane. This video shows you exactly how to run free, private AI models on your own computer using LM Studio — no internet needed, no monthly fees, your data never leaves your device.  
  
What you'll learn:  
\- The difference between cloud AI (ChatGPT, Claude) and local AI  
\- How to pick a model your hardware can actually run  
\- Setting up LM Studio and downloading your first model  
\- Adding MCP tools to your local AI:  
• Brave Search — web search inside the chat  
• Playwright — full browser automation  
• Desktop Commander — control your desktop and run CLI commands  
\- Sharing one model across multiple devices using LM Link  
\- Plugging your local model into Claude Code, Claude Cowork, OpenClaw, and Hermes Agent in three steps  
  
LM Studio: https://lmstudio.ai/  
Node JS: https://nodejs.org/en  
  
👉 Watch all my Claude videos: https://www.youtube.com/playlist?list=PLi7jtY2ZZqRYpcKQh5H4f7iy0iRPLIWXh  
  
👉 Watch all my OpenClaw videos: https://www.youtube.com/playlist?list=PLi7jtY2ZZqRYb7LXb50IjnsdmUOFq0fAW  
  
👉 Get in touch: bart@supportlaunchpad.com

## Transcript

**0:00** · Hello legends. In this video, I'm going to show you how to run AI models locally on your computer. We'll be using a tool called LM Studio, which is a desktop app that you can download for free, and it lets you browse different AI models. For example, the Gemma 4 E2B. Let's us know key details about those models, the size of the model, and most importantly, it actually lets us know if our computer can handle that model. Now, this is a really difficult thing to get your head wrapped around when you're first starting with local AI models.

**0:25** · But, if you go into the settings, you click on hardware, you can actually see that LM Studio will pick up what your computer is and what kind of capacity it has to run different models. For example, if I find a model that I want to download, but it's not actually going to work on my computer, I'm just going to get a warning that says, "Likely too large to run." LM Studio also gives us the ability to have conversations with these models, very similar to ChatGPT and Claude. Over here, this conversation, I've uploaded a PDF, and then I've had a conversation about the contents of that PDF, totally private.

**0:53** · So, if you've got private information or private company data, that's never going to leave your system. In this chat, I've been able to upload an image of a cat at the beach, and then ask the model to describe to me exactly what it sees. The Gemma 4 models are actually fantastic. They can work with images, so this makes it really interesting and fun. And then finally, in this conversation, I gave the model the ability to search the web. I gave it Brave web search, and I asked it a question to find the latest AI news. And then over here, I've got the result with lots of different sources that were cited.

**1:23** · Now, in addition to being able to download and run these models in that chat-like interface, a lot of the power comes from when you're able to get that AI model that you have and actually plug it into different business systems that you want to use. So, if you're using tools like Claude Co-work to automate your business tasks, Claude Code to code things, if you're using things like Open Claude or Hermes Agent, you can actually download a model into your LM Studio, and then you can plug that directly into Claude Co-work, into Claude Code, into Open Claude or Hermes Agent to power the functionality.

**1:52** · I'll show you exactly how to get your local model that you downloaded, that same Gemma model, and plug it from LM Studio directly into Claude Co-work in like three easy steps.

**2:02** · So, that you can have free and private conversations within Claude Co-work. So, to get started, just go across to lmstudio.ai, and then you just click this download button. You need the package to download based on your computer. After you download and install LM Studio, the next thing you want to get is something called a Node.js. This gives you the ability to run JavaScript on your computer. This is one of the most common engines to actually run code on your computer. So, once you've downloaded and installed LM Studio, let's just open it up and go across to the agents button over here, which is the model search.

**2:30** · And then we have this search tab that we can use to browse different AI models that have different capabilities. These are the most popular models and actually the most capable models for the sizes that they are. The Gemma E2B and the Gemma E4B, these models were actually built to work on your mobile phone. So, if you've got a really old computer that isn't too powerful, most likely you'll be able to download at least this model and start using it. So, let's just click on download, and then we can see that we're downloading that model onto our device.

**2:57** · So, while we're waiting for the Gemini model to download onto our computer, I just want to speak a little bit about the differences between cloud AI and then local AI. And local AI is a thing that we're doing by downloading an AI model onto our device. But, cloud AI is where we're actually using an external AI model that doesn't live on our device. So, when you're using something like ChatGPT or Claude, and you ask your question, your question actually leaves your computer, and it goes across to the ChatGPT servers. And actually, it travels across the internet.

**3:26** · And when it gets there, the ChatGPT AI will take your question, it'll process it, it'll generate the response, and then it sends your answer back, once again, over the internet, back into your computer, and you can have your conversation. Now, as you can imagine, you're actually sharing all of your information with ChatGPT. And this means that this is not 100% private.

**3:46** · Now, on top of this, you're also paying for the service to use the ChatGPT AI. I think that's probably a little bit less of uh an important consideration when you want to have a local model on your device. These models are very powerful, they're very smart, they're very fast.

**4:00** · So, for a lot of use cases, I think a paid cloud AI is very useful. But, sometimes, if you're a business owner, you want to have private conversations about your business data that you don't want to leave your business. Or, if you're like me, sometimes you want to have reflections or private conversations with an AI model that you do not want to leave and go to ChatGPT or Claude. So, when it comes to local AI, we're actually taking an AI model and we're installing it onto our computer. We're installing it on specific hardware, different components of our computer.

**4:27** · And then we're taking our question, and when we want to process our question, we're actually not sending it out on the cloud, we're not sending it over the internet. It doesn't actually leave our device. We can have our internet turned off, and that question goes into that local model that sits on our computer, it then gets processed, and then we get some answer back, and then that answer comes back into, for example, LM Studio, which is the application that we're using to run these AI models.

**4:52** · Now, the biggest consideration here is that, yes, this is private, which we do like. This is also free, which is a benefit. But, one of the downsides of this is that this model is typically going to be slower and not as smart as the AI models that we use in the cloud.

**5:09** · So, if you're downloading a small model like Gemma 4, which is a super popular AI model that people use, it's going to be slower, and it's going to be dumber than something like ChatGPT or Claude.

**5:19** · And sometimes the difference between how slow and how dumb the model is is so big that you get very frustrated because it's not able to actually write code for you. It's not able to actually have a smart conversation with you cuz it keeps stumbling over. It's not able to use different tools because it keeps falling over its feet as it tries to use those tools. Coming back to LM Studio, looks like we've downloaded our model. So, I'm just going to click on use in chat, and we automatically get this button that says, "Load model." When we first download an AI model, we just download it into our storage, into our hard drive. And it's not usable when it's stored. It's kind of like it's sleeping.

**5:53** · When we want to use this model and actually have conversations with it, we have to load the model into our memory.

**5:58** · When it's in our memory, it's at work, and it can actually have conversations with us. Now, a quick note on this number over here, as we saw before, the model size is 4.38 GB. This is the model when it just starts work, kind of like if you get an electrician, and you get charged a call-out fee. Before they do any work to your house, before they do anything, you're paying 150 bucks just to have them arrive at your door. And then when they start doing more work, then you might have to pay them more money. Maybe you got to pay them an extra 50 bucks, 100 bucks, 150 bucks.

**6:28** · So, by the time they finish what they're doing, now the total cost is not 150, it's now 300. The same thing happens here. Just to show up, your model's going to consume 4.4 gigs of memory. As you have a conversation, you add more context, it does tool calls for you. All that accumulates as history of the conversation, and then this number can grow, and it might go from 4.4 to 5.4 to 6 to 7 GB.

**6:50** · So, now that means when you're considering how big your computer is, if you've got something like 16 GB of RAM, and you really want to get a 10 GB model, you might not be able to use that model on your computer because as the conversation accumulates, you're going to eat into your RAM and then possibly crash your computer. The next thing we see over here is context length, and that's the amount of work that the model can do. Like I said, the call-out fee is 150 bucks, it's 4.4 GB.

**7:14** · This is a very small conversation, 4,000 tokens is enough to kind of test something out, but it can fill up very, very quickly. And over here, we have how much the model is capable of supporting, which is 131,000 tokens. So, if you click this, you give the capacity for the model to do the most amount of work, which also means that over time, the model might actually need more GB of memory. So, you can see here, it went up to 6 gigs. Once you're ready with all the settings, you can just go and load the model. It will take a couple of seconds to actually move that model away from your storage and into your memory.

**7:44** · And once it's here, you can start having a conversation with it. So, I'm just going to say, "Hi there." And look how fast this model is.

**7:50** · It's actually very, very quick. It took under 2 seconds to actually go through a full thought process and then generate a response for me. Now, I want to be a little bit cheeky with my LM Studio.

**7:59** · There's a feature called LM Link, and this lets you have LM Studio on multiple devices and then share the AI across those devices. So, my MacBook Pro is actually pretty small, and I'm recording a video here, so I don't want to use a local model in my memory in case it crashes my video. But, I've also got the Mac Studio, which has got a much bigger model loaded up onto it, and I can share that model from my Mac Studio and use it on my Mac laptop. So, to do that, I'm just going to click down on this drop-down tab, and I can see my other models that I've got on my Mac Studio.

**8:28** · I've got the Mini Max, which is 130 GB, and I've got the Gemma 4 26B, which is 16 GB. I'm just going to click on a Gemma 4 26B. I'm going to go onto my Mac tokens. Once again, these settings here, since I'm using the LM Link, this is all the capacity capability of my Mac Studio. So, I can actually max it out.

**8:46** · I've got plenty of headroom, and I'm going to load this model as well. Now that I've loaded up that model, I'm going to click on my drop-down. I'm going to select the model that I want to use, which is the 26B, and let's say, "Hi there." And we've got our response from that bigger model, 1.26 seconds.

**9:01** · Since the Gemma models natively support vision, you can see the ability to use vision is already enabled. So, if I wanted to upload an image into this chat, I'm just going to click on attach image. What do you see in this image?

**9:13** · And that's actually still very fast. So, it thought for 2.81 seconds. It had to process this image. It had to ingest that image into the model first, and then decide how to respond. And then we have here, it's a tabby cat resting peacefully on a sandy beach. Now, at this stage, you can actually go out and have a lot of fun with these models. Um but, as you can see, we're pretty limited into what functionality we have.

**9:34** · We've just got like thinking, which is the model being able to think and give us a better response. We've got vision.

**9:39** · Now, one thing that doesn't come out of the box is the ability to use different tools. So, I'm going to click on this little hammer icon, and I've got a bunch of different tools already loaded up.

**9:47** · But, I'm going to click onto this plus, which is going to give me the ability to get different tools, and then load them up into LM Studio. So, I'm going to click on this plus button. I'm going to go on edit MCP JSON. Just going to accept this. And this is my MCP file.

**10:00** · MCP is just the ability to connect different tools into my AI agent. Now, the file that you'll see for the very first time, it's going to look very bare-bones. I'm probably going to butcher it, but it'll be something like this. It's going to say MCP servers, and it's just going to have like a closed bracket like this, and maybe a couple of brackets on either side, which means that you've got nothing connected.

**10:17** · You can find a bunch of different MCP tools by either going to a tool that you use, for example, ClickUp, and then type in ClickUp plus MCP in Google, and you can find the official connector, and it'll explain to you how to plug it into your into the JSON file that we saw, or you can go to Model Context Protocol GitHub page, go into servers, and that's where I found my Brave Search API. So, over here, this is actually archived, but you can use the official server. Let's just scroll down and get the instructions, which are over here. So, for our case, we're always going to be using the NPX.

**10:50** · We have to copy this, and then we have to insert it into this JSON file. I'll just come across to Chat GPT or Claude, and then ask it to upload the MCP server into the LM Studio JSON config. Now, as you can see, I didn't actually give it what was originally in my JSON config from LM Studio. I recommend doing that, especially as you add more servers, it'll be able to cascade them and actually have multiple tools available.

**11:15** · Now, for Brave, we will need to get an API key. This is a paid service, so you can just go to brave.com, get your API key, and then paste it into here. After you've added in your MCP servers, you can just click save. And now we can go and start a new conversation. We can click on the hammer icon, and we can enable our Brave Search MCP. And this is going to give us the ability to do web searches while we're having conversations. Now, one thing to note is that when we have the MCP enabled here, and if I was to enable a bunch of different ones, like all these, then you can see that they're all being added into the message.

**11:46** · And in actually, all of these have their own separate tokens and context that get sent into the message. So, like we saw before with the electrician analogy, the call-out fee is 150 bucks. Now, the call-out fee is like 200 bucks because we're already giving we're preloading with tokens. And you can see exactly like what is being sent by clicking on to here, and all these different MCP tools, they've got a bunch of context that is sent as instructions for how to use the tool. So, all the stuff that you see on that screen just kind of pop up as we go, all these tokens are being sent with the conversation.

**12:15** · Same thing if I go into this next MCP tool, it's just initializing. Let's just actually open up a different one. You can see the Playwright tool, which is browser auto mation. Uh, this is just a bunch of different context that's being sent as well. So, let's just send, "Can you web search the latest AI news?" And you can see that our processing speed is a little bit slower now, because we actually have to get all this context, all the different MCPs, and pre-process them to understand what the request is.

**12:41** · So, that maybe took us like 5 seconds now to actually process that, and now we're going to accept the permission to use the web search, and now we're going to get that generated response of all the latest AI news. And then here is the news result. Now, one final tool that I want to show you is the Playwright tool.

**12:56** · So, I'm just going to go into the hammer. I'm just going to remove the web search, just remove all the context that I don't need. Remove memory. I'm going to keep Playwright. So, the Playwright MCP is a browser automation MCP. To get this, you can go across to the Microsoft GitHub page, then go across to playwright-mcp.

**13:13** · You can scroll down and then find the instruction to use this, and just like before, put it into Claude, ask it to add it to your JSON config file. Note, for this one, you don't need to use any API keys. This is just totally controlled on your device. And I'm going to ask this model to go across to apple.com.au and take a screenshot of what MacBooks they have on offer, and then send that screenshot back to me in this chat. I'm just going to bring this, uh, browser into here. This is the one that was opened up by the Playwright MCP. Let's approve the next action as well.

**13:41** · And as you can see, we just processed a snapshot, and I think we just looked at what's on this webpage. Let's proceed again. Maybe this will be a little bit better to see. Let's just proceed again.

**13:53** · Let's see if we're doing any other actions on this page. So, with this multi-step process, as you can see here, this is like four or five different times that we went through the cycle of doing something, coming back, doing something, coming back. Um, we failed this tool call. This model is a little bit bigger, and this is what I mean. The bigger the model, the better it typically is. It's actually able to fail something and then retry, and then kind of keep iterating through because it has the smartness, the capacity to do that.

**14:18** · Some of the smaller models, like the Gemma E2B, that's like 4 gig, maybe it wouldn't be able to actually follow these instructions. Maybe it would have failed and then just like broken and not generated the next response for us. So, that is one thing to consider, but over here, we can see the screenshot of the Mac page. Looks like it took the entire scrollable screen all the way down.

**14:38** · Yeah, all the way down to the very bottom. Now, the one \[clears throat\] final thing that I want to show you is, okay, we're using this AI within LM Studio. We can have conversations, we can add different tools, but we're still confined to this desktop app. What if we want to get that AI and use it in different applications that we're using?

**14:53** · So, to do that, we're just going to go across to this different tab over here, which is the developer tab. And a developer tab is going to give us this little panel over here. So, this panel lets us actually load up a model and then attach that model into a URL. So, what we saw over here with the Claude AI, actually, this over here has a URL.

**15:12** · It's got an address that's on the internet that when we send our question to, it just goes into that address on the internet. It goes into a URL. So, this over here does the exact same thing for us. Um, this is actually local on our computer. It doesn't make this URL reachable by you. Like, if you were to type this in right now, you do not reach my model on my computer. This is just like home address front door. That's what it's saying. So, if you're at your house, you would see the exact same URL, and only you could access your own home address by using this URL. But, what we need to do is just make sure that we have the server running.

**15:43** · So, yours is going to be off by default, and then we want to make sure that we have a model loaded up as well. Since we were chatting before, we already have a model loaded up. In my case, I have the Gemma E2B from my local computer, or if I scroll down, I've got the Gemma 26B from my MacBook Studio. So, all I need to do is just copy this URL. And at this stage, this is where you would go and actually plug the URL into your open Claude, or into your Claude code, into your configuration files. There's a bunch of videos on the internet about how to do that. I recently put one out about how to plug it into Co-work.

**16:13** · I'm just going to show you very quickly as well. So, I recommend you go off and watch that video. It's got all the steps outlined of how to actually open up this panel, so you can plug in your own AI model into the Claude desktop app. But, I'm going to take that URL that I just had from the LM Studio, I'm going to paste it into here. I'm going to use a gateway API key. I've just typed in LM Studio, and I'm going to leave this as bearer.

**16:37** · Now, I'm just going to go to apply locally, relaunch my Claude desktop app, and now I've got my app back open, and I can drop down, and I can see the different models that I've got loaded up in my LM Studio. All right, guys, I hope you enjoyed this video. If you've stuck around this far, I'd appreciate if you could subscribe to my page. And if you want to see more local AI content, please drop your questions below. All right, thank you, and I'll see you in the next one.