class Pensionado():
    def __init__(self, nombres, apellidos, expectativa, valorUF, opc):
        self.nombre = nombres
        self.apellidos = apellidos
        self.expectativa = expectativa 
        self.valorUF = valorUF
        self.opc = opc

    def calcular_opciones(self, opciones):
        listaPensiones = []

        for opcion in opciones:

            if opcion["monto"] is None or opcion["monto"] <= 0:
                listaPensiones.append(0)
                continue

            total = 0

            if opcion["tipo"] == "fija":
                total = opcion["monto"] * self.expectativa

            elif opcion["tipo"] == "variable":
                montoBase = opcion["monto"]
                aumento = opcion.get("aumento", 0)
                mesesAumento = opcion.get("meses", 0)

                for mes in range(1, self.expectativa + 1):
                    if mes <= mesesAumento:
                        monto_mes = montoBase * ((1 + aumento/100) ** mes)
                    else:
                        monto_mes = montoBase

                    total += monto_mes

            else:
                total = 0

            listaPensiones.append(total)

        return listaPensiones

    def comparar(self, listaPensiones):
        if not listaPensiones:
            return None
        
        mejor_valor = max(listaPensiones)
        mejor_indice = listaPensiones.index(mejor_valor)

        return {
            "mejor_opcion": mejor_indice,
            "mejor_valor": mejor_valor,
            "todas": listaPensiones
        }