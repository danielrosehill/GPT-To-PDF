import streamlit as st
from datetime import datetime
import markdown
from markdown.extensions import fenced_code, codehilite
from weasyprint import HTML
from io import BytesIO
import time

st.image("https://res.cloudinary.com/drrvnflqy/image/upload/v1725822185/GPT_2_PDF_1_gczb6o.png", use_column_width=True)
 
settings = {
    "font_family": "Arial",
    "font_size": "14px",
    "header_text": "GPT_Saver_V1"
}

def generate_pdf(summary, prompt, output, title="GPT Output Report"):
 
    if not summary:
        summary = "(No text entered)"
    if not prompt:
        prompt = "(No text entered)"
    if not output:
        output = "(No text entered)"

 
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    summary_html = md.convert(summary)
    prompt_html = md.convert(prompt)
    output_html = md.convert(output)

   
    output_length = len(output)

    
    html_content = f"""
    <html>
    <head>
    <style>
    body {{ font-family: {settings['font_family']}; font-size: {settings['font_size']}; line-height: 1.5; }}
    h1 {{ font-size: 24px; }}
    h2 {{ font-size: 20px; }}
    p {{ margin: 10px 0; }}
    pre, code {{ font-family: 'Courier New', Courier, monospace; background-color: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap; }}
    pre {{ overflow: auto; border: 1px solid #ccc; }}
    code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
    footer {{ text-align: center; font-size: 12px; margin-top: 20px; }}
    .page-number:after {{ content: counter(page); }}
    </style>
    </head>
    <body>
     
    <h1>{title}</h1>
    <h2>Summary:</h2>
    {summary_html}
    <hr>
    <h2>Prompt:</h2>
    {prompt_html}
    <hr>
    <h2>Output:</h2>
    {output_html}
    <footer>
        GPT_Saver_V1 | Character length: {output_length} | Page <span class="page-number"></span>
    </footer>
    </body>
    </html>
    """

 
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)

    return pdf_file

def main():
    st.title("ChatGPT Output Saver")
    
 
    st.markdown("""
    **Welcome to the ChatGPT Output Saver!**
    
    A simple utility for capturing GPT prompts, outputs, and rendering them both into a formatted PDF document. The output field expects markdown.
    
    By [Daniel Rosehill](https://github.com/danielrosehill/) & GPT-4
    """)

 
    summary = st.text_area("Enter Summary")
    prompt = st.text_area("Enter Prompt")
    output = st.text_area("Enter Output")

    filename = st.text_input("Enter the base filename", value="output")
 
    if "button_color" not in st.session_state:
        st.session_state.button_color = "white"

    generate_button = st.button("Generate PDF", key="generate", on_click=lambda: st.session_state.update({"button_color": "green"}))

    if generate_button:
        pdf_file = generate_pdf(summary, prompt, output)
        st.success("PDF generated successfully!")
        
 
        st.image("https://res.cloudinary.com/drrvnflqy/image/upload/v1725821509/scrolldown_dus4th.png", use_column_width=True)
        time.sleep(1)
        st.empty()   

       
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=f"{filename}_{datetime.now().strftime('%m%d%y')}.pdf",
            mime="application/pdf",
            on_click=lambda: st.session_state.update({"button_color": "white"})
        )

 
    st.markdown(
        f"""
        <style>
        div.stButton > button:first-child {{
            background-color: {st.session_state.button_color};
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
