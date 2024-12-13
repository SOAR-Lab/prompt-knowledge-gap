# Towards Detecting Prompt Knowledge Gaps for Improved LLM-guided Issue Resolution
## Structure
```md
├── chrome_extenstion
│   └──  server -> flask server, run it locally before using the tool
│   └──  load the whole folder into the extension manager of google chrome to use as browser extension or simply open the html file in a browser to test
├── data
│   └──  conversations -> dataset of annotated conversations with gaps and styles
│   └──  conversations_heuristics -> conversations with calculated heuristics
│   └──  initial_styles_categories -> initial list of categories, their definition, and their sources
├── conversation_analysis
│   ├── files for the analysis done on the conversations
```

## Usage Instructions
### 1. Setting Up the Chrome Extension
Navigate to the chrome_extension/server folder.
Start the Flask server by running:\
```python app.py```\
Load the extension:\
Open Chrome and go to chrome://extensions/.
Enable "Developer Mode" (toggle switch in the top-right corner).
Click "Load Unpacked" and select the [Extension Folder] directory inside chrome_extension.\
Alternatively, to test directly, open index.html in any modern browser.

### 2. Accessing the Data
Annotated Conversations: Navigate to data/conversations for the primary dataset.
Conversations with Heuristics: Use data/conversations_heuristics for processed data ready for heuristic-based analysis.

### 3. Running Conversation Analysis
The conversation_analysis folder includes Python scripts and Jupyter notebooks.
Open the analysis notebook or run the scripts.
