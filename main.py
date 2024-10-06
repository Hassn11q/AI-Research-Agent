# Dependencies
import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process , LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Define LLM
llm = LLM(
    model="llama-3.1-70b-versatile",
    temperature=0.0,
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

# Define Fastapi app
app = FastAPI()

# Define Pydantic model
class ResearchTopic(BaseModel):
    topic: str

# Define Search tools
search_tool = SerperDevTool()


# Define Agent
researcher = Agent(
    role="Expert Researcher",
    goal="Conduct comprehensive research on any given topic with the expertise of a PhD professor",
    verbose=True,
    memory=True,
    llm=llm,
    backstory=(
        "I am an accomplished researcher with a PhD in multiple disciplines. "
        "I have extensive experience in conducting in-depth research using various sources "
        "and tools. My expertise lies in analyzing and synthesizing information from diverse "
        "sources to provide comprehensive and insightful findings."
    ),
    tools=[search_tool]
)

# Define app route
@app.post("/research_topic")
async def research_topic(research_topic: ResearchTopic):
    research_task = Task(
        description=f"Conduct comprehensive research on the topic '{research_topic.topic}' as an expert professor with a PhD.",
        expected_output="A detailed report on the research topic, including relevant information, analysis, and insights.",
        tools=[search_tool],
        agent=researcher
    )
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True , 
        process=Process.sequential
    )
    results = crew.kickoff(inputs={"topic": research_topic.topic})
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)