
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate

class CommunicationAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""You are a communication assistant responsible for delivering clear, concise updates to the user based on the results from the crew history. 
            The crew has completed the following task, and it's your job to summarize the result for the user.
            
            Crew History: {agent_history}
            
            Based on the task result and the history provided, generate a clear, professional response that gives the user the necessary information or the outcome of the task in a direct manner.
            Provide only the outcome or necessary information as if directly addressing the user without mentioning any intermediaries.""",
            input_variables=["agent_history"]
        )
    
    def invoke(self, input_data):
        prompt = self.prompt_template.format(agent_history=input_data['agent_history'])
        llm_response = self.llm.invoke(prompt)
        llm_response.name = "Communication"
        return {"messages": [llm_response]}
