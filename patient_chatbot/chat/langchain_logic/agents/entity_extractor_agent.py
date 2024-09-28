
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from ...knowledge_graph import get_knowledge_graph
from ..entity_extractor import EntityExtractor
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from ...models import Patient
import json

class EntityExtractorAgent:
    def __init__(self, llm):
        self.knowledge_graph = get_knowledge_graph()
        self.llm = llm
        entity_extractor = EntityExtractor()
        self.tool = [
            Tool(
                name="extract_entities",
                func=entity_extractor.extract_entities,
                description="Extract health-related entities from user input."
            )
        ] 
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system","""You are an intelligent assistant designed to extract health-related information from user inputs. Use the `extract_entities` tool to identify and return relevant entities from the text.

            Your task includes:
            - Extracting the name of any medication mentioned.
            - Identifying the frequency of taking the medication (e.g., daily, weekly).
            - Extracting dosage information (e.g., "10 mg", "500 ml") mentioned in the input.
            - Finding any upcoming appointments, what changes are being requested, including the date, time and doctor's name
            - Identifying any references to medical conditions or health issues mentioned (e.g., "diabetes", "high blood pressure").
            - Ignoring irrelevant or sensitive topics and only focusing on health-related information.
             
            Please respond with a structured summary of the extracted entities in JSON format. If no information is found for a particular entity, exclude it from the output. 
            """),
            ("human","{message}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
    
    def get_agent(self):
        agent = create_tool_calling_agent(self.llm, self.tool, self.prompt_template)
        executor = AgentExecutor(agent=agent, tools=self.tool, 
                    return_intermediate_steps= False, verbose = False)
        return executor
    
    def get_patient_name(self):
        try:
            self.patient = Patient.objects.first()  
            return f"{self.patient.first_name} {self.patient.last_name}"
        except Patient.DoesNotExist:
            return "Patient not found"
        
    def invoke(self, input_data):
        
        prompt = {"message":input_data['messages']}
        
        llm_response = self.get_agent().invoke(prompt)
        output_str = llm_response['output']

        output = json.loads(output_str[output_str.index('{'):output_str.rindex('}')+1])
        medical_condition = output.get('conditions', None)
        medication = output.get('medication', None)
        dosage = output.get('dosage', None)
        frequency = output.get('frequency', None)
        appointment = output.get('appointment', None) 

        if medical_condition or medication or dosage or frequency:
            self.knowledge_graph.add_patient_info(
                patient_name=self.get_patient_name(), 
                medical_condition=medical_condition, 
                medication=medication, 
                dosage=dosage, 
                frequency=frequency
            )
        
        if appointment:
            requested_change = appointment.get('requested_change', None)
            new_time = appointment.get('new_time', None)
            doctor_name = appointment.get('doctor_name', None)
            
            self.knowledge_graph.add_appointment_change(
                patient_name=self.get_patient_name(),
                requested_change=requested_change,
                new_time=new_time,
                doctor_name=doctor_name  
            )

        # llm_response.name = "EntityExtractor"
        return { "next": "Chatbot", "extracted_entities": [output_str]}
