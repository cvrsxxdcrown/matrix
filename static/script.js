document.addEventListener("DOMContentLoaded", function () {
    // Динамическое изменение размеров матриц
    window.onSizeChange = function (matrixName) {
        const rowsInput = document.querySelector(`input[name='${matrixName}_rows']`);
        const colsInput = document.querySelector(`input[name='${matrixName}_cols']`);
        const rows = parseInt(rowsInput.value);
        const cols = parseInt(colsInput.value);
        const container = document.getElementById(`${matrixName}_matrix`);

        // Удаляем старые поля
        container.innerHTML = '';

        // Создаём новые поля
        for (let i = 0; i < rows; i++) {
            const rowDiv = document.createElement('div');
            for (let j = 0; j < cols; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.step = 'any';
                input.name = `${matrixName}_${i}_${j}`;
                input.className = 'matrix-cell';
                input.value = 0; // начальное значение
                rowDiv.appendChild(input);
            }
            container.appendChild(rowDiv);
        }
    };
});

// Копирование результата
function copyResult() {
    const resultBlock = document.getElementById("result-block");
    if (!resultBlock) return;
    const range = document.createRange();
    range.selectNode(resultBlock);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {
        document.execCommand("copy");
        alert("Результат скопирован!");
    } catch (err) {
        alert("Ошибка при копировании");
    }
    window.getSelection().removeAllRanges();
}