import re
import docx
from PyPDF2 import PdfReader
from rapidfuzz import fuzz

#MASTER SKILL LIST

MASTER_SKILLS={
    "programming":["Python","Java","JavaScript","PLSQL","C++","Ruby"],
    "frameworks" :["Django","SpringBoot","Flask","Angular","React","Node.js","Spring","Maven","Ruby on Rails"],
    "cloud":["AWS","Azure","GCP"],
    "database":["PostgreSQL","MongoDB","DataBricks","Snowflake","Oracle","MySQL"],
    "build":["Docker","Kubernetes","Heroku","Git","Grunt"],
    "others":["Teaching","Nursing","Robotics"]
}

def extract_text_from_pdf(file_path:str):
    """Extract raw text from PDF resume"""
    reader = PdfReader(file_path)
    text =""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def extract_text_from_doc(file_path:str):
    """EXtract raw text from DOC resume"""
    print("in extract tex function")
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_phone(text:str):
    """Extract phone from raw text"""
    #match = re.search(r"\+?\d[\d\s-]{10,}\d",text)
    phone_pattern = re.compile(r"(\+?\d{1,3}[\s-]?)?(\(?\d{2,4}\)?[\s-]?)?\d{3,5}[\s-]?\d{4,}")
    match = phone_pattern.search(text)
    return match.group(0) if match else None

def extract_email(text:str):
    """Extract email for raw text"""
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+",text)
    return match.group(0) if match else None

def extract_skills(text:str, threshold:int =85):
    """Detect skills from master list and extract"""
    found_skills =[]
    text_lower = text.lower()
    for category,skills in MASTER_SKILLS.items():
        for skill in skills: #this matches extact word Angular != Angularjs
            if skill.lower() in text_lower: 
                found_skills.append(skill)
            else:
                #fuzzy match
                score = fuzz.partial_ratio(skill.lower(),text_lower)
                if score >= threshold:
                    found_skills.append(skill)
                 
    return list(set(found_skills)) #removing duplicates by doing set



