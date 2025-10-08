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
    return match.group(0).strip() if match else None

def extract_email(text:str):
    """Extract email for raw text"""
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+",text)
    return match.group(0).strip() if match else None

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

def extract_name(text:str,email:str,phone:int):
    # Assuming the first line and line above email and phone is name
    lines = text.strip().splitlines()
    for line in lines[:5]:
        if email and email in line:
            continue
        if phone and phone in line:
            continue
        words = line.split()
        if 1 < len(words) <=3 and line.isupper() is False :
            name = line.strip()
            return name
    return None

MONTHS = {
    "Jan":1, "Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
    "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12
}

def parse_date(month,year):
    if year.lower() in ('present','current'):
        return datetime.now()
    return datetime(int(year),MONTHS.get(month,1),1)

def extract_experience(text:str):
    """ Extract experience from work section by keyword search """
    exp_pattern =r"(experience|work history|employment)\s*[:\-]?(.*?)(education|skills|$)"
    match = re.search(exp_pattern, text, flags=re.IGNORECASE |re.DOTALL)
    experience_text =  match.group(0).strip() if match else None # experience details text
    exp_years = _extract_exp_years(experience_text)
    return exp_years

def _extract_exp_years(text:str):
    date_range_regex = r'(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*)?(\d{4})\s*(?:-|to)\s*(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*)?(\d{4}|present|current)'
    matches = re.findall(date_range_regex,text, flags=re.IGNORECASE)
    total_months = 0

    for start_m, start_y, end_m , end_y in matches:
        try:
            start = parse_date(start_m,start_y)
            end = parse_date(end_m,end_y)
            diff = (end.year - start.year) *12 + (end.month - start.month)
            if diff >0:
                total_months += diff
        except Exception:
            continue

    return round(total_months/12, 1) if total_months else 0.0


def extract_education(text:str):
    """ Extract education using keyword search """

    edu_pattern = r"(education|qualification|university|college)\s*[:\-]?(.*?)(experience|skills|achievements|$)"
    match = re.search(edu_pattern, text, flags=re.IGNORECASE |re.DOTALL)
    education_text =  match.group(0).strip() if match else None
    education = _extract_highest_education(education_text) if education_text else  None

def _extract_highest_education(text:str):

    ed_levels=[
        "phd":["phd","doctorate","ph.d"],
        "masters": ["masters","m.sc","msc","m.tech","m.e","mca","postgraduate"],
        "bachelors": ["bachelors","b.sc","b.e","b.tech","ba","bca","undergraduate"],
        "diploma" : ["diploma"],
        "school" :["high school","12th","10th","secondary","senior secondary"]
    ]

    for level, keywords in ed_levels.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw)+ r"\b", text):
                return level.capitalize()
    return None
