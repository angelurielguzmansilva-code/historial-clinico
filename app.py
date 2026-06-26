from flask import Flask, render_template, request, redirect, url_for
from estructura import ArbolBinarioBusqueda, ListaDoblementeLigada, busqueda_secuencial
import csv
import os
import time
from datetime import datetime

app = Flask(__name__)

db_pacientes = ArbolBinarioBusqueda()
historial_busquedas = ListaDoblementeLigada()

CSV_FILE = "pacientes.csv"


def cargar_datos():
    if not os.path.exists(CSV_FILE):
        open(CSV_FILE, "w", encoding="utf-8").close()
        return

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            try:
                db_pacientes.insertar(
                    int(row[0]),
                    row[1],
                    int(row[2]),
                    row[3]
                )
            except:
                pass


def guardar_datos():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for p in db_pacientes.obtener_en_orden():
            writer.writerow([
                p["id"],
                p["nombre"],
                p["edad"],
                p["diagnostico"]
            ])


cargar_datos()


@app.route("/")
def index():

    pacientes = db_pacientes.obtener_en_orden()
    historial = historial_busquedas.obtener_historial()

    estadisticas = {}

    for p in pacientes:
        estadisticas[p["diagnostico"]] = estadisticas.get(
            p["diagnostico"], 0
        ) + 1

    return render_template(
        "index.html",
        pacientes=pacientes,
        historial=historial,
        estadisticas=estadisticas,
        experimento=None
    )


@app.route("/agregar", methods=["POST"])
def agregar():

    db_pacientes.insertar(
        int(request.form["id"]),
        request.form["nombre"],
        int(request.form["edad"]),
        request.form["diagnostico"]
    )

    guardar_datos()

    return redirect(url_for("index"))


@app.route("/eliminar/<int:id_p>", methods=["POST"])
def eliminar(id_p):

    db_pacientes.eliminar(id_p)

    guardar_datos()

    return redirect(url_for("index"))


@app.route("/buscar", methods=["POST"])
def buscar():

    id_buscado = int(request.form["id_busqueda"])

    inicio = time.perf_counter()
    resultado = db_pacientes.buscar(id_buscado)
    tiempo_bst = (time.perf_counter() - inicio) * 1000

    lista = db_pacientes.obtener_en_orden()

    inicio = time.perf_counter()
    busqueda_secuencial(lista, id_buscado)
    tiempo_seq = (time.perf_counter() - inicio) * 1000

    estado = (
        f"Encontrado ({resultado.nombre})"
        if resultado
        else "No encontrado"
    )

    historial_busquedas.insertar_inicio(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        id_buscado,
        estado
    )

    pacientes = db_pacientes.obtener_en_orden()
    historial = historial_busquedas.obtener_historial()

    estadisticas = {}

    for p in pacientes:
        estadisticas[p["diagnostico"]] = estadisticas.get(
            p["diagnostico"], 0
        ) + 1

    experimento = {
        "id": id_buscado,
        "tiempo_bst": f"{tiempo_bst:.6f} ms",
        "tiempo_seq": f"{tiempo_seq:.6f} ms",
        "eficiencia":
            f"{tiempo_seq/(tiempo_bst if tiempo_bst>0 else 0.000001):.1f}x"
    }

    return render_template(
        "index.html",
        pacientes=pacientes,
        historial=historial,
        estadisticas=estadisticas,
        experimento=experimento
    )


@app.route("/paciente/<int:id_p>")
def ver_paciente(id_p):

    paciente = db_pacientes.buscar(id_p)

    if paciente:

        return render_template(
            "paciente.html",
            paciente={
                "id": paciente.id,
                "nombre": paciente.nombre,
                "edad": paciente.edad,
                "diagnostico": paciente.diagnostico
            }
        )

    return "Paciente no encontrado", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')