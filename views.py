from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume
import spacy
from pdfminer.high_level import extract_text

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def index(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.save()
            result = parse_resume(resume_file.resume_file.path)
            resume = Resume.objects.create(
                name=result['name'],
                skills=', '.join(result['skills']),
                experience=result['experience'],
                education=result['education'],
                resume_file=resume_file.resume_file
            )
            return render(request, 'result.html', {'resume': resume})
    else:
        form = ResumeForm()
    return render(request, 'index.html', {'form': form})

def parse_resume(filepath):
    text = extract_text(filepath)
    doc = nlp(text)

    name = extract_name(doc)
    skills = extract_skills(doc)
    experience = extract_experience(doc)
    education = extract_education(doc)

    return {'name': name, 'skills': skills, 'experience': experience, 'education': education}

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"

def extract_skills(doc):
    skills = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            skills.append(token.text)
    return skills

def extract_experience(doc):
    experience = 0.0
    for ent in doc.ents:
        if ent.label_ in ["DATE", "CARDINAL"]:
            try:
                num = float(ent.text)
                if any(word in ent.sent.text.lower() for word in ["year", "years", "month", "months", "experience"]):
                    experience = num
                    break
            except ValueError:
                continue
    return experience

def extract_education(doc):
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    return "Unknown"
