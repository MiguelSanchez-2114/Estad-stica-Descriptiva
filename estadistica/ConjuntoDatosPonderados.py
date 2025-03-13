from functools import reduce

class ConjuntoDatosPonderados:
    datos: list[tuple]
    totalDatos: int
    totalObservaciones: int
    precision:int

    def __init__(self, datos:list[tuple] = [], precision:int = 2):
        self.datos = datos
        self.totalDatos = len(self.datos)
        self.totalObservaciones = reduce(lambda acumulador, dato: acumulador + dato[0], datos, 0)
        self.precision = precision
    
    def media(self, mostrar:bool = True) -> float:
        suma = 0
        sumaEscrita1 = sumaEscrita2 = "Sumatoria: "
        for i in range(self.totalDatos):
            dato = self.datos[i]
            datoPonderado = dato[0] * dato[1]
            sumaEscrita1 += f"({dato[0]} X {dato[1]})"
            sumaEscrita2 += f"{datoPonderado}"
            if not i == self.totalDatos - 1:
                sumaEscrita1 += " + "
                sumaEscrita2 += " + "
            suma += datoPonderado
        media = round((suma / self.totalObservaciones), ndigits=self.precision)
        texto = f"Total de observaciones: {self.totalObservaciones}\n"
        texto += f"{sumaEscrita1}\n"
        texto += f"{sumaEscrita2} = {suma}\n"
        texto += f"Media: {suma} / {self.totalObservaciones} = {media}"
        if mostrar:
            print(texto)
        return media
    