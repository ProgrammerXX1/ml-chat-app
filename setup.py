from setuptools import setup, find_packages

setup(
    name="RAK_ml",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "weaviate-client",
        "sentence-transformers",
        "python-docx",
        "PyMuPDF",
        "langdetect",
        "deep-translator",
    ],
    author="Твоё имя",
    description="RAG-система с Weaviate и LLM для локального использования",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
