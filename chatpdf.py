"""
Project Name: chatpdf_api_interface
Description: API Interface for ChatPDF
Author: Juan Terven
Date: December 2023
License: MIT
Contact: jrterven@hotmail.com
"""
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import threading
from tkinter import ttk
from tkinter import font
from utils import get_api_key, upload_chatpdf_file, query_chatpdf


from pathlib import Path

def get_output_filename(source_file_path, prepend_text):
    """
    Generate a unique output filename based on the given source file path and a text to prepend.

    This function takes a source file path and a string to prepend. It generates a new filename
    by appending the prepend_text to the stem of the source file's name, followed by a number 
    which increments until an available (non-existing) filename is found. The function ensures 
    that the generated filename does not already exist in the directory.

    Parameters:
    source_file_path (Path): The file path of the source file. It's assumed to be a Path object.
    prepend_text (str): The text to prepend to the source file's stem in the generated filename.

    Returns:
    Path: A Path object representing the generated unique output file path.
    """
    # Extract the stem of the source file
    stem = source_file_path.stem

    # Initialize the target file name
    target_file_name = f"{stem}{prepend_text}0.txt"
    target_file_path = Path(target_file_name)

    # Find an available file name with a consecutive number
    counter = 1
    while target_file_path.exists():
        target_file_name = f"{stem}{prepend_text}{counter}.txt"
        target_file_path = Path(target_file_name)
        counter += 1

    return target_file_path


def browse_file():
    """
    Opens a file dialog for the user to select a PDF file.

    This function triggers a file dialog window allowing the user to browse and select a PDF file.
    Once a file is selected, its path is set to a global variable 'file_path_var' for later use.
    If no file is selected, 'file_path_var' remains unchanged.

    Note: This function assumes the existence of a global variable 'file_path_var' to store the 
    selected file path.
    """
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_path_var.set(file_path)


def analyze_pdf(chatpdf_api_key):
    """
    Initiates the analysis of a selected PDF file using a separate thread.

    This function disables the analyze button, retrieves the path of the selected PDF from a 
    global variable 'file_path_var', and then starts a new thread to process the PDF analysis. 
    If no file is selected, it updates the status text to prompt the user to select a file and 
    re-enables the analyze button.

    Parameters:
    chatpdf_api_key (str): The API key required for the PDF analysis service.

    Note: This function assumes the existence of certain global elements and functions such as 
    'file_path_var', 'analyze_button', 'root', and 'update_status_text', and it requires a 
    separate function 'analyze_pdf_thread' for the actual analysis process.
    """
    analyze_button.config(state="disabled")
    file_path = file_path_var.get()

    if not file_path:
        root.after(0, update_status_text, f"Please select a PDF to analyze\n")
        analyze_button.config(state="normal")
        return

    threading.Thread(target=analyze_pdf_thread, args=(file_path, chatpdf_api_key)).start()



def analyze_pdf_thread(file_path, chatpdf_api_key):
    """
    A thread function for analyzing a PDF file using the ChatPDF service.

    This function is designed to be run in a separate thread. It uploads the specified PDF file 
    to the ChatPDF service using a provided API key, and updates the global variable 
    'paper_source_id' with the ID returned from the upload. It updates the application's status 
    text at various stages of the process, including when the file is being uploaded and when it 
    is ready for interaction.

    Parameters:
    file_path (str): The path of the PDF file to be analyzed.
    chatpdf_api_key (str): The API key for accessing the ChatPDF service.

    Note: This function assumes the existence of global elements and functions such as 'root', 
    'update_status_text', and 'upload_chatpdf_file'. It also modifies the global variable 
    'paper_source_id'.
    """
    global paper_source_id

    # get path from command line argument
    pdf_file_path = file_path

    # Upload file to ChatPDF
    root.after(0, update_status_text, f"Uploading document {pdf_file_path}...\n")
    paper_source_id = upload_chatpdf_file(pdf_file_path, chatpdf_api_key=chatpdf_api_key)

    root.after(0, update_status_text, f"READY TO CHAT!\n")


def update_status_text(text, color="red"):
    """
    Updates a text widget with given text and color.

    This function inserts the provided text into a text widget with the specified color. 
    It then scrolls the text widget to show the most recent entry. This is typically used 
    for updating the status of an operation in the GUI.

    Parameters:
    text (str): The text to be inserted into the text widget.
    color (str, optional): The color to be used for the inserted text. Defaults to "red".

    Note: This function assumes the existence of a function 'insert_colored_text' and a global 
    text widget object 'status_text_obj'.
    """
    insert_colored_text(status_text_obj, text, color)
    status_text_obj.see(END)  # Scroll to the end of the text



