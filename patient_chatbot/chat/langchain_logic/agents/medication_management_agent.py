
from langchain_core.prompts import PromptTemplate
from ..entity_extractor import EntityExtractor
from ...models import Patient

class MedicationManagementAgent:
    def __init__(self, llm):
        self.patient = Patient.objects.first()
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""You are a medication management assistant.
            Please answer questions regarding medication regimens.
            This is the message from the user: {message}
            This is the personal information about the patient: {patient_info}
            This is the medical information about the patient: {patient_medical_info}
            These are some extracted terms from user message that you can use for reference: {context}""",
            input_variables=["message", "patient_info", "patient_medical_info", "context"]
        )
    
    def get_patient_info(self):
        try:
            return f"Name: {self.patient.first_name} {self.patient.last_name}, DOB: {self.patient.dob}, Doctor: {self.patient.doctor_name}"
        except Patient.DoesNotExist:
            return "Patient not found"
    
    def get_patient_medical_info(self):
        try:
            return f"Medical Condition: {self.patient.medical_condition}, Medical Regimen: {self.patient.medication_regimen}"
        except Patient.DoesNotExist:
            return "Patient not found"
        
    def extracted_context(self, user_message):
        entity_extractor1 = EntityExtractor()
        entities = entity_extractor1.extract_entities(user_message.content)
        return str(entities)
    
    def invoke(self, input_data):
        prompt = self.prompt_template.format(message=input_data['messages'][-1], patient_info=self.get_patient_info(), patient_medical_info = self.get_patient_medical_info(), context=self.extracted_context(input_data['messages'][-1]))
        llm_response = self.llm.invoke(prompt)
        llm_response.name = "MedicationManager"
        return {"agent_history": [llm_response]}
