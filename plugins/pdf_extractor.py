import os
from pyrogram import Client, filters
from PyPDF2 import PdfReader

# Configurations
DOWNLOAD_LOCATION = "./DOWNLOADS/"

@Client.on_message(filters.private & filters.document & filters.regex(r".*\.pdf$"))
async def pdf_to_text_handler(client, message):
    # Download the PDF file
    file_path = await client.download_media(
        message.document, file_name=DOWNLOAD_LOCATION + message.document.file_name
    )
    text_file_path = file_path.replace(".pdf", ".txt")

    try:
        # Extract text from PDF
        with open(file_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        # Save text to a file
        with open(text_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        # Send the extracted text file to the user
        await message.reply_document(
            document=text_file_path,
            caption="Here's the extracted text from your PDF.",
        )
    except Exception as e:
        await message.reply_text(f"An error occurred while processing the PDF: {e}")
    finally:
        # Clean up downloaded files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(text_file_path):
            os.remove(text_file_path)
