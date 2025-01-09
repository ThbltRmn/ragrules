import pymupdf
import io
import base64


def highlight_text_in_pdf_and_extract_pages_stream(pdf_data, search_text):
    """
    Highlight all occurrences of a search text in a PDF and return the pages where the text is found.

    Args:
        pdf_data (bytes): PDF file data.
        search_text (str): Text to highlight.

    Returns:
        tuple: (bytes, list): The modified PDF as byte data and the list of page numbers where the text is found.
    """
    pdf_document = pymupdf.open(stream=pdf_data, filetype="pdf")
    pages_with_text = []

    for page_number, page in enumerate(pdf_document, start=1):
        # Search for occurrences of the search text
        text_instances = page.search_for(search_text)

        if text_instances:  # If text is found
            pages_with_text.append(page_number)

            # Highlight each instance
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))
                highlight.update()

    # Save the highlighted PDF to a buffer
    pdf_buffer = io.BytesIO()
    pdf_document.save(pdf_buffer)
    pdf_document.close()
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue(), pages_with_text

def highlight_text_in_pdf_and_extract_pages(filename, search_text):
    """
    Highlight all occurrences of a search text in a PDF and return the pages where the text is found.

    Args:
        filename (str): PDF file link.
        search_text (str): Text to highlight.

    Returns:
        tuple: (bytes, list): The modified PDF as byte data and the list of page numbers where the text is found.
    """
    pdf_document = pymupdf.open(filename=filename, filetype="pdf")
    pages_with_text = []

    for page_number, page in enumerate(pdf_document, start=1):
        # Search for occurrences of the search text
        text_instances = page.search_for(search_text)

        if text_instances:  # If text is found
            pages_with_text.append(page_number)

            # Highlight each instance
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))
                highlight.update()

    # Save the highlighted PDF to a buffer
    pdf_buffer = io.BytesIO()
    pdf_document.save(pdf_buffer)
    pdf_document.close()
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue(), pages_with_text

def show_pdf(pdf_data, p):
    """
    Embed a PDF in the Streamlit app.

    Args:
        pdf_data (bytes): PDF data to display.
    """
    # Encode the PDF data as base64
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    #pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page={p}" width="700" height="900" type="application/pdf"></iframe>'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'


    return(pdf_display)
    #st.markdown(pdf_display, unsafe_allow_html=True)



# # Streamlit UI
# st.title("PDF Text Highlighter")

# # File upload
# uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
# search_text = st.text_input("Enter the text to highlight")

# if uploaded_file and search_text:

#     highlighted_pdf_data, pages_with_text = highlight_text_in_pdf_and_extract_pages(
#         uploaded_file.read(), search_text
#     )

#     page = pages_with_text[0]
    
#     st.write("Highlighted PDF:")
#     show_pdf(highlighted_pdf_data, page)
    
#     # Provide a download button for the highlighted PDF
#     st.download_button(
#         label="Download Highlighted PDF",
#         data=highlighted_pdf_data,
#         file_name="highlighted.pdf",
#         mime="application/pdf",
#     )