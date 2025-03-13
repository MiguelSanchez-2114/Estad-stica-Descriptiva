from EstadisticaDescriptiva.graficas import Tabla, Columna
from math import floor, sqrt
from functools import reduce

class ConjuntoDatos:
    datos:list
    totalObservaciones: int
    precision:int

    def __init__(self, datos:list, precision:int = 2) -> None:
        self.datos = datos
        self.totalObservaciones = len(datos)
        self.precision = precision

    def __datosOrdenados(self) -> list:
        datos = self.datos
        datos.sort()
        return datos

    def __formatNumber(self, number) -> float:
        return round(number, ndigits=self.precision)
    
    def media(self, mostrar:bool = True) -> float:
        caracteresObservaciones = f"{self.__datosOrdenados()[-1]}".__len__()
        suma = 0
        sumaEscrita = "Sumatoria: \n"
        for i in range(self.totalObservaciones):
            dato = self.datos[i]
            sumaEscrita += f"{dato}".rjust(caracteresObservaciones)
            if i == 0:
                sumaEscrita += " +"
            elif i == self.totalObservaciones - 1:
                sumaEscrita += " ="
            sumaEscrita += "\n"
            suma += dato
        sumaEscrita += "".rjust(caracteresObservaciones+2,"-")
        media = round((suma / self.totalObservaciones), ndigits=self.precision)
        texto = f"Total de observaciones: {self.totalObservaciones}\n"
        texto += f"{sumaEscrita}\n{suma}\n"
        texto += f"Media: {suma} / {self.totalObservaciones} = {media}"
        if mostrar:
            print(texto)
        return media
    
    def sumatoriaDiferenciasMedia(self, mostrar:bool = True) -> float:
        media = self.media(mostrar=False)
        print(f"Media: {media}")
        
        tabla = Tabla(columnas=[
            Columna(nombre="Observacion", alineado="centro"),
            Columna(nombre="Diferencia", alineado="derecha"),
            Columna(nombre="Acumulado", alineado="derecha")
        ], anchoColumnas=18)

        acumulado = 0
        for i in range(self.totalObservaciones):
            dato = self.datos[i]
            diferencia = dato - media
            acumulado += diferencia
            tabla.agregarFila(datos=[
                f"{dato}",
                f"{dato} - {media} = {diferencia}",
                f"{acumulado}"
            ])
        tabla.dibujar()
        return acumulado

    def mediana(self, mostrar: bool = True) -> float:
        datosOrdenados = self.__datosOrdenados()
        caracteresOrdinales = f"{self.totalObservaciones}".__len__()
        caracteresObservaciones = f"{datosOrdenados[-1]}".__len__()
        centro = floor((self.totalObservaciones / 2)) - 1
        medianaTexto = ''
        posCentro = []
        if self.totalObservaciones % 2 == 0:
            mediana = round(((datosOrdenados[centro] + datosOrdenados[centro + 1]) / 2), ndigits=self.precision)
            medianaTexto = f"({datosOrdenados[centro]} + {datosOrdenados[centro + 1]}) / 2 = {mediana}"
            posCentro = [centro, centro + 1]
        else:
            mediana = datosOrdenados[centro]
            medianaTexto = f"{mediana}"
            posCentro = [centro]
        print("Datos ordenados:")
        for i in range(datosOrdenados.__len__()):
            datoTexto = f"{(i+1)}".rjust(caracteresOrdinales)+".- "+f"{datosOrdenados[i]}".rjust(caracteresObservaciones)
            if posCentro.count(i) > 0:
                datoTexto += " * "
            print(datoTexto)
        print(f"Mediana: {medianaTexto}")
        return mediana
    
    def moda(self, mostrar: bool = True) -> list[float]:
        datosOrdenados = self.__datosOrdenados()
        datosPonderados = []
        valor = None
        maximo = None
        moda = None
        posModa = None
        
        tabla = Tabla(columnas=[
            Columna(nombre="Observacion", alineado="centro"),
            Columna(nombre="Repeticiones", alineado="derecha")
        ], anchoColumnas=18)
        for i in range(self.totalObservaciones):
            dato = datosOrdenados[i]
            if not valor == dato:
                if valor != None:
                    datosPonderados.append([valor, contador])
                    tabla.agregarFila([valor, contador])
                    if maximo == None or contador > maximo:
                        maximo = contador
                        moda = [valor]
                        posModa = [len(datosPonderados) - 1]
                    elif not maximo == None and contador == maximo:
                        moda.append(valor)
                        posModa.append(len(datosPonderados) - 1)
                valor = dato
                contador = 0
            contador += 1
        datosPonderados.append([valor, contador])
        tabla.agregarFila([valor, contador])
        if maximo == None or contador > maximo:
            maximo = contador
            moda = [valor]
            posModa = [len(datosPonderados) - 1]
        elif not maximo == None and contador == maximo:
            moda.append(valor)
            posModa.append(len(datosPonderados) - 1)
        print("Datos agrupados: ")
        tabla.dibujar()
        datosModa = list(map(lambda i: datosPonderados[i], posModa))
        tabla = Tabla(columnas=[
            Columna(nombre="Moda", alineado="centro"),
            Columna(nombre="Repeticiones", alineado="derecha")
        ], anchoColumnas=18, datos=datosModa)
        tabla.dibujar()
        return moda

    def rango(self, mostrar: bool = True) -> float:
        datosOrdenados = self.__datosOrdenados()
        minimo = datosOrdenados[0]
        maximo = datosOrdenados[-1]
        caracteresOrdinales = f"{self.totalObservaciones}".__len__()
        caracteresObservaciones = f"{maximo}".__len__()
        if mostrar:
            print("Datos ordenados:")
            for i in range(datosOrdenados.__len__()):
                datoTexto = f"{(i+1)}".rjust(caracteresOrdinales)+".- "+f"{datosOrdenados[i]}".rjust(caracteresObservaciones)
                if i == 0 or i == self.totalObservaciones - 1:
                    datoTexto += " * "
                print(datoTexto)
        rango = maximo - minimo
        if mostrar:
            print("Rango:")
            print(f"{maximo} - {minimo} = {rango}")
        return rango

    def varianza(self, mostrar: bool = True) -> float:
        media = self.media(mostrar=False)
        if mostrar:
            print(f"Media: {media}")
        
        tabla = Tabla(columnas=[
            Columna(nombre="Observacion", alineado="centro"),
            Columna(nombre="Diferencia", alineado="derecha"),
            Columna(nombre="Cuadrado", alineado="derecha"),
            Columna(nombre="Acumulado", alineado="derecha")
        ], anchoColumnas=25, datos=[])

        acumulado = 0
        for i in range(self.totalObservaciones):
            dato = self.datos[i]
            diferencia = self.__formatNumber(dato - media)
            cuadrado = self.__formatNumber(diferencia**2)
            acumulado += self.__formatNumber(cuadrado)

            tabla.agregarFila(datos=[
                f"{dato}",
                f"{dato} - {media} = {diferencia}",
                f"({diferencia})^2 = {cuadrado}",
                f"{self.__formatNumber(acumulado)}"
            ])
        varianza = self.__formatNumber((acumulado / self.totalObservaciones))
        if mostrar:
            tabla.dibujar()
            print(f"Sumatoria: {self.__formatNumber(acumulado)}")
            print(f"Varianza: {varianza}")
        return varianza

    def desviacionEstandar(self, mostrar: bool = True) -> float:
        varianza = self.varianza(mostrar=mostrar)
        desviacionEstandar = self.__formatNumber(sqrt(varianza))
        if mostrar:
            print("Desviación estándar: ")
            print(f"√{varianza} = {desviacionEstandar}")
        return desviacionEstandar

