# 🤖 Autonomous Web Research Agent

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=Playwright&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)

A fully autonomous, agentic AI researcher that can understand a complex query, plan a research strategy, search the web, scrape website content, and synthesize a comprehensive Markdown report. 

Built with **LangGraph**, **Google Gemini**, **Tavily**, and **Playwright**.

## ✨ Features
- **Agentic Workflow**: Uses LangGraph's state graph to handle loops, memory, and intelligent tool routing.
- **Dynamic Web Search**: Integrates with the Tavily API for highly relevant, AI-optimized semantic web searches.
- **Deep Web Scraping**: Uses Playwright & BeautifulSoup to invisibly navigate to specific URLs, parse HTML, and extract clean text (bypassing ads and navigation elements).
- **Multi-Persona Architecture**: Splits the cognitive load into three distinct AI personalities: The Planner, The Researcher, and The Writer.
- **Free-Tier Optimized**: Configured to run completely for free using Google's Gemini 2.5 Flash API and Tavily's free tier.

---

## 🧠 System Architecture

The agent operates on a cyclical **State Graph** using LangGraph:

1. **Planner Node 📝**: Analyzes the user's initial prompt and breaks it down into a step-by-step numbered checklist of web queries.
2. **Researcher Node 🕵️‍♂️**: An LLM equipped with tools (`web_search` and `scrape_webpage`). It iterates over the plan, executing searches, clicking links, and reading pages until it gathers sufficient context.
3. **Writer Node ✍️**: Takes the massive raw conversation history and tool outputs, and synthesizes it into a clean, structured, and highly readable Markdown report.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- [Tavily API Key](https://tavily.com/) (Free)
- [Google Gemini API Key](https://aistudio.google.com/) (Free)

### 2. Installation
Clone the repository and navigate into the project directory:
```bash
git clone https://github.com/surabhi2408/agentic-web-researcher.git
cd agentic-web-researcher
```

Create a virtual environment and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
TAVILY_API_KEY=your_tavily_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 4. Run the Agent
Run the main script to start the agentic workflow:
```bash
python main.py
```
You will be prompted to enter a research topic. Once completed, the final output will be printed in the console and automatically saved to a file named `research_report.md`.

---

## 🛠️ Tech Stack
- **Routing & State Management**: LangGraph
- **LLM / Brain**: Google Gemini 2.5 Flash
- **Web Search API**: Tavily API
- **Browser Automation**: Playwright Async
- **HTML Parsing**: BeautifulSoup4

---

*Built with ❤️ exploring the bleeding edge of Agentic AI workflows.*
