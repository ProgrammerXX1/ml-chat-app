from setuptools import setup, find_packages

setup(
    name="rak_ml",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "weaviate-client",
        "sentence-transformers",
        "python-docx",
        "PyMuPDF",
        "langdetect",
        "deep-translator",
    ],
    author="Bek",
    description="RAG-система с Weaviate и LLM для локального использования",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
