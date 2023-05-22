import os
from io import StringIO
import pdfminer
from pdfminer.high_level import extract_text_to_fp
import io
import openai
import werkzeug
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        name = request.form.get('name', '')
        job_info = request.form.get('jobInfo', '')
        notes = request.form.get('notes', '')

        # Handle file upload for the resume
        resume_file = request.files.get('resume', None)
        resume = extract_text_from_pdf(resume_file)
        


        prompt=generate_prompt(name, resume, job_info, notes)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates cover letters."},
                    {"role": "user", "content": prompt}
                ]
        )
        content = response['choices'][0]['message']['content']
        
        #return redirect(url_for("index", result=response.choices[0].text))
        return redirect(url_for("index", result=content))

    result = request.args.get("result")
    return render_template("mainPage.html", result=result)




def generate_prompt(name, resume, jobInfo, notes):
    return f"Generate a cover letter for {name} applying for a job using the following resume and job description.\nResume: {resume}\nJob Description: {jobInfo} \n Here are some additional notes: {notes}"




def extract_text_from_pdf(file_object):
    output_string = io.StringIO()
    extract_text_to_fp(file_object, output_string)
    return output_string.getvalue()