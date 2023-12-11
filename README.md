# chatpdf_api_interface

## Description
The `chatpdf_api_interface` is a Python-based graphical user interface application designed to interact with ChatPDF, an API for analyzing and interacting with PDF documents. Developed by Juan Terven, this tool offers a convenient way to upload PDF files, analyze them using ChatPDF, and engage in a chat-based interaction to extract and understand content from the PDFs.

## Features
- Browse and select PDF files for analysis.
- Upload PDFs to ChatPDF using an API key.
- Chat-based interaction for analyzing and querying content from PDF documents.
- Display of conversation history.
- Export functionality for chat conversations.
- Clear data and reset functionality.

## Installation
To run `chatpdf_api_interface`, you need Python installed on your system. Clone this repository to your local machine and install the required dependencies:

```bash
git clone [repository URL]
cd chatpdf_api_interface
pip install -r requirements.txt
```

## Usage
To start the application, run:

```bash
python chatpdf.py
```

1. **Browse and Select PDF**: Use the 'Browse' button to select a PDF file for analysis.
2. **Analyze PDF**: Click 'Analyze PDF' to upload the file to ChatPDF and begin analysis.
3. **Chat Interaction**: Enter prompts in the provided text field and send them to interact with the analyzed PDF.
4. **Export Chat**: You can export the chat history using the 'Export Chat' button.
5. **Clear All**: This button clears all the data and resets the interface.

## Configuration
You need to set an environment variable `CHAT_PDF_KEY` with your ChatPDF API key. This key is necessary for the application to interact with the ChatPDF service.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any queries or contributions, feel free to contact Juan Terven at jrterven@hotmail.com.

## Acknowledgments
Special thanks to all contributors and users of the `chatpdf_api_interface`. Your feedback and contributions are highly appreciated.

---

Feel free to modify this template according to your project's specifics and requirements. Remember to add any additional sections as needed, such as 'Contributing', 'Credits', or 'Changelog'.