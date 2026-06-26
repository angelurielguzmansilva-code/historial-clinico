import time

class NodoBST:
    def __init__(self, id_paciente, nombre, edad, diagnostico):
        self.id = id_paciente
        self.nombre = nombre
        self.edad = edad
        self.diagnostico = diagnostico
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, id_paciente, nombre, edad, diagnostico):
        nuevo = NodoBST(id_paciente, nombre, edad, diagnostico)
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar_recursivo(self.raiz, nuevo)

    def _insertar_recursivo(self, actual, nuevo):
        if nuevo.id < actual.id:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
            else:
                self._insertar_recursivo(actual.izquierdo, nuevo)
        elif nuevo.id > actual.id:
            if actual.derecho is None:
                actual.derecho = nuevo
            else:
                self._insertar_recursivo(actual.derecho, nuevo)
        else:
            actual.nombre = nuevo.nombre
            actual.edad = nuevo.edad
            actual.diagnostico = nuevo.diagnostico

    def buscar(self, id_paciente):
        return self._buscar_recursivo(self.raiz, id_paciente)

    def _buscar_recursivo(self, actual, id_paciente):
        if actual is None or actual.id == id_paciente:
            return actual
        if id_paciente < actual.id:
            return self._buscar_recursivo(actual.izquierdo, id_paciente)
        return self._buscar_recursivo(actual.derecho, id_paciente)

    def eliminar(self, id_paciente):
        self.raiz = self._eliminar_recursivo(self.raiz, id_paciente)

    def _eliminar_recursivo(self, actual, id_paciente):
        if actual is None:
            return actual
        if id_paciente < actual.id:
            actual.izquierdo = self._eliminar_recursivo(actual.izquierdo, id_paciente)
        elif id_paciente > actual.id:
            actual.derecho = self._eliminar_recursivo(actual.derecho, id_paciente)
        else:
            if actual.izquierdo is None:
                return actual.derecho
            elif actual.derecho is None:
                return actual.izquierdo
            temporal = self._minimo_valor_nodo(actual.derecho)
            actual.id = temporal.id
            actual.nombre = temporal.nombre
            actual.edad = temporal.edad
            actual.diagnostico = temporal.diagnostico
            actual.derecho = self._eliminar_recursivo(actual.derecho, temporal.id)
        return actual

    def _minimo_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def obtener_en_orden(self):
        lista_pacientes = []
        self._inorden_recursivo(self.raiz, lista_pacientes)
        return lista_pacientes

    def _inorden_recursivo(self, actual, lista):
        if actual:
            self._inorden_recursivo(actual.izquierdo, lista)
            lista.append({
                "id": actual.id,
                "nombre": actual.nombre,
                "edad": actual.edad,
                "diagnostico": actual.diagnostico
            })
            self._inorden_recursivo(actual.derecho, lista)

class NodoLista:
    def __init__(self, fecha, id_buscado, resultado):
        self.fecha = fecha
        self.id_buscado = id_buscado
        self.resultado = resultado
        self.siguiente = None
        self.anterior = None

class ListaDoblementeLigada:
    def __init__(self):
        self.cabeza = None

    def insertar_inicio(self, fecha, id_buscado, resultado):
        nuevo = NodoLista(fecha, id_buscado, resultado)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo

    def obtener_historial(self):
        historial = []
        actual = self.cabeza
        while actual is not None:
            historial.append({
                "fecha": actual.fecha,
                "id_buscado": actual.id_buscado,
                "resultado": actual.resultado
            })
            actual = actual.siguiente
        return historial

def busqueda_secuencial(lista_pacientes, id_buscado):
    for p in lista_pacientes:
        if p['id'] == id_buscado:
            return p
    return None