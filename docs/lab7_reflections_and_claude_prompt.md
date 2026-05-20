# Lab 7 Reflections and Claude Code Build Prompt

## Draft reflections

### 1. What is Agentic AI?
A normal LLM is mostly text in, text out. It can give advice, summarize a job description, or write a plan, but it depends on me to bring all the information into the chat. A Level 2 agent can use tools, but I still direct each step. A more agentic workflow is different because I design the system, connect the tools, set the guardrails, and then give the agent a goal.

For my custom lab, the recurring task is keeping my job pipeline warm while traveling abroad with only my phone. A Level 2 version would require me to paste one job description at a time and ask if it is a fit. A Level 3 version can call a candidate profile tool, pull job search parameters, retrieve a job feed, and then rank the available roles into an application queue. I still want to stay in the loop before applying, changing my resume, or contacting anyone, because the agent can support the decision but should not own the decision.

### 2. Building the Job Scout Agent
I built a Job Scout Agent in n8n to help me prioritize job opportunities while traveling. The workflow starts with a chat trigger, then sends the request to an AI Agent connected to Claude Sonnet. The agent has three tools: Candidate Profile, Job Search Parameters, and Job Feed. The Candidate Profile tool gives the agent my background, internships, target roles, and weak-fit signals. The Job Search Parameters tool defines what I am looking for, including target industries, locations, salary preferences, start date timing, and scoring rules. The Job Feed tool returns sample job postings for the agent to rank.

In the successful run, the agent called all three tools and confirmed what each one returned before ranking the jobs. It ranked Anduril’s Procurement Analyst role and RTX’s Supply Chain Rotational Associate role highest, which made sense based on my sourcing, supply chain, and aerospace background. The output was useful because it did not just summarize jobs. It created a phone-friendly application queue with fit scores, risks, and next steps.

### 3. Breaking the Agent
To test failure behavior, I deactivated the Job Feed tool and ran the same job recommendation prompt again. This was the most important break test because the job feed is the agent’s source of actual opportunities. Without it, the agent should not create a ranked list.

The agent failed safely. It called the remaining tools, noticed that the Job Feed tool was unavailable, and stopped instead of inventing jobs. That was exactly the behavior I wanted. It showed that the guardrail in the system prompt worked. A weaker agent might have created fake job postings from general knowledge, which would waste time and could send me after roles that do not exist. This test showed that tools make an agent useful, but guardrails determine whether it fails safely.

### 4. Bad-Fit Test
I tested the agent on a clearly misaligned role: Senior Data Scientist, Marketplace Optimization at Uber. The role had a high salary and a strong company name, but it required production machine learning, advanced Python, statistics, and model deployment. Those requirements do not match my target path in sourcing, procurement, operations, planning, or supply chain.

The agent correctly scored the role low and recommended Skip. It explained that the role was a poor fit because it was pure data science, too technical, and misaligned with my career direction. I liked this result because it showed the agent was not blindly chasing salary or brand name. A useful job-search agent should protect my attention, not just show me impressive companies.

### 5. Auditing the Output
I audited the output by checking whether the ranked jobs came from the Job Feed and whether the agent invented anything outside the tool data. In the successful run, the agent ranked only the eight jobs from the structured Job Feed and clearly stated that the feed was sample data. It also flagged salary estimates, manual verification requirements, and missing posted dates instead of pretending those details were confirmed.

The ranking logic was mostly reasonable. Anduril, RTX, the Space Systems Buyer/Planner role, Blue Origin, and Parker Hannifin were ranked above weak-fit roles like Uber Data Scientist, RetailCo Marketing Analytics, and Apple Senior Strategic Sourcing Manager. The biggest limitation is that the feed was sample data, not live postings. If this system processed a large job queue every week, I would not line-by-line audit every result manually. Instead, I would use automated checks: verify that every ranked job has a source, flag missing salary or application links, deduplicate postings, sample-check high-fit recommendations, and track whether the agent’s top recommendations are actually worth applying to.

### 6. AI Governance Brief
Purpose and scope: The Job Scout Agent is allowed to rank job opportunities, explain fit, and suggest next actions. It should never apply to jobs, message recruiters, rewrite my resume with unverified claims, or bypass job-board restrictions.

Data access and privacy: The agent should only access career data that I intentionally provide, such as my resume profile, job preferences, and job postings. It should not store sensitive login information, scrape protected platforms, or expose personal job-search data publicly.

Human oversight: Every recommendation requires human review before action. I should approve applications, networking messages, resume edits, and any decision to pursue or skip a role.

