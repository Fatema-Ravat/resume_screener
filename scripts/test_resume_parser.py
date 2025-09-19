import os
import sys
from core.utils import resume_parser
from django.conf import settings

print(sys.argv)

if len(sys.argv)<2:
    print("Name of the file to be prased not passed.")
    sys.exit()

file_name =  "resume.pdf" #sys.argv[1]
resume_path = os.path.join(settings.BASE_DIR,"samples",file_name)

print(resume_path)
text = ""
if resume_path.endswith(".pdf"):
    text = resume_parser.extract_text_from_pdf(resume_path)

if resume_path.endswith(".docx"):
    text = resume_parser.extract_text_from_doc(resume_path)

print(text)
print("Extracted email:", resume_parser.extract_email(text))
print("Extracted phone:", resume_parser.extract_phone(text))
print("Extracted skills:", resume_parser.extract_skills(text))
