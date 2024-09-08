import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import markdown
from markdown.extensions import fenced_code, codehilite
from weasyprint import HTML
import os

# Default settings
settings = {
    "font_family": "Arial",
    "font_size": "14px",
    "header_text": "GPT_Saver_V1"
}

def save_pdf(summary, prompt, output, filename, title="GPT Output Report"):
    # Define the output directory
    output_dir = os.path.expanduser("~/Desktop/GPT_Outputs")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%m%d%y")
    file_path = os.path.join(output_dir, f"{filename}_{timestamp}.pdf")

    # Handle empty fields
    if not summary:
        summary = "(No text entered)"
    if not prompt:
        prompt = "(No text entered)"
    if not output:
        output = "(No text entered)"

    # Convert markdown to HTML with fenced code blocks and highlighting
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    summary_html = md.convert(summary)
    prompt_html = md.convert(prompt)
    output_html = md.convert(output)

    # Calculate character length of output
    output_length = len(output)

    # Create full HTML content with improved code rendering
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

    # Render PDF with the HTML content
    HTML(string=html_content).write_pdf(file_path)

    messagebox.showinfo("Success", f"PDF saved to: {file_path}")

def get_filename():
    filename = simpledialog.askstring("Filename", "Enter the base filename:")
    if not filename:
        filename = "output"
    return filename

def on_save():
    summary = summary_text.get("1.0", tk.END).strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    output = output_text.get("1.0", tk.END).strip()

    filename = get_filename()
    save_pdf(summary, prompt, output, filename)
    reset_fields()

def reset_fields():
    """Clears the input fields so the user can start a new entry."""
    summary_text.delete("1.0", tk.END)
    prompt_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

def configure_settings():
    global settings
    font_family = simpledialog.askstring("Font Family", "Enter font family:", initialvalue=settings['font_family'])
    font_size = simpledialog.askstring("Font Size", "Enter font size (e.g., 14px):", initialvalue=settings['font_size'])
    header_text = simpledialog.askstring("Header Text", "Enter header/footer text:", initialvalue=settings['header_text'])

    if font_family:
        settings['font_family'] = font_family
    if font_size:
        settings['font_size'] = font_size
    if header_text:
        settings['header_text'] = header_text

# Create the main application window
app = tk.Tk()
app.title("ChatGPT Output Saver")

# Menu
menu = tk.Menu(app)
app.config(menu=menu)

settings_menu = tk.Menu(menu)
menu.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Configure", command=configure_settings)

# Summary entry
tk.Label(app, text="Enter Summary:").pack(pady=5)
summary_text = tk.Text(app, wrap='word', height=5, width=50)
summary_text.pack(padx=10, pady=5)

# Prompt entry
tk.Label(app, text="Enter Prompt:").pack(pady=5)
prompt_text = tk.Text(app, wrap='word', height=10, width=50)
prompt_text.pack(padx=10, pady=5)

# Output entry
tk.Label(app, text="Enter Output:").pack(pady=5)
output_text = tk.Text(app, wrap='word', height=15, width=50)
output_text.pack(padx=10, pady=5)

# Save button
save_button = tk.Button(app, text="Save as PDF", command=on_save)
save_button.pack(pady=20)

app.mainloop()
