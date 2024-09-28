
from langchain_core.prompts import PromptTemplate
from ...knowledge_graph import get_knowledge_graph
from ...models import Patient
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory

class ChatbotAgent:
    def __init__(self, llm):
        self.patient = Patient.objects.first()
        self.llm = llm
        # self.memory = ConversationSummaryMemory(llm=llm)
        self.memory =  ConversationBufferMemory()
        # self.kg_memory = KnowledgeGraphMemory(knowledge_graph=get_knowledge_graph())

        self.prompt_template = PromptTemplate(
            template="""You are a health management and appointment management chatbot. Your task is to answer health realted queries of patients such as giving information about their diet, medicines and appointments with doctors. 
            If the patient asks any irrelevant question then kindly reply that you can not answer their question.
            
            Here is the patient message - {message}
            Here is the patient informaiton - {patient_info}
            This is the medical information about the patient: {patient_medical_info}
            Here is the patient's appointment information - {patient_appointments}
            Here is a summary of the previous conversation: {conversation_summary}
            
            If the user wants to peform an action (e.g., change, cancel) on their next appointment then make sure to gather information about new date, time and doctor's name. If any of these entities are missing then ask follow up questions. You can just make update on the next upcoming appointment. Do not allow changes for future appointments beyond the next one.
            Make a python dictionary that stores this information in the following keys - datetime, doctor_name

            If the user is requesting to reschedule an appointment, do not actually reschedule the appointment, but prepare a response indicating that the request will be conveyed to the doctor. Respond in a professional and helpful manner. 

            Please respond in plain text without using any formatting like bold or italics or using json code or structured data formats.
            """,
            input_variables=["message", "patient_info", "patient_appointments", "patient_medical_info", "conversation_summary"]
        )
    
    def get_patient_info(self):
        try:
            return f"Name: {self.patient.first_name} {self.patient.last_name}, DOB: {self.patient.dob}, Doctor: {self.patient.doctor_name}"
        except Patient.DoesNotExist:
            return "Patient not found"
        
    def get_appointment_info(self):
        appointments = [self.patient.last_appointment, self.patient.next_appointment]
        return ", ".join([f"{apt.strftime('%Y-%m-%d %H:%M')}" for apt in appointments])
    
    def get_patient_medical_info(self):
        try:
            return f"Medical Condition: {self.patient.medical_condition}, Medical Regimen: {self.patient.medication_regimen}"
        except Patient.DoesNotExist:
            return "Patient not found"
        
    def invoke(self, input_data):
        conversation_summary = self.memory.load_memory_variables({})
        prompt = self.prompt_template.format(
            message=input_data['messages'][0].content, 
            patient_info=self.get_patient_info(),
            patient_appointments=self.get_appointment_info(),
            patient_medical_info = self.get_patient_medical_info(),
            conversation_summary=conversation_summary
            )
        llm_response = self.llm.invoke(prompt)
        llm_response.name = "Chatbot"
        self.memory.save_context({"input": str(input_data['messages'][0].content)}, {"output": str(llm_response.content)})
        return {"messages": [llm_response]}