def handle_return(event, chatpdf_api_key, source_id):
    """
    Handles the Return key event in a text widget, allowing for newline insertion or sending a chat prompt.

    This function is bound to the Return key event in a text widget. If the Shift key is also pressed,
    it inserts a newline at the cursor position in 'prompt_text_obj'. If Shift is not pressed, it 
    triggers the function 'send_chat_prompt' to process and send the text as a chat prompt.

    Parameters:
    event (Event): The event object containing information about the key press.
    chatpdf_api_key (str): The API key for accessing the ChatPDF service.
    source_id (str): The source ID for the ChatPDF service.

    Note: This function assumes the existence of a text widget 'prompt_text_obj' and a function 
    'send_chat_prompt'. It also uses the event's state to check if the Shift key is pressed.
    
    Returns:
    str: Returns "break" to stop the event from propagating further.
    """

    # 0x0001 is the shift key state. You can use 'event.state == 1' as well.
    if event.state & 0x0001:
        # Insert a new line character at the cursor position
        prompt_text_obj.insert("insert", '\n')
    else:
        # If shift is not pressed, call your send_chat_prompt function
        send_chat_prompt(chatpdf_api_key, source_id)
    # Stop the event from propagating further
    return "break"


def send_chat_prompt(chatpdf_api_key, source_id):
    """
    Processes and sends the current text in 'prompt_text_obj' as a chat prompt.

    This function retrieves the text from 'prompt_text_obj', formats it, and starts a new thread 
    using 'send_chat_prompt_thread' to send this prompt to the ChatPDF service. It updates the 
    'response_text_obj' with the prompt and a processing message. After sending, it clears the prompt 
    text widget.

    Parameters:
    chatpdf_api_key (str): The API key for the ChatPDF service.
    source_id (str): The source ID for the ChatPDF service.

    Note: This function assumes the existence of text widgets 'prompt_text_obj' and 'response_text_obj',
    a function 'insert_colored_text', and a separate thread function 'send_chat_prompt_thread'.
    """

    prompt = prompt_text_obj.get("1.0", "end")

    # remove last line break
    prompt = prompt[:-1] if len(prompt) > 0 and prompt[-1] == "\n" else ""

    # Insert prompt and processing message in response_text_obj
    insert_colored_text(response_text_obj, f"{prompt}\n", "black")
    insert_colored_text(response_text_obj, "Processing prompt ...\n", "blue")

    # Start a new thread to process the prompt
    threading.Thread(target=send_chat_prompt_thread, args=(chatpdf_api_key, source_id, prompt,)).start()

    # Clear the prompt text widget
    prompt_text_obj.delete("1.0", END)
    prompt_text_obj.mark_set("insert", "1.0")



def send_chat_prompt_thread(chatpdf_api_key, source_id, prompt):
    """
    A thread function that sends a chat prompt to the ChatPDF service and handles the response.

    This function is designed to be run in a separate thread. It sends the provided chat prompt to
    the ChatPDF service using the given API key and source ID, retrieves the response, and then
    updates 'response_text_obj' with this response. It also removes the temporary 'processing prompt'
    message from 'response_text_obj'.

    Parameters:
    chatpdf_api_key (str): The API key for accessing the ChatPDF service.
    source_id (str): The source ID for the ChatPDF service.
    prompt (str): The chat prompt to be sent for processing.

    Note: This function assumes the existence of global elements and functions like 'response_text_obj',
    'query_chatpdf', and 'insert_colored_text'.
    """

    response = query_chatpdf(chatpdf_api_key, source_id, prompt)

    # Remove the "processing prompt ..." text
    response_text_obj.delete('end - 2 lines linestart', 'end - 1 line')

    # Insert the response
    insert_colored_text(response_text_obj, f"{response}\n\n", "blue")

    
def insert_colored_text(text_widget, text, color):
    """
    Inserts colored text into a given text widget.

    This function adds the given text to the specified text widget with the specified color. It creates
    a unique tag for each color and applies this tag to the inserted text to set its foreground color.

    Parameters:
    text_widget (Text): The text widget where the text is to be inserted.
    text (str): The text to be inserted.
    color (str): The color to be applied to the text.

    Note: The function uses tkinter's text widget and tag system for text colorization.
    """

    tag_name = f"tag_{color}"
    text_widget.tag_configure(tag_name, foreground=color)
    text_widget.insert(END, text, (tag_name,))


def clear_data():
    """
    Clears all data from the response and status text widgets and re-enables the analyze button.

    This function is used to reset the interface by clearing all text from 'response_text_obj' and
    'status_text_obj', and setting the state of 'analyze_button' to normal, enabling it for further
    use.

    Note: This function assumes the existence of global elements 'response_text_obj', 'status_text_obj',
    and 'analyze_button'.
    """

    response_text_obj.delete('1.0', END)
    status_text_obj.delete('1.0', END)
    analyze_button.config(state="normal")

        

def export_chat():
    """
    Exports the contents of the chat (response text) to a user-specified text file.

    This function prompts the user to choose a file location and name for saving the chat 
    contents. It uses the current file path from 'file_path_var' to suggest a default name 
    and directory for the exported file. If the user selects a location and confirms, the 
    chat content from 'response_text_obj' is saved to the specified file.

    Note: This function assumes the existence of global elements and functions like 
    'file_path_var', 'response_text_obj', 'get_output_filename', and 'update_status_text'.
    It also uses tkinter's file dialog for saving files.
    """

    default_name = get_output_filename(Path(file_path_var.get()), "_chat")
    msg = "Chat exported!"
    exported_text = response_text_obj.get("1.0", "end")

    default_dir = Path(file_path_var.get()).parent
    filetypes = [('Text files', '*.txt'), ('All files', '*.*')]
    filepath = filedialog.asksaveasfilename(initialdir=default_dir,
                                            initialfile=default_name,
                                            defaultextension=".txt",
                                            filetypes=filetypes)
    if filepath:
        print(filepath)
        target_file_path = Path(filepath)
        print(f"Saving to {target_file_path}")
        target_file_path.write_text(exported_text)

        root.after(0, update_status_text, f"{msg}\n")



