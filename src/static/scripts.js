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

document.getElementById('studyTimeWeekly').addEventListener('input', function() {
    validateInput(this, 0, 100);
});

document.getElementById('absences').addEventListener('input', function() {
    validateInput(this, 0, 100);
});

function submitForm() {
    const inputData = {
        StudyTimeWeekly: document.getElementById('studyTimeWeekly').value,
        Absences: document.getElementById('absences').value,
        Tutoring: document.getElementById('tutoring').value,
        ParentalSupport: document.getElementById('parentalSupport').value,
        ParentalEducation: document.getElementById('parentalEducation').value
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
        if (data.error) {
            alert(data.error);
        } else {
            const gradeClassMap = ['A', 'B', 'C', 'D', 'F'];
            const gradeClass = gradeClassMap[data.prediction[0]];
            document.getElementById('result').innerHTML = `<strong>Grade Class Prediction:</strong> <span class="grade-class">${gradeClass}</span>`;
        }
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

function updateInputFields() {
    const selectedColumns = Array.from(document.querySelectorAll('input[name="columns"]:checked')).map(el => el.value);
    disableInputBoxes(selectedColumns);
}

document.querySelectorAll('input[name="columns"]').forEach(checkbox => {
    checkbox.addEventListener('change', updateInputFields);
});

document.addEventListener('DOMContentLoaded', () => {
    updateInputFields();
});