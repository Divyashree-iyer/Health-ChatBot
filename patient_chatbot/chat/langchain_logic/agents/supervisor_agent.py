from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from enum import Enum
from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser

members = ["AppointmentManagement", "CommunicationAgent", "MedicalSearchAgent", "MedicationManagementAgent"]
member_options = {member:member for member in members}
MemberEnum = Enum('MemberEnum', member_options)


class SupervisorOutput(BaseModel):
    next: MemberEnum = MemberEnum.CommunicationAgent





class SupervisorAgent:
    def __init__(self, llm):
        self.supervisor_parser = JsonOutputParser(pydantic_object=SupervisorOutput)
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""You are a supervisor tasked with managing a conversation between the
                crew of workers:  {members}. Given the following user request, 
                and crew responses respond with the worker to act next.
                Each worker will perform a task and respond with their results and status. 
                When finished with the task, route to communicate to deliver the result to 
                user. Given the conversation and crew history below, who should act next?
                Select one of: {options} 
                \n{format_instructions}\n""",
                input_variables=["message","agent_history"]
        ).partial(options=str(members), members=", ".join(members), 
            format_instructions = self.supervisor_parser.get_format_instructions())
    
    def chain(self):
        from langchain.chains import LLMChain
        return LLMChain(llm=self.llm, prompt=self.prompt_template, output_parser=self.supervisor_parser)
    
    def invoke(self, input_data):
        prompt = self.prompt_template.format( 
            messages=input_data['messages'], 
            agent_history = input_data.get('agent_history', [])
            )
        return self.chain().invoke(prompt)
