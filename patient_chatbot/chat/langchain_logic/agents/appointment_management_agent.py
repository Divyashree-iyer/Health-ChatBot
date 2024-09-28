
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from ...models import Patient
from ..entity_extractor import EntityExtractor
from langchain_core.messages import AIMessage

class AppointmentManagementAgent:
    def __init__(self, llm):
        self.patient = Patient.objects.first()
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""You are an appointment management assistant for a medical practice. 
            Please analyze the user's request and respond accordingly.
            
            User Message: {message}
            Patient Information: {patient_info}
            Current Appointments: {current_appointments}
            
            If the user wants to peform an action (e.g., change, cancel) on their next appointment then make sure to gather information about new date, time and doctor's name. If any of these entities are missing then ask follow up questions. You can just make update on the next upcoming appointment. Do not allow changes for future appointments beyond the next one.
            Make a python dictionary that stores this information in the following keys - datetime, doctor_name

            If the user is requesting to reschedule an appointment, do not actually reschedule the appointment, but prepare a response indicating that the request will be conveyed to the doctor. Respond in a professional and helpful manner.
            This message should be stored in agent_reply key in the python dictionary.
            """,
            input_variables=["message", "patient_info", "current_appointments"]
        )
    
    def get_patient_info(self):
        try:
            return f"Name: {self.patient.first_name} {self.patient.last_name}, DOB: {self.patient.dob}, Doctor: {self.patient.doctor_name}"
        except Patient.DoesNotExist:
            return "Patient not found"
        
    def get_appointment_info(self):
        appointments = [self.patient.last_appointment, self.patient.next_appointment]
        return ", ".join([f"{apt.strftime('%Y-%m-%d %H:%M')}" for apt in appointments])

    # def extracted_context(self, user_message):
    #     entity_extractor1 = EntityExtractor()
    #     entities = entity_extractor1.extract_entities(user_message.content)
    #     return str(entities)
    
    def invoke(self, input_data):
        prompt = self.prompt_template.format(
            message=input_data['messages'][-1],
            patient_info=self.get_patient_info(),
            current_appointments=self.get_appointment_info()
        )
        llm_response = self.llm.invoke(prompt)
        llm_response.name = "AppointmentManager"
        return {"agent_history": [llm_response]}
