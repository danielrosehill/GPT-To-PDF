import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter.font import Font
from datetime import datetime
import markdown
from markdown.extensions import fenced_code, codehilite
from weasyprint import HTML
import os
from PIL import Image, ImageTk  # Use Pillow for loading images

# Default settings
settings = {
    "font_family": "Arial",
    "font_size": "14px",
    "header_text": "By: Daniel Rosehill & GPT-4",
    "output_dir": os.path.expanduser("~/Desktop")  # Default output directory
}

def save_pdf(summary, prompt, output, filename, title="GPT Output Report"):
    output_dir = settings["output_dir"]
    
    timestamp = datetime.now().strftime("%m%d%y")
    file_path = os.path.join(output_dir, f"{filename}_{timestamp}.pdf")

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
        <a href="https://github.com/danielrosehill" target="_blank">By: Daniel Rosehill & GPT-4</a> | Character length: {output_length} | Page <span class="page-number"></span>
    </footer>
    </body>
    </html>
    """

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

def select_output_directory():
    output_dir = filedialog.askdirectory(title="Select Output Directory", initialdir=settings["output_dir"])
    if output_dir:
        settings["output_dir"] = output_dir
        output_path_entry.config(state='normal')
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, output_dir)
        output_path_entry.config(state='readonly')

# Create the main application window
app = tk.Tk()
app.title("GPT Output Saving Utility")
app.geometry("550x850")  # Adjusted size to ensure button visibility and space for image

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the image
image_path = os.path.join(script_dir, "appbanner.png")

# Load and resize the image to 400px wide while maintaining the aspect ratio
image = Image.open(image_path)
image.thumbnail((400, 400))  # Resize the image to 400px width while keeping the aspect ratio
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(app, image=photo)
image_label.pack(pady=10)

# Output directory selection
output_dir_frame = tk.Frame(app)
output_dir_frame.pack(fill='x', padx=10, pady=5)
tk.Label(output_dir_frame, text="Output Directory:", font=("Helvetica", 12, "bold")).pack(anchor='w')
output_path_entry = tk.Entry(output_dir_frame, width=50)
output_path_entry.insert(0, settings["output_dir"])
output_path_entry.config(state='readonly')
output_path_entry.pack(side="left", fill='x', expand=True)
output_dir_button = tk.Button(output_dir_frame, text="Browse", command=select_output_directory)
output_dir_button.pack(side="right")

# Custom font for labels
label_font = Font(family="Helvetica", size=12, weight="bold")

# Menu
menu = tk.Menu(app)
app.config(menu=menu)

settings_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Configure", command=configure_settings)

# Program description and usage instructions
tk.Label(app, text="This program was generated using ChatGPT!", font=label_font).pack(pady=10)
tk.Label(app, text="Usage: Fill out the fields, hit the button", font=label_font).pack(pady=5)

# Save button (moved above the form fields)
button_frame = tk.Frame(app)
button_frame.pack(fill='x', pady=10)
save_button = tk.Button(button_frame, text="Save as PDF", command=on_save, bg="#4CAF50", fg="white", padx=10, pady=5)
save_button.pack(anchor='center')

# Summary entry
summary_frame = tk.Frame(app)
summary_frame.pack(fill='x', padx=10, pady=5)
tk.Label(summary_frame, text="Enter Summary:", font=label_font).pack(anchor='w')
summary_text = tk.Text(summary_frame, wrap='word', height=5, width=50)
summary_text.pack(fill='x')

# Prompt entry
prompt_frame = tk.Frame(app)
prompt_frame.pack(fill='x', padx=10, pady=5)
tk.Label(prompt_frame, text="Enter Prompt:", font=label_font).pack(anchor='w')
prompt_text = tk.Text(prompt_frame, wrap='word', height=10, width=50)
prompt_text.pack(fill='x')

# Output entry
output_frame = tk.Frame(app)
output_frame.pack(fill='x', padx=10, pady=5)
tk.Label(output_frame, text="Enter Output:", font=label_font).pack(anchor='w')
output_text = tk.Text(output_frame, wrap='word', height=15, width=50)
output_text.pack(fill='x')

app.mainloop()
