from enum import Enum
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage
from .agents import *
from langgraph.graph import StateGraph, START, END
import os
import json
data = json.load(open('chat/llm_config.json'))

os.environ["GOOGLE_API_KEY"] = data['google_api']['api_key']

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=data['google_api']['llm_model'], temperature=0, max_tokens=None, timeout=None)


# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str 
    
    agent_history: Annotated[Sequence[BaseMessage], operator.add]


workflow = StateGraph(AgentState)

chatbot_obj = ChatbotAgent(llm)
workflow.add_node('Chatbot', lambda state: chatbot_obj.invoke(state))

entity_extractor_obj = EntityExtractorAgent(llm)
workflow.add_node('EntityExtractor', lambda state: entity_extractor_obj.invoke(state))



workflow.add_edge(START, 'EntityExtractor')
workflow.add_edge('EntityExtractor', 'Chatbot')
workflow.add_edge('Chatbot', END)

# workflow.add_node("AppointmentManagement", lambda state: AppointmentManagementAgent(llm).invoke(state))
# workflow.add_node("CommunicationAgent", lambda state: CommunicationAgent(llm).invoke(state)) 
# workflow.add_node("MedicalSearchAgent", lambda state: MedicalSearchAgent(llm).invoke(state))
# workflow.add_node("MedicationManagementAgent", lambda state: MedicationManagementAgent(llm).invoke(state))
# workflow.add_node("Supervisor", lambda state: SupervisorAgent(llm).invoke(state))


# workflow.set_entry_point("Supervisor")
# workflow.add_edge('AppointmentManagement', "Supervisor") 
# workflow.add_edge('MedicalSearchAgent', "Supervisor") 
# workflow.add_edge('MedicationManagementAgent', "Supervisor") 
# workflow.add_edge('CommunicationAgent', END) 

# members = ["AppointmentManagement", "CommunicationAgent", "MedicalSearchAgent", "MedicationManagementAgent"]
# member_options = {member:member for member in members}
# MemberEnum = Enum('MemberEnum', member_options)

# workflow.add_conditional_edges("Supervisor", lambda x: x["next"], member_options)

graph = workflow.compile()






