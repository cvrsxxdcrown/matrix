from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


def parse_matrix(form_data, prefix):
    rows = int(form_data.get(f'{prefix}_rows', 0))
    cols = int(form_data.get(f'{prefix}_cols', 0))
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = form_data.get(f'{prefix}_{i}_{j}', '0')
            try:
                row.append(float(val))
            except ValueError:
                row.append(0.0)
        matrix.append(row)
    return np.array(matrix), rows, cols


def to_latex(matrix):
    latex = "\\begin{bmatrix}"
    for row in matrix:
        latex += " & ".join(f"{x:.2f}" for x in row) + r" \\"
    latex += "\\end{bmatrix}"
    return latex


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    matrix_a_latex = matrix_b_latex = result_latex = None
    operation_latex = operation_description = None
    matrix_steps = []

    matrix_a_values = {}
    matrix_b_values = {}
    a_rows = a_cols = b_rows = b_cols = 2
    selected_operation = 'add'

    if request.method == 'POST':
        try:
            a_rows = int(request.form.get('a_rows', 2))
            a_cols = int(request.form.get('a_cols', 2))
            b_rows = int(request.form.get('b_rows', 2))
            b_cols = int(request.form.get('b_cols', 2))
            selected_operation = request.form.get('operation')

            for i in range(a_rows):
                for j in range(a_cols):
                    key = f'a_{i}_{j}'
                    matrix_a_values[key] = request.form.get(key, '0')

            for i in range(b_rows):
                for j in range(b_cols):
                    key = f'b_{i}_{j}'
                    matrix_b_values[key] = request.form.get(key, '0')

            matrix_a, _, _ = parse_matrix(request.form, 'a')
            matrix_b, _, _ = parse_matrix(request.form, 'b')

            matrix_a_latex = to_latex(matrix_a)
            matrix_b_latex = to_latex(matrix_b)

            if selected_operation == 'add':
                if matrix_a.shape != matrix_b.shape:
                    raise ValueError("Размеры матриц не совпадают для сложения.")
                result = matrix_a + matrix_b
                result_latex = to_latex(result)
                operation_latex = f"{matrix_a_latex} + {matrix_b_latex} = {result_latex}"
            elif selected_operation == 'subtract':
                if matrix_a.shape != matrix_b.shape:
                    raise ValueError("Размеры матриц не совпадают для вычитания.")
                result = matrix_a - matrix_b
                result_latex = to_latex(result)
                operation_latex = f"{matrix_a_latex} - {matrix_b_latex} = {result_latex}"
            elif selected_operation == 'multiply':
                if matrix_a.shape[1] != matrix_b.shape[0]:
                    raise ValueError("Число столбцов A должно совпадать с числом строк B.")
                result = matrix_a @ matrix_b
                result_latex = to_latex(result)
                operation_latex = f"{matrix_a_latex} \\times {matrix_b_latex} = {result_latex}"
            elif selected_operation == 'transpose_a':
                result = matrix_a.T
                result_latex = to_latex(result)
                operation_description = "Транспонирование матрицы A"
                matrix_steps.append(f"{matrix_a_latex}^T = {result_latex}")
            elif selected_operation == 'transpose_b':
                result = matrix_b.T
                result_latex = to_latex(result)
                operation_description = "Транспонирование матрицы B"
                matrix_steps.append(f"{matrix_b_latex}^T = {result_latex}")
            elif selected_operation == 'inverse_a':
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Матрица A должна быть квадратной для обращения.")
                det = np.linalg.det(matrix_a)
                if np.isclose(det, 0):
                    raise ValueError("Матрица A вырождена — обратная не существует.")
                result = np.linalg.inv(matrix_a)
                result_latex = to_latex(result)
                operation_description = "Обратная матрица A"
                matrix_steps.append(f"{matrix_a_latex}^{{-1}} = {result_latex}")
            elif selected_operation == 'inverse_b':
                if matrix_b.shape[0] != matrix_b.shape[1]:
                    raise ValueError("Матрица B должна быть квадратной для обращения.")
                det = np.linalg.det(matrix_b)
                if np.isclose(det, 0):
                    raise ValueError("Матрица B вырождена — обратная не существует.")
                result = np.linalg.inv(matrix_b)
                result_latex = to_latex(result)
                operation_description = "Обратная матрица B"
                matrix_steps.append(f"{matrix_b_latex}^{{-1}} = {result_latex}")
            elif selected_operation == 'determinant_a':
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Матрица A должна быть квадратной для определителя.")
                det = np.linalg.det(matrix_a)
                result = det
                result_latex = f"\\det({matrix_a_latex}) = {det:.2f}"
                operation_description = "Определитель матрицы A"
                matrix_steps.append(result_latex)

            elif selected_operation == 'determinant_b':
                if matrix_b.shape[0] != matrix_b.shape[1]:
                    raise ValueError("Матрица B должна быть квадратной для определителя.")
                det = np.linalg.det(matrix_b)
                result = det
                result_latex = f"\\det({matrix_b_latex}) = {det:.2f}"
                operation_description = "Определитель матрицы B"
                matrix_steps.append(result_latex)

            elif selected_operation == 'rank_a':
                rank = np.linalg.matrix_rank(matrix_a)
                result = rank
                result_latex = f"\\text{{rank}}({matrix_a_latex}) = {rank}"
                operation_description = "Ранг матрицы A"
                matrix_steps.append(result_latex)

            elif selected_operation == 'rank_b':
                rank = np.linalg.matrix_rank(matrix_b)
                result = rank
                result_latex = f"\\text{{rank}}({matrix_b_latex}) = {rank}"
                operation_description = "Ранг матрицы B"
                matrix_steps.append(result_latex)

            else:
                error = "Неизвестная операция."
        except Exception as e:
            error = str(e)

    return render_template(
        'index.html',
        result=result,
        error=error,
        a_rows=a_rows,
        a_cols=a_cols,
        b_rows=b_rows,
        b_cols=b_cols,
        matrix_a_values=matrix_a_values,
        matrix_b_values=matrix_b_values,
        selected_operation=selected_operation,
        matrix_a_latex=matrix_a_latex,
        matrix_b_latex=matrix_b_latex,
        result_latex=result_latex,
        operation_latex=operation_latex,
        operation_description=operation_description,
        matrix_steps=matrix_steps
    )


if __name__ == '__main__':
    app.run(debug=True)
