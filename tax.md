# Nigeria Tax Reform Bills Q&A Assistant
## Team Roles, Structure & Project Management Guide

---

## 🎯 TEAM COMPOSITION (4 PEOPLE)

### Role 1: **AI/ML Engineer (Lead)**
**Primary Owner:** Agentic RAG System

#### Responsibilities:
- Design and implement the core LangGraph agent logic
- Build conditional retrieval system (knows when to fetch docs vs. when not to)
- Implement conversation memory/context management
- Set up vector database (Chroma) for semantic search
- Handle document chunking and embeddings strategy
- Ensure source citation implementation
- Optimize retrieval accuracy and response quality
- Write unit tests for AI components

#### Deliverables:
- Fully functional AI engine (LangGraph code)
- Vector database with tax documents
- Agent decision logic documentation
- Test cases for different query types

#### Skills Needed:
- LangChain & LangGraph expertise
- Vector database knowledge
- Prompt engineering
- Python proficiency

---

### Role 2: **Backend Engineer**
**Primary Owner:** FastAPI Implementation

#### Responsibilities:
- Build RESTful API endpoints (chat endpoint, session management, etc.)
- Implement session/conversation storage (database schema)
- Connect FastAPI to the AI engine
- Handle request/response formatting
- Implement error handling and validation
- Set up logging for debugging
- Optimize API performance
- Write unit tests for API endpoints

#### Deliverables:
- FastAPI application with working endpoints
- Database schema for conversation sessions
- API documentation (Swagger/OpenAPI)
- Error handling middleware
- Test cases for all endpoints

#### Skills Needed:
- FastAPI expertise
- Database design (SQL/NoSQL)
- REST API principles
- Python proficiency

---

### Role 3: **Frontend Engineer**
**Primary Owner:** React UI Implementation

#### Responsibilities:
- Build clean, professional chat interface
- Implement conversation display and history
- Create source citation display component
- Handle loading states and error messages
- Build responsive design (mobile & desktop)
- Connect to FastAPI backend
- Optimize UI/UX for user experience
- Write component tests

#### Deliverables:
- React application with chat interface
- Responsive design that works on all devices
- Source citation component
- Conversation history display
- Loading and error states

#### Skills Needed:
- React expertise
- Tailwind CSS proficiency
- API integration (fetch/axios)
- UI/UX design sense

---

### Role 4: **Product Manager (YOU)**
**Primary Owner:** Vision, Strategy & Coordination

#### Responsibilities:

**Strategic Planning:**
- Define product requirements and success criteria
- Create user personas (Aunty Ngozi, Chidi, Governor Yahaya, etc.)
- Document user stories and use cases
- Prioritize features based on impact

**Project Coordination:**
- Manage timeline and milestones
- Track progress against deadline (Jan 7, 2026, 10 AM)
- Facilitate communication between team members
- Hold daily standups and weekly planning sessions
- Identify and unblock bottlenecks
- Maintain project documentation

**Quality Assurance:**
- Define acceptance criteria for each feature
- Create test scenarios for the Q&A assistant
- Verify that the solution actually solves the problem
- Gather feedback on user experience

**Deliverables:**
- Product requirements document (PRD)
- User stories and acceptance criteria
- Project timeline and milestones
- Weekly progress reports
- Final presentation/demo script

#### Skills Needed:
- Communication and leadership
- Project management
- Domain understanding (Nigerian tax reforms)
- Attention to detail

---

## 📊 PROJECT MANAGEMENT SETUP

### Using a PM Tool (Recommendations)

**Best Options for Your Team:**
1. **Asana** (Most user-friendly, great for teams of 4)
2. **Trello** (Simple Kanban boards, perfect for visual tracking)
3. **Monday.com** (Powerful, good reporting)
4. **Notion** (Free, flexible, all-in-one)

**My Recommendation:** **Asana** or **Trello** for this project

---

## 🛠️ HOW TO SET UP YOUR PM TOOL (Using Asana as Example)

### Step 1: Create Project Structure
```
PROJECT: Nigeria Tax Reform Q&A Assistant
│
├── PHASE 1: Planning & Setup (Week 1)
│   ├── Finalize requirements
│   ├── Design system architecture
│   ├── Set up development environment
│   └── Gather/organize tax documents
│
├── PHASE 2: Core Development (Week 1.5)
│   ├── AI Engine Development
│   ├── Backend API Development
│   ├── Frontend UI Development
│   └── Database Setup
│
├── PHASE 3: Integration & Testing (Week 2)
│   ├── Connect AI to Backend
│   ├── Connect Backend to Frontend
│   ├── End-to-end testing
│   └── Bug fixes
│
└── PHASE 4: Polish & Delivery (Final Days)
    ├── Create demo video
    ├── Write documentation
    ├── Prepare presentation
    └── Final submission
```

