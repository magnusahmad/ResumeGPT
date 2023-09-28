import requests
from bs4 import BeautifulSoup 
import openai


openai.api_key = "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" 

def get_job_ad_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_text = soup.get_text()
    return job_text

def generate_cover_letter(job_text, cv):
  
  prompt = f"""During this chat, imagine you are an advanced AI tool for helping users write job application cover letters. 
The job description is {job_text}. The user's CV is {cv}. Write a convincing cover letter using the job description and CV.
Your cover letter should do the following:
- Be concise: keep it to less than a page
- Use relevant keyword and requirements from the job description
- Be specific: Use 2-3 examples from the CV to qualify your assertions. Make sure not to simply repeat what's in the CV.

Each paragraph must address one of the following:  motivation for joining the company, motivation for the role, or relevant experience/skills making the candidate a good fit for the role.

When you respond, only respond with the cover letter body.
NEVER write conversational things, like "Here is a cover letter for the job ad you sent"
DO NOT write any formalities such as the applicant or company's address or contact details.
"""
  
  response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        temperature=0.7,
        max_tokens=3000
    )
  return response.choices[0].text
  
if __name__ == "__main__":

  url = "https://jobs.ashbyhq.com/docker/a90fdb65-3f79-4b94-ad82-4def8e7f4f55"
  job_ad = get_job_ad_text(url)
  
  cv = open("pandoc_output.md").read()

  cover_letter = generate_cover_letter(job_ad, cv)

  print(cover_letter)