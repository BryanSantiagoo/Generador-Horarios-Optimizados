import csv
import numpy as np
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Leer el archivo e imprimirlo por filas
materias = []

with open('D:/Proyecto Modelos/Data.csv', encoding="utf8", errors='ignore') as archivo:
    mat = csv.reader(archivo)
    for i in mat:
        if i[0] != "":
            materias.append([i[0], i[1], i[2]])

# Función que retorna el nombre de la materia
def retNomMat(ind):
    for i in materias:
        if i[0] == ind:
            return i[2]

@app.route('/', methods=['GET', 'POST'])
def index():
    schedule = None
    filtered_materias = []
    
    #indx=[16,20,21,22,25]
    #indx=[9,10,51,52,53]
    indx=[54,11,55,56,57]
    #indx=[27,28,29,30]

    if request.method == 'POST':
        selected_materias_ids = request.form.getlist('materias')  # Obtener la lista de IDs de materias seleccionadas

        # Filtrar las materias seleccionadas
        for materia in materias:
            if materia[0] in selected_materias_ids:
                filtered_materias.append(materia)

        if 'generar_horario' in request.form:
            num_materias = int(request.form['num_materias'])
            restriccion = int(request.form['restriccion'])
            dia_libre = int(request.form['dia_libre'])
            categoria = int(request.form['categoria'])

            # Filtrar materias por categoría
            for i, materia in enumerate(materias):
                if (categoria == 1 and 13 <= i+1 <= 40):
                    filtered_materias.append(materia)
                elif(categoria == 2 and 41 <= i+1 <= 66):
                    filtered_materias.append(materia)
                elif(categoria == 3 and i+1 <= 12):
                    filtered_materias.append(materia)

            # Limitar el número de materias seleccionadas
            selected_materias = filtered_materias[:num_materias]

            # Generar el horario
            arr = np.zeros((6, 5))
            count = 0

            while count < num_materias:
                if restriccion == 0:
                    row = random.randint(0, 2)
                    col = random.randint(0,2)
                elif restriccion == 1:
                    row = random.randint(3, 5)
                    col = random.randint(0,2)
                else:
                    row = random.randint(0, 5)
                    col = random.randint(0,2)

                if dia_libre == 1 and (col == 0 or col == 2):
                    continue
                elif dia_libre == 2 and (col == 1 or col == 3):
                    continue
                elif dia_libre == 3 and (col == 2 or col == 0):
                    continue
                elif dia_libre == 4 and (col == 3 or col == 1):
                    continue
                elif dia_libre == 5 and (col == 4 or col == 2):
                    continue

                if arr[row][col] == 0 and arr[row][(col+2)%5] == 0:
                    arr[row][col] = indx[count]
                    arr[row][(col+2)%5] = indx[count]
                    count += 1

            schedule = arr.tolist()
            
        indii=0
        indij=0
        for i in schedule:
            for j in i:
                if(j!=0):
                    k=str(int(j))
                    schedule[indii][indij]=str(retNomMat(k))
                indij=indij+1
            indii=indii+1
            indij=0

    return render_template('index.html', schedule=schedule, materias=filtered_materias)

if __name__ == '__main__':
    app.run(debug=True)
