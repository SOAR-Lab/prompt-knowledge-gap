document.addEventListener("DOMContentLoaded", function () {
    // Code Snippet Add Button
    document.getElementById("add-code-snippet").addEventListener("click", addCodeSnippet);

    // Library Add Button
    document.getElementById("add-library").addEventListener("click", addLibrary);

    // Resource Add Button
    document.getElementById("add-resource").addEventListener("click", addResource);

    // Other necessary event listeners can go here
});

let prompt = '';

// Array to hold code snippets
let codeSnippets = [];

// Add code snippet (via upload or manual entry)
function addCodeSnippet() {
    const fileInput = document.getElementById("code-upload");
    const fileNameInput = document.querySelector(".file-name-input");
    const textAreaInput = document.querySelector(".textarea-input");
    const fileList = document.getElementById("file-list");
    const fileExtensionDropdown = document.querySelector(".file-extension-dropdown");


    // Handle file uploads
    if (fileInput.files.length > 0) {
        Array.from(fileInput.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(event) {
                // Get the file content
                const fileContent = event.target.result;
                
                // Save the file name and content in the codeSnippets array
                codeSnippets.push({ name: file.name, content: fileContent });
                console.log("Current Code Snippets Array:", codeSnippets);

                // Display the uploaded file in the UI
                const listItem = document.createElement("div");
                listItem.textContent = `Uploaded: ${file.name}`;
                fileList.appendChild(listItem);
                
                // Create a remove button
                const removeButton = document.createElement("button");
                removeButton.textContent = "Remove";
                removeButton.addEventListener("click", () => {
                    listItem.remove();
                    // Remove the snippet from the array
                    codeSnippets = codeSnippets.filter(snippet => snippet.name !== file.name);
                });
                removeButton.classList.add("remove-button");
                listItem.appendChild(removeButton);
            };
            // Read the file as text
            reader.readAsText(file);
        });
        fileInput.value = ""; // Clear the input
    } 
    // Handle manual input
    else if (fileNameInput.value && textAreaInput.value) {
        const selectedExtension = fileExtensionDropdown.value;
        const fullFileName = `${fileNameInput.value}${selectedExtension}`;

        const listItem = document.createElement("div");
        listItem.textContent = `Uploaded: ${fullFileName}`;
        fileList.appendChild(listItem);

        // Save the manual input in the codeSnippets array
        codeSnippets.push({ name: fullFileName, content: textAreaInput.value });
        console.log("Current Code Snippets Array:", codeSnippets);

        // Clear the inputs
        fileNameInput.value = "";
        textAreaInput.value = "";

        // Create a remove button
        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.addEventListener("click", () => {
            listItem.remove();
            // Remove the snippet from the array
            codeSnippets = codeSnippets.filter(snippet => snippet.name !== fullFileName);
        });
        removeButton.classList.add("remove-button");
        listItem.appendChild(removeButton);
    }
}
// Array to hold libraries
let libraries = [];

// Add/remove libraries
function addLibrary() {
    const libraryInput = document.querySelector("#libraries-list input");
    if (libraryInput.value) {
        const libraryName = libraryInput.value;

        const libraryDiv = document.createElement("div");
        libraryDiv.textContent = libraryName;
        libraryDiv.classList.add("library-item");

        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.addEventListener("click", () => {
            libraryDiv.remove();
            // Remove the library from the array
            libraries = libraries.filter(lib => lib !== libraryName);
            // Log the updated state of the libraries array after removal
            console.log("Updated Libraries Array after removal:", libraries);
        });
        removeButton.classList.add("remove-button");
        libraryDiv.appendChild(removeButton);

        document.getElementById("libraries-list").appendChild(libraryDiv);
        libraryInput.value = "";

        // Add the library to the array and log the current state
        libraries.push(libraryName);
        console.log("Current Libraries Array:", libraries);
    }
}

// Array to hold resources
let resources = [];

// Add/remove resources
function addResource() {
    const resourceInput = document.querySelector("#resources-list input");
    if (resourceInput.value) {
        const resourceName = resourceInput.value;

        const resourceDiv = document.createElement("div");
        resourceDiv.textContent = resourceName;
        resourceDiv.classList.add("resource-item");

        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.addEventListener("click", () => {
            resourceDiv.remove();
            // Remove the resource from the array
            resources = resources.filter(res => res !== resourceName);
            // Log the updated state of the resources array after removal
            console.log("Updated Resources Array after removal:", resources);
        });
        removeButton.classList.add("remove-button");
        resourceDiv.appendChild(removeButton);

        document.getElementById("resources-list").appendChild(resourceDiv);
        resourceInput.value = "";

        // Add the resource to the array and log the current state
        resources.push(resourceName);
        console.log("Current Resources Array:", resources);
    }
}