if __name__ == "__main__":
    root = Tk()
    root.title("ChatPDF")

    # Get API key
    chatpdf_api_key = get_api_key(var_name='CHAT_PDF_KEY')
    paper_source_id = None

    # Calculate the proportions of the main window
    window_width = 900
    padx = 5
    width_widget = 100
    row = 0

    # Set root window size
    root.geometry(f"{window_width}x800")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a custom font object
    custom_font = font.Font(family="Helvetica", size=12)

    file_path_var = StringVar(root)

    # Frame for file and model characteristics 3 columns
    file_browse_frame = Frame(root)
    file_browse_frame.grid(row=row, column=0, columnspan=4, pady=5, sticky=W)
    row += 1

    file_label = Label(file_browse_frame, text="PDF file:", font=custom_font)
    file_label.grid(row=0, column=1, padx=5, sticky=W)

    file_entry = Entry(file_browse_frame, textvariable=file_path_var,
                       width=50, font=custom_font)
    file_entry.grid(row=0, column=2, padx=5, sticky=W)

    browse_button = Button(file_browse_frame, text="Browse",
                           command=browse_file, font=custom_font)
    browse_button.grid(row=0, column=3, padx=5, sticky=W)

    # --------------------------------------------
    start_clear_frame = Frame(root)
    start_clear_frame.grid(row=row, column=0, columnspan=6, pady=5, sticky=W)
    row += 1

    # Analyze button
    analyze_button = Button(start_clear_frame, text="Analyze PDF",
                            command=lambda:  analyze_pdf(chatpdf_api_key),
                            font=custom_font)
    analyze_button.grid(row=0, column=1, padx=5, sticky=W)

    # Clear summaries button
    clear_summary_button = Button(start_clear_frame, text="Clear All",
                                  command=clear_data,
                                  font=custom_font)
    clear_summary_button.grid(row=0, column=2, pady=5, sticky=W)

    # --------------------------------------------
    status_label = Label(root, text="Status:", font=custom_font)
    status_label.grid(row=row, column=0, pady=5, sticky=W)
    row += 1

    # Status text
    status_text_obj = Text(root, wrap=WORD, height=4, width=width_widget, font=custom_font)
    status_text_obj.grid(row=row, column=0, padx=5, pady=5, sticky=W)

    # Status scrollbar
    status_scrollbar = Scrollbar(root, command=status_text_obj.yview)
    status_scrollbar.grid(row=row, column=1, sticky=N+S)
    status_text_obj.config(yscrollcommand=status_scrollbar.set)
    row += 1

    # Add the chat functionality to the right 
    prompt_label = Label(root, text="Prompt:", font=custom_font)
    prompt_label.grid(row=row, column=0, pady=5, sticky=W)
    row += 1

    # Text prompt
    prompt_text_obj = Text(root, wrap=WORD, height=4, width=width_widget, font=custom_font)
    prompt_text_obj.bind("<Return>", lambda event, arg=chatpdf_api_key: handle_return(event, arg, paper_source_id))
    prompt_text_obj.grid(row=row, column=0, padx=5, pady=5, sticky=W)

    # Prompt scrollbar
    prompt_scrollbar = Scrollbar(root, command=prompt_text_obj.yview)
    prompt_scrollbar.grid(row=row, column=1, sticky=N+S)
    prompt_text_obj.config(yscrollcommand=prompt_scrollbar.set)
    row += 1

    # Send prompt button
    send_button = Button(root, text="Send Prompt",
                         command=lambda: send_chat_prompt(chatpdf_api_key, paper_source_id),
                         font=custom_font)
    send_button.grid(row=row, column=0, pady=5, sticky=W)
    row += 1

    # Conversation label
    response_label = Label(root, text="Conversation:", font=custom_font)
    response_label.grid(row=row, column=0, pady=5, sticky=W)
    row += 1

    # Conversation text
    response_text_obj = Text(root, wrap=WORD, height=15, width=width_widget, font=custom_font)
    response_text_obj.grid(row=row, column=0, padx=5, pady=5, sticky=W)
    text_scrollbar = Scrollbar(root, command=response_text_obj.yview)
    text_scrollbar.grid(row=row, column=1, sticky=N+S)
    row += 1

    # Export coversation button
    export_chat_button = Button(root, text="Export Chat",
                                command=export_chat,
                         font=custom_font)
    export_chat_button.grid(row=row, column=0, pady=5, sticky=W)
    export_chat_button.config(state="normal")
    row += 1

    root.mainloop()



