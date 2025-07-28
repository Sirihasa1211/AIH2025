FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install pymupdf numpy scikit-learn
CMD ["python", "process_pdfs.py"] 