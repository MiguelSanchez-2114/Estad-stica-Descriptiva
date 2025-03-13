class Columna:
    nombre: str
    alineado: str

    def __init__(self, nombre:str, alineado:str = "centro"):
        self.nombre = nombre
        self.alineado = alineado.lower().strip()

class Tabla:
    columnas: list[Columna]
    datos: list[tuple]
    anchoColumnas: int
    totalColumnas: int
    totalFilas: int

    # Variables privadas inmutables
    __LIMITADORES = {
        "SEPARADOR_VERTICAL": "|",
        "SEPARADOR_HORIZONTAL": "-",
        "ESQUINA_SUP_IZQ": "┌",
        "ESQUINA_SUP_DER": "┐",
        "ESQUINA_INF_IZQ": "└",
        "ESQUINA_INF_DER": "┘",
        "INTERSECCION_IZQ": "├",
        "INTERSECCION_DER": "┤",
        "DOBLE_INTRSECCION": "┼",
        "SALTO_LINEA": "\n"
    }

    def __init__(self, columnas: list[Columna], datos: list[tuple] = [], anchoColumnas: int = 18):
        self.totalColumnas = len(columnas)
        self.columnas = columnas
        if datos:
            self.datos = datos
        else:
            self.datos = []
        self.totalFilas = len(datos)
        self.anchoColumnas = anchoColumnas
    
    def agregarFila(self, datos: tuple):
        self.datos.append(datos)
        self.totalFilas += 1
    
    def reemplazarDatos(self, datos: list[tuple]):
        self.datos = datos
    
    def dibujar(self):
        [tabla, anchoEncabezado] = self.__crearEncabezado()

        for i in range(self.totalFilas):
            tabla += self.__LIMITADORES["SEPARADOR_VERTICAL"]
            for j in range(self.totalColumnas):
                tabla += self.__alinearTexto(f"{self.datos[i][j]}", self.columnas[j].alineado)
                tabla += self.__LIMITADORES["SEPARADOR_VERTICAL"]
            tabla += self.__LIMITADORES["SALTO_LINEA"]
        
        tabla += self.__crearCierre(anchoEncabezado)

        print(tabla)

    def __crearEncabezado(self):
        encabezado = self.__LIMITADORES["SEPARADOR_VERTICAL"]
        for i in range(self.totalColumnas):
            encabezado += self.columnas[i].nombre.ljust(self.anchoColumnas)
            encabezado += self.__LIMITADORES["SEPARADOR_VERTICAL"]
        encabezado += self.__LIMITADORES["SALTO_LINEA"]
        
        anchoEncabezado = len(encabezado)-3
        encabezadoFormateado = self.__LIMITADORES["ESQUINA_SUP_IZQ"]
        encabezadoFormateado += "".center(anchoEncabezado,self.__LIMITADORES["SEPARADOR_HORIZONTAL"])
        encabezadoFormateado += self.__LIMITADORES["ESQUINA_SUP_DER"]+self.__LIMITADORES["SALTO_LINEA"]
        encabezadoFormateado += encabezado
        encabezadoFormateado += self.__LIMITADORES["INTERSECCION_IZQ"]
        encabezadoFormateado += "".center(anchoEncabezado,self.__LIMITADORES["SEPARADOR_HORIZONTAL"])
        encabezadoFormateado += self.__LIMITADORES["INTERSECCION_DER"]+self.__LIMITADORES["SALTO_LINEA"]
        return [encabezadoFormateado, anchoEncabezado]
    
    def __crearCierre(self, anchoTotal: int):
        cierre = self.__LIMITADORES["ESQUINA_INF_IZQ"]
        cierre += "".center(anchoTotal,self.__LIMITADORES["SEPARADOR_HORIZONTAL"])
        cierre += self.__LIMITADORES["ESQUINA_INF_DER"]
        return cierre

    def __alinearTexto(self, texto: str, alineado: str):
        ancho = self.anchoColumnas
        if len(texto) > ancho:
            texto = texto[:ancho-3]+"..."
        match alineado:
            case "derecha":
                texto = texto.rjust(ancho)
            case "izquierda":
                texto = texto.ljust(ancho)
            case _:
                texto = texto.center(ancho)
        return texto
