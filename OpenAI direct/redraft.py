import requests
from bs4 import BeautifulSoup 
import openai

first_draft = """Dear Hiring Manager,

I am writing in response to your job posting for a Senior Product Manager (Runtime) at Docker. I am confident my professional experience, technical skills, and international background make me an ideal fit for this role.

I have professional experience across five countries in sales, UX research, product-market-fit, strategic roadmaps, data analytics & modelling, and self-taught Cloud (Certified Solutions Architect) and web development. Most recently, I served as a Senior Product Manager at Affinidi in Berlin, where I was responsible for end-to-end delivery of multiple MVPs for privacy-preserving decentralized identity products used by over one million customers around the world. Additionally, I was the product owner for a developer-facing suite of tools to build decentralized, privacy-preserving applications leveraging blockchain-agnostic verification mechanisms.

Previously, I was a Product Manager in the Supply Chain Analytics team at Amazon in London, where I led the UK inventory placement strategy and developed an automation roadmap for a new EU marketplace. I also built predictive analytics and interactive dashboards to surface Supply Chain opportunities, such as identifying and prioritizing shipment of 80,000 delayed Christmas packages in 2020. I have also run EU-wide A/B tests impacting 8-digit weekly shipment units, including an initiative to improve delivery speed of apparel lines by 30%, doubling coverage of apparel products in warehouses in five EU marketplaces.

My technical skills include a Certified AWS Solutions Architect, Advanced SQL, Excel, and Proficient Python, JS, and full stack web development. I have also developed an OSINT tool to conduct twitter user research, which is available on my GitHub page.

I am passionate about development, innovation, and problem-solving, and I am excited about the opportunity to contribute to Docker's success as a Senior Product Manager. I would be grateful for the chance to discuss this role in more detail and thank you for your time and consideration. 

Sincerely,

Magnus Ahmad"""

openai.api_key = "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" 

def get_job_ad_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_text = soup.get_text()
    return job_text

def generate_cover_letter(first_draft, job_text):
  #cv = open("pandoc_output.md").read()
  #input("Please provide the text of your CV: ")

  prompt = f"""You are an advanced AI tool for helping users write convincing job application cover letters. 
You have just written a first draft as follows: {first_draft}. Your task is to improve the draft by fine tuning it to the job description.
The job description is {job_text}: 
Make sure that the cover letter sounds like it was written specifically for this job, while keeping it specific to the user's experience.

When you respond, only respond with the cover letter body.
NEVER write conversational things, like "Here is a cover letter for the job ad you sent"
DO NOT write any formalities such as the applicant or company's address or contact details.
Now, take a deep breath, and redraft the cover letter.
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
  
  cover_letter = generate_cover_letter(first_draft, job_ad)

  print(cover_letter)