Testing, auditing, and accountability: The system should be tested against strong-fit, medium-fit, and bad-fit roles. I would track whether the agent invents jobs, misreads requirements, overstates my qualifications, or recommends roles that do not match my stated preferences.

Monitoring and sunset: The agent should be reviewed if its recommendations become stale, if job sources stop working, if it starts ranking poor-fit jobs highly, or if it relies on outdated profile information. If the job feed fails, the system should stop instead of inventing data.

The hardest layer to get right at scale is data access and source quality. The tool is only valuable if it sees real, current job postings, but many job platforms restrict scraping or require logins. The system has to stay useful without crossing platform boundaries or producing fake opportunities.

### 7. Should We Be Using AI Agents for This?
The biggest concern is not that the agent will replace human judgment. The bigger concern is that a bad agent could quietly create a misleading job pipeline. If it invents roles, overstates fit, ignores seniority requirements, or pushes me toward jobs that do not match my goals, it could waste time and damage my application strategy.

I still think the benefits outweigh the risks if the system is designed correctly. The guardrail is simple: the agent can recommend, rank, and draft notes, but it cannot apply or contact anyone without my approval. It also cannot invent jobs or bypass restricted platforms. If the system only works from verified feeds, manually supplied postings, or job alerts, then it becomes a useful assistant instead of a risky automation.

### 8. My Personal Agent Reflection
I would let this agent run in the background to collect and rank opportunities, but I would not let it run unsupervised all the way through application submission. Before I trusted it more, it would need to prove over several weeks that it can rank jobs accurately, avoid fake postings, reject poor-fit roles, and produce useful next steps from real job feeds.

Compared with healthcare agents like an insurance appeal agent, the stakes are lower, but the governance logic is similar. In both cases, the agent can draft and prioritize, but a human should review before anything is submitted. For my job search, the risk is wasted time or poor positioning. In healthcare, the risk could affect patient care or reimbursement. The common lesson is that agentic AI is strongest when it expands human capacity without removing human accountability.

## Claude Code prompt

Paste this into Claude Code from `~/Documents/mis432-ai-in-business`:

```text
We are building Lab 7 for my MIS 432 AI in Business portfolio.

Repo:
~/Documents/mis432-ai-in-business

Create:
lab7/index.html

Also update the homepage/index.html to add a Lab 7 card/link if the homepage already lists previous labs.

Lab title:
Agentic AI Lab: Job Scout Agent for a Mobile Job Pipeline

Student:
Kenyon Woodley

Course:
MIS 432 · AI in Business · Western Washington University

Context:
The original lab asked students to build an agentic AI workflow in n8n, test it, break it, audit it, discuss governance, and publish a portfolio page. My professor approved a custom spin. Instead of the healthcare insurance appeal agent, I built a Job Scout Agent to help keep my job pipeline warm while traveling abroad with only my phone.

The agentic workflow:
Chat Trigger → AI Agent → Anthropic Chat Model
AI Agent tools:
1. Candidate Profile
2. Job Search Parameters
3. Job Feed

Artifacts are saved in:
lab7/assets/

Use these assets if present:
- job-scout-agent.json
- workflow-canvas.png
- normal-output-and-logs.png
- break-test-job-feed-deactivated.png
- bad-fit-test-output.png

If an image is missing, still build the page and create a clean placeholder card that says "Screenshot captured in n8n workflow logs."

Design:
- Single HTML file
- Inline CSS only
- No external dependencies
- Professional portfolio style
- Dark crimson / black / white theme inspired by the assignment
- Clean cards
- Strong executive summary
- Clear agent workflow diagram
- Screenshots embedded where available
- Code/system prompt snippets in readable blocks
- Mobile responsive
- Avoid em dashes in visible writing
- Make it polished enough for LinkedIn or recruiter review

Page sections:
1. Hero
2. Executive Summary
3. Key Takeaways
4. What is Agentic AI?
5. Workflow Architecture
6. Building the Job Scout Agent
7. Breaking the Agent
8. Bad-Fit Test
9. Auditing the Output
10. AI Governance Brief
11. Should We Be Using AI Agents for This?
12. My Personal Agent Reflection
13. Future Version
14. Footer

Use the reflection text from docs/lab7_reflections_and_claude_prompt.md if available. Also use the output text files from lab7/text/ as supporting evidence.

Technical tasks:
- Create lab7/index.html
- Copy or reference assets from lab7/assets
- Update homepage/index.html with Lab 7 card/link
- Keep page self-contained aside from local image assets
- Commit with message: Add Lab 7 agentic AI job scout
- Push to GitHub

After building:
- Show changed files
- Confirm lab7/index.html exists
- Confirm homepage has Lab 7 link
- Confirm commit and push succeeded
```
