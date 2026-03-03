# Steve Jobs (1955–1996) Persona LLM

Designed and implemented a temporally constrained LLM persona system using retrieval-based grounding, input/output policy enforcement, and local model deployment via Ollama. Developed a web-based interface and implemented timeline containment mechanisms to prevent post-1996 knowledge leakage.

##  Features

- Timeline restriction (pre-1997 only)
- Input policy enforcement
- Output validation filtering
- Retrieval-based historical grounding
- Local deployment using Ollama
- Web interface (Flask)

## Architecture

User → Retrieval Layer → LLM → Output Validation → Response

The system prevents:
- Post-1996 knowledge leakage
- Future speculation
- References to later Apple products (iPhone, iPad, etc.)
- References to Steve Jobs’ death (2011)

##  Setup Instructions

### 1. Install Ollama
https://ollama.com

### 2. Pull Base Model

ollama pull phi3:mini

### 3. Create Custom Model

ollama create steve1996 -f Modelfile

### 4. Install Python Dependencies

pip install -r requirements.txt

### 5. Run Web Interface

python app.py

open: http://127.0.0.1:5000

## Project Purpose

This project demonstrates:

-LLM constraint engineering
-Retrieval-Augmented Generation (RAG)
-Temporal containment strategies
-Safe persona simulation
-Local LLM deployment without GPU