### Step 2: Create Tasks with Clear Structure

**For AI Engineer:**
```
Task: Implement Conditional Retrieval Logic
- Description: Build agent that decides when to retrieve documents
- Assigned to: AI Engineer
- Due date: Dec 31, 2025
- Dependencies: Document indexing complete
- Subtasks:
  - Research LangGraph best practices
  - Write decision logic
  - Test with 10 different query types
  - Document edge cases
```

**For Backend Engineer:**
```
Task: Build Chat API Endpoint
- Description: Create FastAPI endpoint for /api/chat
- Assigned to: Backend Engineer
- Due date: Dec 31, 2025
- Dependencies: AI engine API defined
- Subtasks:
  - Design request/response schema
  - Implement endpoint
  - Add error handling
  - Write tests
  - Document endpoint
```

**For Frontend Engineer:**
```
Task: Build Chat Interface Component
- Description: Create React chat component with message display
- Assigned to: Frontend Engineer
- Due date: Dec 31, 2025
- Dependencies: Backend endpoints documented
- Subtasks:
  - Create message input component
  - Create message display component
  - Add typing indicators
  - Implement scroll behavior
  - Test responsiveness
```

### Step 3: Set Dependencies & Milestones

```
CRITICAL PATH (Tasks that block other tasks):
1. Document preparation & indexing (AI Engineer) → Blocks everything
2. API endpoint design (All) → Blocks Backend & Frontend
3. Backend implementation → Blocks Frontend integration
4. Integration & testing → Blocks demo creation
```

---

## 🎤 YOUR ROLE AS PRODUCT MANAGER - Week by Week

### WEEK 1 (Dec 23-29, 2025)

**Day 1-2: Requirements & Planning**
- [ ] Hold kickoff meeting with all 4 team members
- [ ] Define detailed user stories
- [ ] Create acceptance criteria for each feature
- [ ] Document questions about tax reforms to clarify
- [ ] Create "Definition of Done"

**Day 3-4: Design & Documentation**
- [ ] Gather and organize tax reform documents
- [ ] Create system architecture diagram
- [ ] Write technical requirements document
- [ ] Define API contract (request/response formats)
- [ ] Create UI wireframes/mockups

**Day 5-7: Team Alignment**
- [ ] Review all documents with team
- [ ] Clarify doubts about requirements
- [ ] Set up PM tool with all tasks
- [ ] Establish daily standup schedule (15 min, 9 AM)
- [ ] Create Slack/communication channel
- [ ] First progress check

---

### WEEK 2 (Dec 30, 2025 - Jan 6, 2026)

**Daily (During Development):**
- [ ] 15-min standup: What did you do? What will you do? Any blockers?
- [ ] Monitor task progress in PM tool
- [ ] Unblock team members immediately
- [ ] Track any risks or delays

**3x Weekly (Mon/Wed/Fri):**
- [ ] 30-min sync with each engineer
- [ ] Review code quality
- [ ] Verify acceptance criteria being met
- [ ] Test features as they're completed

**Quality Assurance:**
- [ ] Create test scenarios for Q&A assistant
- [ ] Test accuracy of answers (does it cite sources correctly?)
- [ ] Verify conversation memory works
- [ ] Check error handling
- [ ] Validate UI/UX is intuitive

**Risk Management:**
- [ ] Identify any delays immediately
- [ ] Adjust timeline if needed
- [ ] Create contingency plans
- [ ] Escalate blockers to instructors if needed

---

### FINAL DAYS (Jan 6-7, 2025)

**Jan 6 (Tuesday):**
- [ ] All code merged and tested
- [ ] Demo video recorded
- [ ] Presentation slides prepared
- [ ] README finalized
- [ ] GitHub repository organized

**Jan 7 (Wednesday Morning - DEADLINE):**
- [ ] Final submission through Google Sheet
- [ ] All deliverables uploaded
- [ ] Team verification check

---

## 📋 PRODUCT MANAGER'S ESSENTIAL DOCUMENTS

### 1. **Product Requirements Document (PRD)**
```markdown
# Nigeria Tax Reform Bills Q&A Assistant - PRD

## Problem Statement
Nigerian citizens are confused about tax reforms due to complex documents.

## Solution
AI-powered assistant that answers questions about tax reforms 
with citations from official documents.

## User Personas
- Aunty Ngozi: Small business owner, needs to understand tax impact
- Chidi: Software developer, wants to know income tax changes
- Governor Yahaya: Concerned about VAT derivation

## Core Features
1. Question & Answer capability
2. Source citations
3. Conversation memory
4. Accurate, helpful responses

## Success Criteria
- 90%+ answer accuracy
- Sources cited for every response
- Conversation context remembered
- Average response time < 3 seconds
```

