# Towards Detecting Prompt Knowledge Gaps for Improved LLM-guided Issue Resolution
This replication package provides all the necessary components to replicate the analysis and findings presented in the study. The package is organized into structured directories containing the browser extension, annotated datasets, heuristic calculations, and analysis scripts.

## Structure
```md
├── chrome_extenstion
│   └──  server -> flask server, run it locally before using the tool
│   └──  load the whole folder into the extension manager of Google Chrome to use as a browser extension or simply open the HTML file in a browser to test
├── data
│   └──  conversations -> dataset of annotated conversations with gaps and styles
│   └──  conversations_heuristics -> conversations with calculated heuristics
│   └──  initial_styles_categories -> initial list of conversation styles categories, their definition, and their sources
├── conversation_analysis
│   ├── files for the analysis done on the conversations
```

## Usage Instructions
### 1. Setting Up the Chrome Extension
Navigate to the chrome_extension/server folder.
Start the Flask server by running:\
```python main.py```

**Load the extension:**\
Open Chrome and go to ``chrome://extensions/``.
Enable ``Developer Mode`` (toggle switch in the top-right corner).
Click ``Load Unpacked`` and select the [Extension Folder] directory inside ``chrome_extension``.\
Alternatively, to test directly, open ``chrome_extenstion/hello.html`` in any modern browser.

### 2. Accessing the Data
**Annotated Conversations**: Navigate to ``data/conversations`` for the primary dataset.\
**Conversations with Heuristics**: Use ``data/conversations_heuristics`` for processed data ready for heuristic-based analysis.\
You could also refer to ``data/initial_styles_categories`` to read about the conversation styles categories, their definition, and the sources used for our annotations.

### 3. Running Conversation Analysis
The ``conversation_analysis`` folder includes Python scripts and Jupyter notebooks.
Open the analysis notebooks and run the scripts.\
Files ``heuristics.ipynb``, ``neuralcoref.ipynb.ipynb``, and ``main.py`` are for generating the heuristics based on the provided dataset.\
File ``annotation_analysis.ipynb`` is used to analyze the annotation done for the study.