// Function to update the progress bars based on JSON response
function updateProgressBars(results) {
    // Set width, text, and percentage for each progress bar based on JSON values
    document.querySelector(".score-bar:nth-child(2) .progress").style.width = results['Contextual Richness'] + '%';
    document.querySelector(".score-bar:nth-child(2) .progress").innerText = getLabelText(results['Contextual Richness'], results['Contextual Richness']);
    
    document.querySelector(".score-bar:nth-child(3) .progress").style.width = results['Specificity'] + '%';
    document.querySelector(".score-bar:nth-child(3) .progress").innerText = getLabelText(results['Specificity'], results['Specificity']);
    
    document.querySelector(".score-bar:nth-child(4) .progress").style.width = results['Clarity'] + '%';
    document.querySelector(".score-bar:nth-child(4) .progress").innerText = getLabelText(results['Clarity'], results['Clarity']);

    prompt = results['prompt']
    
    // Update colors based on the width
    updateProgressBarColors();
}

// Function to get label text with percentage based on the width
function getLabelText(label, percentage) {
    let labelText;
    if (label < 20) {
        labelText = 'Bad';
    } else if (label < 50) {
        labelText = 'Ok';
    } else {
        labelText = 'Good';
    }
    return `${label.toFixed(2)}%`;  // Add percentage to the label
}

// Function to set color based on progress width
function updateProgressBarColors() {
    // Select all progress bars
    const progressBars = document.querySelectorAll(".progress");
    progressBars.forEach(progress => {
        // Get the width value from the inline style (remove % sign and convert to number)
        const width = parseInt(progress.style.width);

        // Set color based on width value
        if (width < 20) {
            progress.style.backgroundColor = "red";
        } else if (width < 50) {
            progress.style.backgroundColor = "#fca103";
            // progress.style.color = "#000"; // Default color (green)
        } else {
            progress.style.backgroundColor = "#4caf50"; // Default color (green)
        }
    });
}

// Call the function on page load or whenever progress bars are updated
document.addEventListener("DOMContentLoaded", updateProgressBarColors);

document.getElementById('submit-btn').addEventListener('click', function () {
    // Show progress bar and set initial progress
    document.getElementById("scores").style.display = "none";
    document.getElementById("progress-bar-container").style.display = "block";
    document.getElementById("progress").style.width = "0%";
    
    let progress = 0;
    let interval = setInterval(() => {
        if (progress >= 100) {
            clearInterval(interval);
            // Hide progress bar and show scores
            document.getElementById("progress-bar-container").style.display = "none";
            document.getElementById("scores").style.display = "block";
            document.getElementById("suggestions").style.display = "block";
        } else {
            progress += 10;
            document.getElementById("progress").style.width = progress + "%";
            document.getElementById("progress").innerText = progress + "%";
        }
    }, 500); // Adjust time for faster or slower progress
    // Gather form data
    const issue = document.getElementById('issue').value;
    const expectedOutcome = document.getElementById('expected-outcome').value;
    const programmingLanguage = document.getElementById('programming-language').value;
    const languageVersion = document.getElementById('language-version').value;

    // Gather error log
    const errorLog = document.getElementById('error-log').value;

    // Create the payload
    const payload = {
        issue,
        expectedOutcome,
        programmingLanguage,
        languageVersion,
        codeSnippets,
        errorLog,
        resources,
        libraries
    };

    console.log(JSON.stringify(payload))

    // Send the data to the Flask server
    fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            console.error('HTTP error', response.status);
            return;
        }
        return response.json();
    })
    .then(results => {
        // document.getElementById("scores").style.display = "block";
        updateProgressBars(results);
    })
    .catch(error => console.error('Fetch error:', error));
});

document.getElementById("copy-btn").addEventListener("click", function() {
    const textToCopy = prompt; // Replace this with dynamic content if needed

    navigator.clipboard.writeText(textToCopy).then(() => {
        alert("Copied to clipboard!");
    }).catch(err => {
        console.error("Failed to copy: ", err);
    });
});