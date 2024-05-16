document.addEventListener('DOMContentLoaded', function () {
    const analyzeButton = document.getElementById('analyzeButton');
    const clearButton = document.getElementById('clearButton');
    const loadFileButton = document.getElementById('loadFileButton');
    const codeInput = document.getElementById('codeInput');
    const tokensTable = document.getElementById('tokensTable').getElementsByTagName('tbody')[0];

    analyzeButton.addEventListener('click', function () {
        const code = codeInput.value;
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `code=${encodeURIComponent(code)}`
        })
        .then(response => response.json())
        .then(data => {
            tokensTable.innerHTML = '';
            data.tokens.forEach(token => {
                const row = tokensTable.insertRow();
                row.insertCell(0).textContent = token.line;
                row.insertCell(1).textContent = token.token;
                token.types.forEach(type => {
                    const cell = row.insertCell();
                    cell.textContent = type ? 'X' : '';
                });
            });
            const totalRow = tokensTable.insertRow();
            totalRow.classList.add('total');
            totalRow.insertCell(0).textContent = 'Total';
            totalRow.insertCell(1).textContent = '';
            Object.values(data.token_counts).forEach(count => {
                const cell = totalRow.insertCell();
                cell.textContent = count;
            });
        });
    });

    clearButton.addEventListener('click', function () {
        codeInput.value = '';
        tokensTable.innerHTML = '';
    });

    loadFileButton.addEventListener('click', function () {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.txt';
        input.onchange = function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    codeInput.value = e.target.result;
                };
                reader.readAsText(file);
            }
        };
        input.click();
    });
});
