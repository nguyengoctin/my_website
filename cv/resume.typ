// ==============================================================================
// Resume Source Code (Typst Engine)
// Standard Single-Column Layout (Jake's Resume / r/EngineeringResumes Standard)
// ==============================================================================

#set page(
  paper: "a4",
  margin: (x: 1.25cm, top: 1.1cm, bottom: 1.1cm),
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Arial", "Roboto"),
  size: 9.2pt,
  lang: "en",
)

#set par(justify: false, leading: 0.52em)

#let section(title) = {
  v(5pt)
  text(weight: "bold", size: 10.2pt)[#upper(title)]
  v(-5pt)
  line(length: 100%, stroke: 0.6pt + luma(80))
  v(2pt)
}

// ------------------------------------------------------------------------------
// Header
// ------------------------------------------------------------------------------
#align(center)[
  #text(size: 17pt, weight: "bold")[NGUYEN NGOC TIN] \
  #v(2pt)
  #text(size: 8.8pt)[
    +84 397 662 903 #h(4pt) | #h(4pt)
    Binh Tan, HCM #h(4pt) | #h(4pt)
    #link("mailto:ngoctin.work@gmail.com")[ngoctin.work\@gmail.com] #h(4pt) | #h(4pt)
    #link("https://github.com/ngoctinn")[github] #h(4pt) | #h(4pt)
    #link("https://www.linkedin.com/in/tin-nguyen-ngoc-2453372a3/")[linkedin] #h(4pt) | #h(4pt)
    #link("https://ngoctin.me")[ngoctin.me]
  ]
]

// ------------------------------------------------------------------------------
// Education
// ------------------------------------------------------------------------------
#section("Education")

#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold")[Saigon University (SGU)] --- #text(style: "italic")[Ho Chi Minh City, Vietnam] \
    Engineer in Information Technology --- Major: Information Systems \
    Language Proficiency: TOEIC 625 / 990 (Jun 2026)
  ],
  text(style: "italic")[Mar 2021 -- Jun 2026]
)

// ------------------------------------------------------------------------------
// Skills
// ------------------------------------------------------------------------------
#section("Skills")

#v(1pt)
- *Programming Languages:* Python, TypeScript, JavaScript, Java (Core)
- *Backend and Web Frameworks:* Django REST Framework, FastAPI, Next.js (App Router), React, RESTful APIs, WebSockets, TailwindCSS
- *Cloud and AI Engineering:* AWS (Lambda, SAM, Bedrock, DynamoDB, S3), LLM Integration (Gemini, Bedrock, Ollama), Agentic Workflows, MCP
- *Databases and Architecture:* PostgreSQL, Redis, DynamoDB (Single-Table Design), SQLite, Clean Architecture, Event-Driven Architecture
- *DevOps and Tools:* Docker, Git, GitHub Actions, Linux

// ------------------------------------------------------------------------------
// Experience
// ------------------------------------------------------------------------------
#section("Experience")

#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold")[FCAJ] --- #text(style: "italic")[Cloud Application Development Intern] \
    #text(size: 8.5pt, fill: luma(100))[Ho Chi Minh City, Vietnam]
  ],
  text(style: "italic")[Mar 2026 -- May 2026]
)
#v(1pt)
#list(
  [Architected and deployed an event-driven serverless backend prototype utilizing Python and AWS Lambda, decoupling core business logic and optimizing asynchronous event processing.],
  [Constructed standardized AWS SAM templates and architectural documentation, establishing reproducible local emulation and streamlining deployment workflows for the engineering team.],
  [Configured cloud monitoring and structured logging pipelines across serverless components, ensuring environment consistency and accelerating error diagnosis during testing.],
)

// ------------------------------------------------------------------------------
// Projects
// ------------------------------------------------------------------------------
#section("Projects")

#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold")[Bếp Dì 6 -- Online Ordering Platform (Zalo Mini App)] | #text(style: "italic")[Django REST, React, PostgreSQL, Redis] \
    #text(size: 8.5pt)[#link("https://github.com/ngoctinn/bepdi6-zalo-miniapp")[GitHub] | #link("https://ngoctin.me/posts/bep-di-6-zalo-mini-app-ordering-platform/")[Case Study]]
  ],
  text(style: "italic")[Aug 2026 -- Present]
)
#v(1pt)
#list(
  [Architected an end-to-end Food and Beverage online ordering system integrating a Zalo Mini App frontend (React 18, ZMP SDK) with a centralized Django REST API and PostgreSQL database.],
  [Engineered immutable order snapshotting and UUIDv4 idempotency keys via transaction.atomic() and Redis, eliminating duplicate checkouts and securing financial data integrity.],
  [Built a dynamic delivery fee engine using GPS Haversine distance calculations and integrated automated VietQR payment generation to streamline checkout flows.],
)

#v(3pt)
#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold")[Lexi -- AI-Powered English Speaking Tutor] | #text(style: "italic")[Next.js, TypeScript, Python, AWS] \
    #text(size: 8.5pt)[#link("https://github.com/ngoctinn/lexi-be")[GitHub] | #link("https://youtu.be/qPlBFtEk3pM?si=alCi4TsdS3b6tnI2")[Demo Video]]
  ],
  text(style: "italic")[Mar 2026 -- May 2026]
)
#v(1pt)
#list(
  [Architected a cloud-native serverless backend using AWS SAM, API Gateway, Lambda, Cognito, DynamoDB, and S3, enforcing Clean Architecture across Domain, Application, and Infrastructure layers.],
  [Engineered a real-time voice streaming pipeline via API Gateway WebSockets, orchestrating Amazon Transcribe, Bedrock, and Polly for low-latency conversational feedback.],
  [Designed a DynamoDB Single-Table schema with composite partition/sort keys and GSIs, supporting 6+ distinct access patterns for user sessions, flashcards, and dialogue history with single-digit millisecond latency.],
)

#v(3pt)
#grid(
  columns: (1fr, auto),
  [
    #text(weight: "bold")[Bilingual Movie-Based English Learning Platform] | #text(style: "italic")[Next.js, TypeScript, FastAPI, Python, SQLite] \
    #text(size: 8.5pt)[#link("https://github.com/nguyengoctin/hoc_tieng_anh_qua_phim_song_ngu")[GitHub] | #link("https://youtu.be/USj7dpTuOZI")[Demo Video]]
  ],
  text(style: "italic")[Mar 2026 -- Present]
)
#v(1pt)
#list(
  [Architected a full-stack language learning web application using Next.js App Router and FastAPI, delivering synchronized bilingual movie playback and contextual vocabulary acquisition.],
  [Implemented subtitle parsing and binary-search timestamp alignment algorithms with SQLite indexing, enabling instantaneous contextual vocabulary lookups during video streaming.],
  [Integrated Google Gemini API with structured prompt engineering to generate contextual grammar breakdowns, phonetic explanations, and collocations directly from movie dialogues.],
)
