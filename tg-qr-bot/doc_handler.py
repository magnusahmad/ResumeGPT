import mammoth
# import docx
from steamship import Steamship
from Markdown2docx import Markdown2docx
import argparse

def parse_document(downloaded_file):
    with open("input.docx", 'wb') as f:
            f.write(downloaded_file)
        
        # Convert docx to HTML
    with open("input.docx", "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
    html_text = result.value
    #return html_text
    # Create new Word docx from Markdown
    # doc = docx.Document()
    # doc.add_paragraph(html_text)
    # print('hi')
    html_text.save("input.html")
    return 'done'

def parse_document_for_bot(input_md):
    # Load the package instance stub.
    pkg = Steamship.use(
        "resume-helper-bot",
        instance_handle="resume-helper-bot-42f-102r",
        workspace_handle="resume-helper-bot-42f-102r-3q2ldw",
        api_key="371135FF-DFF7-4666-B782-36376DFBDECA"
    )
    
    with open(input_md, "rb") as md_prompt:
        string_prompt = str(md_prompt.read())
        # Invoke the method
    resp = pkg.invoke(
        "prompt",
        prompt=string_prompt,
        #context_id=VALUE,
        #kwargs=VALUE
    )
    
    md_text = resp[0].get("text")
    with open('chat.md','w') as f:
        f.write(md_text)

    print('Markdown file written!')

# def send_doc_to_bot(html_file):
#     open(html_file, "a")

         
#     pass to chain as a prompt
#     Capture response as a variable
#     pipe response into a docx
#     save docx
#     '''
#     return