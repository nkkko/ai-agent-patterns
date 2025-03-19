Title: Introducing AX: Why Agent Experience Matters

URL Source: https://biilmann.blog/articles/introducing-ax/

Markdown Content:
We tend to focus on the generative aspect of large language models, the outputs they can create, the text, images and videos they produce. But the largest disruption from the current evolution of AI will come from bringing **agency** to computers.

Computers are no longer just deterministic machines that execute the transactions we ask them to do or schedule. They are becoming **agents** in the world, acting and operating and initiating the execution of transactions themselves. Computers will perceive their environment and take actions autonomously in order to achieve goals.

The vast majority of all these interactions will happen through software in the digital world.

Platforms, tools or frameworks that are hard for large language models (LLMs) and agents to use will start feeling less powerful and require more manual intervention. In contrast, tools that are simple for agents to integrate with and well suited for the strengths and constraints of LLMs will quickly become vastly more capable, efficient and popular.

In 1993, cognitive psychologist and designer Don Norman [coined the term](https://www.nngroup.com/articles/definition-user-experience/) **“user experience”** (UX), to cover all aspects of a person’s experience with a system including industrial design, graphics, the interface, the physical interaction, and documentation.

As the world became more and more connected and digital, the role of SDKs turning products into platforms, and opening them up for custom development, became increasingly important. In 2011, Jeremiah Lee [coined the term](https://uxmag.com/articles/effective-developer-experience) **“developer experience”** (DX) to describe the experience for developers of building on top of a platform.

Companies discovered that improving the DX of their products would empower and incentivize developers to extend their product with new capabilities and lead to huge competitive advantages. For developer tool companies, DX became a key competitive differentiator.

As we enter into an era where agents will interact with our products autonomously, and build with our platforms while consuming our content and experiences on the web and beyond, we need to start considering how to craft our product experience specifically for AI Agents.

We need to start focusing on AX or **“agent experience”** — **the holistic experience AI agents will have as the user of a product or platform.**

Is it simple for an Agent to get access to operating a platform on behalf of a user? Are there clean, well described APIs that agents can operate? Are there machine-ready documentation and context for LLMs and agents to properly use the available platform and SDKs? Addressing the distinct needs of agents through better AX, will improve their usefulness for the benefit of the human user.

Too many companies are focusing on adding shallow AI features all over their products or building yet another AI agent. The real breakthrough will be thinking about how your customers’ favorite agents can help them derive more value from your product. This requires thinking deeply about agents as a persona your team is building and developing for.

AX in practice
--------------

When ChatGPT launched its GPT store, our team jumped at it and built a Netlify GPT integration to streamline web deployment. This integration allows ChatGPT’s models to deploy any project to a URL on Netlify as an ephemeral website. End users of ChatGPT can easily claim the site and add it to their Netlify account with a single click. This effortless flow allows users and agents to collaborate seamlessly.

This flow has now been integrated into other GPTs within ChatGPT’s ecosystem, like Grimoire. And today, more than 1,000 sites are being created on Netlify directly from ChatGPT every single day. This only happened because we focused on what agents would need from our platform, identified new interaction flows to consider, and thought through how our API would need to be adapted and machine documented to make it optimized for LLMs.

Agents will far more frequently be collaborators and extensions of humans, rather than replacements. Both will wildly increase the productivity and the ability of a single human being.

In the developer space, AI will lower the barriers to entry and usher in an era with exponentially more developers, dramatically lowering the cost of custom development. Tools like [Bolt.new](http://bolt.new/) makes it easy for anyone to spin up a web project. We’re already seeing hundreds of thousands of people building their first web apps and starting to develop entirely new skillsets based on collaborating with agents — and this is the least capable these agents will ever be.

Colin Sidoti, CEO and founder of the authentication platform Clerk, is working on the agent experience of Clerk. This includes making it simpler for agents like those from Bolt, Lovable or Windsurf to build applications handling authentication with Clerk. He’s also tackling the even broader angle of making it easy for agents to sign in to applications built with Clerk.

In a [recent Twitter thread](https://x.com/tweetsbycolin/status/1880665260060983567?s=46&t=kTGxqT2-5adpe6xffJEZjQ) polling his users on which of these two initiatives to focus on first, Matt Luo, founder of the professionalized Discord called ClarityText, mentions how direct message authors may soon expand beyond humans to include AI agents.

Nikita Shamgunov, founder of the serverless database company Neon, shared with me how he is deeply invested in making sure Neon caters to agents. He’s already staffed a team of AI engineers to dogfood Neon as agentic infrastructure positioning it as the default Postgres provider of choice.

These are all examples of companies starting to embrace AX as a discipline and recognizing agents as a crucial new persona for their software.

Closed vs Open
--------------

As AI agents start becoming useful and commonplace, we’re broadly going to see two approaches enabling agents to interact with the software we depend on:

A **closed** vertical approach, where companies tightly integrate their own agents into their own software. An **open** approach, where companies focus on making their software accessible to external agents.

There are currently more examples of the closed approach, in part because of a lack of broad cross industry collaboration on how to enable agents to work across the boundaries of different products. As we build out better open approaches to tool use, API understanding and versioning, documentation access and user/AI agent collaboration flows we will see this change.

For example, today products like Google Workspace are adding buttons for Gemini AI all over their products, with no clear path for users to bring other agents with them for content creation, visual design, data manipulation, and presentation development. Microsoft is taking a similar closed approach within Office 365 where they are building their own tightly integrated Copilot branded agents.

But as the innovation cycles of the broader startup ecosystem start figuring out new approaches to agent design, the first companies to truly open up their applications — enabling users to bring their favorite agents to help craft presentations, build spreadsheets, collaborate on documents — can gain a large competitive advantage through ecosystem and competition.

Leaning into AX as a strategy, means embracing a vision of an open agent world. This vision aligns with the original ethos of the open web: a place where many diverse competing agents (built by different people or companies) can seamlessly interact with software on behalf of their users. Prioritizing AX makes it as simple as possible for any agent a user prefers, to deliver outcomes on their behalf.

The era of AX
-------------

Generic SaaS tools will increasingly be replaced by custom developed internal applications. Entirely new paradigms of web experiences will emerge as developers can build things of a complexity previously unimaginable for any typical web team. As the cost of building and deploying continues to go down, the number of web apps and sites will explode

For all software companies, this shift demands a fundamental change in mindset: start consciously designing the **AX** of their products, or risk being replaced by tools that empowers their customers to harness the exponential power of seamlessly collaborating with agents.

Netlify built its original growth engine that transformed modern front-end development through a relentless focus on the developer experience of building for the web. We obsessed over the shortest path from code to URL in production for developers and fully automated web operations so developers could focus on building and creating.

Our next company-wide obsession is AX. What is the shortest path for an agent to go from user input to URL in production? How do we make our primitives and APIs simple for LLMs to build with? What new workflows are needed to make the collaboration between developer and agent not just efficient, but delightful?

Outside of our own efforts, there’s also a broader story of how we advance the AX of the web itself, and we will work with the industry to help mature and advance these AX practices for the benefit of the industry as a whole.

As the starting point for app and web development shifts from manual development to AI-assisted co-creation, AX will become the most critical factor for how well we serve our users and fulfill our core mission: **to enable the world’s developers to create, and unlock the power of the web.**

Whether you’re a practitioner or business leader, ask yourself this: What would an open approach to AI agents as an audience for your product unlock? How could similar focus on AX transform your own product and its impact?

Software designed for AI agents has the potential to deliver exponential value. As an industry we must collectively focus on building an open agent ecosystem and designing thoughtful AX to create a better, more open, and connected digital world.