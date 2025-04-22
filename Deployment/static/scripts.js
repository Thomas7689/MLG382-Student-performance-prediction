function validateInput(inputElement, min, max) {
    const value = parseFloat(inputElement.value);
    if (value < min) {
        alert(`${inputElement.name} must be at least ${min}.`);
        inputElement.value = min;
    } else if (value > max) {
        alert(`${inputElement.name} must be at most ${max}.`);
        inputElement.value = max;
    }
}

document.getElementById('age').addEventListener('input', function() {
    validateInput(this, 15, 18);
});

document.getElementById('gpa').addEventListener('input', function() {
    validateInput(this, 0, 4);
});

function submitForm() {
    const age = document.getElementById('age').value;
    const gpa = document.getElementById('gpa').value;
    const inputData = {
        Age: age,
        Gender: document.getElementById('gender').value,
        Ethnicity: document.getElementById('ethnicity').value,
        ParentalEducation: document.getElementById('parentalEducation').value,
        StudyTimeWeekly: document.getElementById('studyTimeWeekly').value,
        Absences: document.getElementById('absences').value,
        Tutoring: document.getElementById('tutoring').value,
        ParentalSupport: document.getElementById('parentalSupport').value,
        Extracurricular: document.getElementById('extracurricular').value,
        Sports: document.getElementById('sports').value,
        Music: document.getElementById('music').value,
        Volunteering: document.getElementById('volunteering').value,
        GPA: gpa
    };
    const selectedColumns = Array.from(document.querySelectorAll('input[name="columns"]:checked')).map(el => el.value);
    const selectedModel = document.getElementById('modelSelector').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_data: inputData, model: selectedModel, columns: selectedColumns })
    })
    .then(response => response.json())
    .then(data => {
        const gradeClassMap = ['A', 'B', 'C', 'D', 'F'];
        const gradeClass = gradeClassMap[data.prediction[0]];
        document.getElementById('result').innerHTML = `<strong>Grade Class Prediction:</strong> <span class="grade-class">${gradeClass}</span>`;
    })
    .catch(error => console.error('Error:', error));
}

function trainModel() {
    const selectedColumns = Array.from(document.querySelectorAll('input[name="columns"]:checked')).map(el => el.value);
    const selectedModel = document.getElementById('trainModelSelector').value;
    // Add loading cursor
    document.body.classList.add('loading');
    fetch('/train', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ model: selectedModel, columns: selectedColumns })
    })
    .then(response => response.json())
    .then(data => {
        alert('Model trained successfully!');
        updateModelSelector();
    })
    .catch(error => console.error('Error:', error))
    .finally(() => {
        // Remove loading cursor
        document.body.classList.remove('loading');
    });
}

function updateModelSelector() {
    fetch('/list_models')
    .then(response => response.json())
    .then(data => {
        const modelSelector = document.getElementById('modelSelector');
        modelSelector.innerHTML = '';
        Object.keys(data.models).forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.text = model;
            modelSelector.appendChild(option);
        });
        // Call updateInputFields after updating the model selector
        updateInputFields();
    })
    .catch(error => console.error('Error:', error));
}

function updateInputFields() {
    console.log("updateInputFields called");
    const selectedModel = document.getElementById('modelSelector').value;
    console.log("Selected model:", selectedModel);
    fetch(`/list_models`)
        .then(response => response.json())
        .then(data => {
            const selectedColumns = data.models[selectedModel];
            disableInputBoxes(selectedColumns);
        })
        .catch(error => console.error('Error:', error));
}

function disableInputBoxes(selectedColumns) {
    const predictionForm = document.getElementById('predictForm');
    const allInputBoxes = predictionForm.querySelectorAll('input, select');
    allInputBoxes.forEach(input => {
        if (input.id !== 'modelSelector' && !selectedColumns.includes(input.name)) {
            input.disabled = true;
        } else {
            input.disabled = false;
        }
    });
}

document.getElementById('modelSelector').addEventListener('change', updateInputFields);
document.addEventListener('DOMContentLoaded', updateModelSelector);
