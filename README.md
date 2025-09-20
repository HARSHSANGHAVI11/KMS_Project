✅ Project Overview

In many companies, employees work on projects in isolation. Knowledge about the project is often stored in personal notes or remains in the mind of individual employees.
When an employee leaves the company, critical knowledge is lost. New employees struggle to understand the project structure, business logic, or technical implementation, which leads to delays, repeated mistakes, and reduced productivity.

Our solution – the AI Powered Knowledge Management System (KMS) – solves this problem by providing a centralized, structured, and intelligent knowledge base.

🎯 Purpose

• Provide a centralized platform for employees to upload project documents (PDF, DOCX, TXT).
• Allow employees to structure knowledge updates under key categories (Business Logic, Security Parameters, etc.).
• Enable intelligent querying of documents and updates using AI-based question answering.
• Maintain full history of updates and chat interactions.
• Support HR with dashboards to track employee activity and provide feedback.

This helps ensure that project knowledge is retained within the organization, accessible by anyone at any time.

⚡ Key Features

✅ Upload & Embed
 – Employees upload documents.
 – Documents are processed and stored with embedded vectors for semantic search.

✅ Ask Questions
 – Employees can ask natural language questions.
 – The system retrieves precise answers from the uploaded knowledge base using a powerful AI retrieval model.

✅ Update KMS Knowledge Base
 – Structured knowledge updates organized under categories like:
  • Business Concept
  • Core Business Logic
  • Security Parameters
  • Absolute To-Do List
  • Error Handling
  • Q&A Sessions
 – Updates are appended to project-specific files and vector indices for semantic search.

✅ AI News Feed
 – Displays latest AI, ML, and .NET industry news in a scrolling footer.

✅ Feedback System
 – Employees can send feedback to HR.
 – HR can send feedback to employees.
 – Feedback history is stored and displayed.

✅ HR Dashboard
 – View employee uploads.
 – View total feedback.
 – View employee performance statistics.

⚙️ Technology Stack

• Frontend & Backend: Streamlit
• Embedding Model: Sentence Transformers (local model: all-MiniLM-L6-v2)
• Vector Store: FAISS for semantic search
• Database: PostgreSQL for user and feedback data
• Document Handling: python-docx for .docx files
• AI News API: RapidAPI News API
• Containerization: Docker (used for sales automation project but isolated)
• Python Libraries: torch, faiss, psycopg2, bcrypt, pickle, os, datetime

🚀 Workflow
Employee logs in to the KMS portal.
Uploads project-related documents for embedding.
Embedding model converts documents into vector representations for semantic retrieval.
Employees can submit structured updates with timestamps under various categories.
Employees can ask questions in natural language. System retrieves answers using vector similarity search.
HR has a dashboard to track overall activity, manage feedback, and view uploaded files.
AI News Feed keeps employees updated on industry developments.

🎯 Benefits

✔️ Centralized knowledge base.
✔️ Easy retrieval of specific project information.
✔️ Reduces dependency on individual employee knowledge.
✔️ Preserves project updates and history.
✔️ Improves onboarding process for new employees.
✔️ Provides real-time feedback mechanism.

Youtube Link: 
Project Demo: https://youtu.be/O_J9FAWT-KM
