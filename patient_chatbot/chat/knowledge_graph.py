from neo4j import GraphDatabase
import json

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_patient_info(self, patient_name, medical_condition, medication, dosage, frequency):

        with self.driver.session() as session:
            if medical_condition:
                session.run("MERGE (p:Patient {name: $patient_name}) SET p.medical_condition = $medical_condition", 
                            patient_name=patient_name, medical_condition=medical_condition)
            
            if medication:
                session.run("""
                    MERGE (p:Patient {name: $patient_name})
                    MERGE (m:Medication {name: $medication})
                    MERGE (p)-[:TAKES]->(m)
                    SET m.dosage = $dosage, m.frequency = $frequency
                """, patient_name=patient_name, medication=medication, dosage=dosage, frequency=frequency)

    def add_appointment_change(self, patient_name, requested_change, new_time, doctor_name):
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Patient {name: $patient_name})
                MERGE (d:Doctor {name: $doctor_name})
                MERGE (a:Appointment {status: $requested_change, time: $new_time})
                MERGE (p)-[:HAS_APPOINTMENT]->(a)-[:WITH_DOCTOR]->(d)
            """, patient_name=patient_name, doctor_name=doctor_name, requested_change=requested_change, new_time=new_time)

    def query_patient_data(self, name):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Patient {name: $name})-[:HAS]->(c:Condition), (p)-[:TAKES]->(m:Medication)
                RETURN p.name AS patient, c.name AS condition, m.name AS medication
            """, name=name)
            return result.values()

_knowledge_graph_instance = None
data = json.load(open('chat/llm_config.json'))
def get_knowledge_graph():
    global _knowledge_graph_instance
    if _knowledge_graph_instance is None:
        _knowledge_graph_instance = KnowledgeGraph(
            uri=data['knowledge_graph_cred']['uri'], 
            user=data['knowledge_graph_cred']['user'], 
            password=data['knowledge_graph_cred']['password']
        )
    return _knowledge_graph_instance
