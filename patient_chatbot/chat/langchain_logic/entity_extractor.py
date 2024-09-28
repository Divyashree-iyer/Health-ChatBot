import spacy
from spacy.matcher import Matcher
import re
from langchain.tools import tool

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)

        # Define custom patterns for health-related entities
        self.matcher.add("MEDICATION", [[{"LOWER": {"IN": ["taking", "on", "using", "prescribed"]}}, {"POS": "PROPN"}]])
        self.matcher.add("FREQUENCY", [[{"LIKE_NUM": True}, {"LOWER": {"IN": ["times", "time"]}}, {"LOWER": {"IN": ["a", "per"]}}, {"LOWER": {"IN": ["day", "week", "month"]}}], [{"LOWER": {"IN": ["daily", "weekly"]}}]])
        self.matcher.add("APPOINTMENT", [[{"LOWER": {"IN": ["appointment", "visit", "checkup" "consultation"]}}, {"POS": "ADP"}, {"ENT_TYPE": "DATE"}]])
        self.matcher.add("MEDICAL_CONDITION", [[{"LOWER": {"IN": ["diagnosed", "suffering", "condition"]}}, {"POS": "PROPN"}]])

    @tool
    def extract_entities(self, user_input):
        """ get entities from user input """
        doc = self.nlp(user_input)
        entities = {}

        # Extract named entities recognized by spaCy
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME", "CARDINAL"]:
                entities[ent.label_.lower()] = ent.text

        # Use custom matcher for health-related entities
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            if self.nlp.vocab.strings[match_id] == "MEDICATION":
                entities["medication"] = span[1].text
            elif self.nlp.vocab.strings[match_id] == "FREQUENCY":
                entities["frequency"] = span.text
            elif self.nlp.vocab.strings[match_id] == "APPOINTMENT":
                entities["appointment"] = span.text
            elif self.nlp.vocab.strings[match_id] == "MEDICAL_CONDITION":
                entities["medical_condition"] = span[1].text

        # Extract dosage using regex
        dosage_pattern = r'\d+\s*(?:mg|milligram|gram|g|ml|milligram)'
        dosage_match = re.search(dosage_pattern, user_input, re.IGNORECASE)
        if dosage_match:
            entities["dosage"] = dosage_match.group()

        return entities
    
