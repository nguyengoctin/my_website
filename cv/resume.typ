// ==============================================================================
// Resume Source Code (Typst Engine)
// Standard Single-Column Layout (Jake's Resume / r/EngineeringResumes Standard)
// ==============================================================================

#set page(
  paper: "a4",
  margin: (x: 1.25cm, y: 1.25cm),
)

#set text(
  font: ("Liberation Sans", "DejaVu Sans", "Arial", "Roboto"),
  size: 9.5pt,
  lang: "en",
)

#set par(justify: false, leading: 0.55em)

#let section(title) = {
  v(6pt)
  text(weight: "bold", size: 10.5pt)[#upper(title)]
  v(-5pt)
  line(length: 100%, stroke: 0.6pt + luma(80))
  v(2pt)
}

// ------------------------------------------------------------------------------
// Header
// ------------------------------------------------------------------------------
#align(center)[
  #text(size: 18pt, weight: "bold")[NGUYEN NGOC TIN] \
  #v(2pt)
  #text(size: 9pt)[
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
- *Backend and Web Frameworks:* FastAPI, Next.js (App Router), React, RESTful APIs, WebSockets, TailwindCSS
- *Cloud and AI Engineering:* AWS (Lambda, SAM, Bedrock, DynamoDB, S3), LLM APIs (Gemini, Bedrock), Agentic Workflows, MCP
- *Databases and Architecture:* PostgreSQL, DynamoDB (Single-Table Design), SQLite, Clean Architecture, Event-Driven Architecture
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
  [Developed a full-stack Next.js (App Router) interface with Tailwind CSS, integrating secure JWT auth workflows and automating CI/CD deployments via AWS Amplify.],
)

#v(4pt)
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
