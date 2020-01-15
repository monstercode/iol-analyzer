from excel import ExcelWriter

class IOLAnalyzer:
    def __init__(self, movimientos):
        self.movimientos = movimientos

    def agrupar_por_activo(self,movimientos):
        movimientos_por_activo = {}
        for mov in movimientos:
            if mov["activo"] not in movimientos_por_activo:
                movimientos_por_activo[mov["activo"]] = []
            movimientos_por_activo[mov["activo"]].append(mov)

        return movimientos_por_activo

    def totalizar_movimientos(self, movimientos):
        """Sumariza el total de los movimientos. No agrupa por activo, ya debe de estar agrupado """
        total = {"monto (ARS)":0, "monto (USD)":0, "cantidad":0}
        for mov in movimientos:
            for key in total:
                if key in mov:
                    total[key] += mov[key]

        return total

    def write_to_file(self):
        file = ExcelWriter("sumarizado.xls")

        columns = ["fecha", "activo", "accion", "moneda", "precio", "cantidad", "monto (ARS)", "monto (USD)"]
        for tipo_activo in ["ACCIONES", "BONOS", "FCI", "LETRAS"]:
            movimientos_por_activo = self.agrupar_por_activo(self.movimientos[tipo_activo])

            for activo in movimientos_por_activo:
                file.write_contents(columns=columns, rows=movimientos_por_activo[activo], total=self.totalizar_movimientos(movimientos_por_activo[activo]))
            

        # bonos = self.agrupar_por_activo(self.movimientos["BONOS"])
        # columns = ["fecha", "activo", "accion", "precio", "cantidad", "monto (ARS)", "monto (USD)"]
        # for bono in bonos:
        #     file.write_contents(columns=columns, rows=bonos[bono], total=self.totalizar_movimientos(bonos[bono]))

        # fcis = self.agrupar_por_activo(self.movimientos["FCI"])
        # for fci in fcis:
        #     file.write_contents(columns=columns, rows=fcis[fci], total=self.totalizar_movimientos(fcis[fci]))
        file.save()

    # def write_acciones():
    #     movimientos_por_accion = {}
    #     for mov in self.movimientos["ACCIONES"]:
    #         if mov["activo"] not in movimientos_por_accion:
    #             movimientos_por_accion[mov["activo"]] = []
    #         movimientos_por_accion[mov["activo"]].append(mov)

    #     total_por_accion = {}
    #     total = {}
    #     for accion in movimientos_por_accion:
    #         if accion not in total_por_accion:
    #             total_por_accion = {}

    #         for movimiento in movimientos_por_accion[accion]:
    #             total_por_accion["monto"] += movimiento["monto"]
    #             print(f" {movimiento['fecha']} {movimiento['accion']} {movimiento['monto']}")

    #         total += total_accion
    #         print(f" Total {accion}: {total_accion}")
    #     print(f"TOTAL: {total}")



    # def get_totals(self):
    #     totals = {}
    #     for tipo in self.movimientos:
    #         totals[tipo] = {"ARS":0, "USD":0, "cantidad": 0}
    #         movs = self.movimientos[tipo]

    #         for movimiento in movs:
    #             if tipo in ["ACCIONES", "BONOS"]:
    #                 if not movimiento["activo"] in totals[tipo]:
    #                     totals[tipo][movimiento["activo"]] = 0
    #                 totals[tipo][movimiento["activo"]] += movimiento["cantidad"]
    #                 if totals[tipo][movimiento["activo"]] == 0:
    #                     del totals[tipo][movimiento["activo"]]
    #             totals[tipo][movimiento["moneda"]] += movimiento["monto"]


    #     for tipo in totals:
    #         print(f"\n ==== {tipo} ==== ")
    #         print(totals[tipo])

    # def get_resume(self):
    #     self.get_resumen_acciones()
    #     print("\n" +"="*150 + "\n")
    #     self.get_resumen_bonos()
    #     print("\n" +"="*150 + "\n")
    #     self.get_resumen_movimientos_fondos()
    #     print("\n" +"="*150 + "\n")
    #     self.get_resumen_compra_venta_divisa()
    #     print("\n" +"="*150 + "\n")
    #     self.get_resumen_letras()
    #     print("\n" +"="*150 + "\n")
    #     self.get_resumen_fci()

    # def get_resumen_acciones(self):
    #     movimientos_por_accion = {}
    #     for mov in self.movimientos["ACCIONES"]:
    #         if mov["activo"] not in movimientos_por_accion:
    #             movimientos_por_accion[mov["activo"]] = []
    #         movimientos_por_accion[mov["activo"]].append(mov)

    #     total = 0
    #     for accion in movimientos_por_accion:
    #         print(f" {accion}: ==================")
    #         total_accion = 0

    #         for movimiento in movimientos_por_accion[accion]:
    #             total_accion += movimiento["monto"]
    #             print(f" {movimiento['fecha']} {movimiento['accion']} {movimiento['monto']}")

    #         total += total_accion
    #         print(f" Total {accion}: {total_accion}")
    #     print(f"TOTAL: {total}")

    # def get_resumen_bonos(self):
    #     movimientos_por_bono = {}
    #     for mov in self.movimientos["ACCIONES"]:
    #         if mov["activo"] not in movimientos_por_bono:
    #             movimientos_por_bono[mov["activo"]] = []
    #         movimientos_por_bono[mov["activo"]].append(mov)


    #     total = {
    #         "ARS": 0,
    #         "USD": 0
    #     }
    #     for bono in movimientos_por_bono:
    #         print(f" {bono}: ==================")
    #         total_bono = {"ARS": 0, "USD": 0}

    #         for movimiento in movimientos_por_bono[bono]:
    #             total_bono[movimiento["moneda"]] += movimiento["monto"]
    #             print(f" {movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto']:>15.2f} ({movimiento['cantidad']}) ")

    #         total["ARS"] += total_bono["ARS"]
    #         total["USD"] += total_bono["USD"]
    #         print(f" Total {bono}: ARS {total_bono['ARS']} | USD {total_bono['USD']} ")
    #     print(f"TOTAL: {total}")

    # def get_resumen_compra_venta_divisa(self):
    #     for movimiento in self.movimientos["DIVISAS"]:
    #         if movimiento["moneda"] == "ARS":
    #             continue
    #         print(f"{movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto']:15.2f}  (ARS {movimiento['precio']})")

    # def get_resumen_letras(self):
    #     total = { "ARS": 0, "USD": 0}
    #     for movimiento in self.movimientos["LETRAS"]:
    #         print(f"{movimiento['fecha']} {movimiento['accion']:>25} {movimiento['activo']:>10} {movimiento['moneda']} {movimiento['monto']:15.2f}")
    #         total[movimiento['moneda']] += movimiento['monto']
    #     print(f"ARS: {total['ARS']} | USD: {total['USD']} ")

    def get_resumen_movimientos_fondos(self):
        total = {
            "ARS": 0,
            "USD": 0,
        }
        for movimiento in self.movimientos["MOV_FONDOS"]:
            print(f" {movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto (ARS)']:>15.2f} {movimiento['monto (USD)']:>15.2f}")
            if "DEPOSITO" in movimiento['accion']:
                total["ARS"] -= movimiento['monto (ARS)']
                total["USD"] -= movimiento['monto (USD)']
            elif "EXTRACCION" in movimiento['accion']:
                total["ARS"] += movimiento['monto (ARS)']
                total["USD"] += movimiento['monto (USD)']
        print(f"ARS: {total['ARS']} | USD: {total['USD']} ")

    # def get_resumen_fci(self):
    #     total = { "ARS": 0, "USD": 0}
    #     for movimiento in self.movimientos["FCI"]:
    #         print(f"{movimiento['fecha']} {movimiento['accion']:>25} {movimiento['activo']:>10} {movimiento['moneda']} {movimiento['monto']:15.2f}")
    #         total[movimiento['moneda']] += movimiento['monto']
    #     print(f"ARS: {total['ARS']:15.2f} | USD: {total['USD']:15.2f} ")