### 2. **User Stories Template**
```markdown
AS A [user type]
I WANT [capability]
SO THAT [benefit]

ACCEPTANCE CRITERIA:
- System retrieves relevant documents for tax questions
- Answers include official sources
- Follow-up questions use conversation history
- System doesn't retrieve documents for greetings
```

### 3. **Weekly Status Report Template**
```markdown
# Weekly Status Report - Week [X]

## Overall Progress: [80%]

## Completed This Week:
- ✅ AI engine conditional retrieval working
- ✅ Backend API endpoints created
- ✅ Frontend chat component built

## In Progress:
- 🔄 Integration testing
- 🔄 Bug fixes

## Blockers:
- ⚠️ Document chunking optimization needed

## Next Week Plan:
- Complete integration testing
- Record demo video
- Finalize documentation
```

---

## 💬 COMMUNICATION STRUCTURE

### Daily (9:00 AM - 15 minutes)
**Standup Meeting (All 4 team members)**
- What did you complete yesterday?
- What will you do today?
- Any blockers?
- Use Asana to track this

### 2x Weekly (Mon/Thu - 30 minutes)
**Technical Sync with Engineers**
- Code review
- Architecture decisions
- Technical blockers
- Use Google Meet + screen sharing

### 1x Weekly (Friday - 1 hour)
**Full Team Sync**
- Week review
- Demo completed features
- Plan next week
- Update PM tool

### Async Communication
**Slack Channels:**
- #general: Team announcements
- #ai-engine: AI engineer discussions
- #backend: Backend engineer discussions
- #frontend: Frontend engineer discussions
- #blockers: Flag urgent issues

---

## 🎯 YOUR SUCCESS METRICS AS PM

| Metric | Target | Current |
|--------|--------|---------|
| On-time delivery | Jan 7, 10 AM | TBD |
| Features complete | 100% of core features | TBD |
| Code quality | 0 critical bugs | TBD |
| Team satisfaction | All team members feel supported | TBD |
| Documentation | Complete & clear | TBD |

---

## 🚀 KEY PM BEST PRACTICES FOR THIS PROJECT

**1. Clarity Over Everything**
- Write requirements so clear that a 10-year-old understands
- Ask clarifying questions early
- Document every decision

**2. Unblock Fast**
- If someone is stuck, solve it within 2 hours
- Escalate if you can't solve it
- Never let blockers sit for a day

**3. Regular Communication**
- Over-communicate, not under
- Update team immediately on changes
- Share progress publicly (celebrate wins!)

**4. Quality Focus**
- Test features as they're built
- Don't wait until the end to test
- Catch bugs early

**5. Risk Management**
- Identify risks early
- Have backup plans
- Build in buffer time (you have 2 weeks!)

**6. Team Support**
- Check in on team morale
- Remove obstacles
- Celebrate progress
- Be the team's biggest cheerleader

---

## 📌 CRITICAL DATES

| Date | Event | Your Action |
|------|-------|------------|
| Dec 23 | Project kickoff | Hold kickoff meeting |
| Dec 27 | 25% progress expected | Check all tasks on track |
| Jan 1 | 50% progress expected | Code review with team |
| Jan 3 | 75% progress expected | Testing & bug fixes |
| Jan 6 | 95% progress expected | Final polish |
| Jan 7, 10 AM | **DEADLINE** | Submit everything |
| Jan 9 | Presentation | Present to class |

---

## 💡 FINAL TIPS FOR SUCCESS

1. **Start with clarity** - Spend time on requirements before coding
2. **Setup tooling first** - Get PM tool working from day 1
3. **Establish rhythm** - Daily standups create accountability
4. **Remove friction** - Make it easy for team to communicate
5. **Celebrate wins** - Acknowledge completed milestones
6. **Test constantly** - Don't wait for the end
7. **Document as you go** - Don't leave it for last
8. **Stay focused** - Don't add features beyond the core requirement

---

## 🎬 YOUR PM WORKFLOW (Daily)

```
09:00 → 15-min standup with team
09:30 → Review Asana for blockers
10:00 → 1-on-1 with one team member (rotate)
11:00 → Test completed features
12:00 → Update documentation
13:00 → Plan/adjust timeline if needed
14:00 → Work on your own deliverables (PRD, slides, etc.)
15:00 → Buffer for unexpected issues
```

---

## ✅ CHECKLIST FOR PROJECT KICKOFF

- [ ] All team members know their role
- [ ] Asana/Trello project created with all tasks
- [ ] Daily standup scheduled
- [ ] Slack channel created
- [ ] Requirements document written
- [ ] System architecture documented
- [ ] Tax documents organized
- [ ] API contract defined
- [ ] UI wireframes created
- [ ] Development environment setup guide written

**Now you're ready to build! 🚀**