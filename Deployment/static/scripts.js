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
        document.getElementById('result').innerText = 'GradeClass prediction: ' + data.prediction;
    })
    .catch(error => console.error('Error:', error));
}

function trainModel() {
    const selectedColumns = Array.from(document.querySelectorAll('input[name="columns"]:checked')).map(el => el.value);
    const selectedModel = document.getElementById('modelSelector').value;

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
    })
    .catch(error => console.error('Error:', error));
}
