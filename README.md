🧠 NEXUS

NEXUS is a research discovery platform that aggregates and organizes technology research papers into a structured, filterable feed for students and professionals.

🚩 Problem

Technology research is fragmented across multiple platforms such as arXiv, blogs, and reports. This makes it difficult for learners and early-stage builders to stay updated efficiently.

💡 Solution

NEXUS centralizes research content and presents it through a clean, topic-driven interface that allows users to explore relevant papers quickly and effectively.

🏗 Architecture

Backend: FastAPI

Data Source: arXiv API

Database: SQLite (metadata storage only)

Frontend: Static HTML + Tailwind CSS

AI (Planned): Google Gemini for intent-based research discovery

🔧 Current Features

Fetches and stores research paper metadata from arXiv

Topic-based research filtering

Paginated research feed

Responsive, modern UI

🤖 AI Integration (Planned)

NEXUS is designed to support a conversational assistant powered by Google Gemini, which will understand user intent and dynamically surface relevant research.

The AI layer is non-blocking and optional, ensuring system stability even if AI services are unavailable.

🚀 Backend is hosted on Render

https://nexus-n77m.onrender.com

🌐 Frontend is hosted on Netlify

https://admirable-arithmetic-46cc7a.netlify.app

The frontend is a static HTML application.
