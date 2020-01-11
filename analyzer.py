
class IOLAnalyzer:
    def __init__(self, movimientos_por_accion, movimientos_por_bono, movimientos_letras, movimientos_fondos, movimientos_compra_venta_divisas):
        self.movimientos_por_accion = movimientos_por_accion
        self.movimientos_por_bono = movimientos_por_bono
        self.movimientos_letras = movimientos_letras
        self.movimientos_fondos = movimientos_fondos
        self.movimientos_compra_venta_divisas = movimientos_compra_venta_divisas

    def get_resume(self):
        self.get_resumen_acciones()
        print("\n" +"="*150 + "\n")
        self.get_resumen_bonos()
        print("\n" +"="*150 + "\n")
        self.get_resumen_movimientos_fondos()
        print("\n" +"="*150 + "\n")
        self.get_resumen_compra_venta_divisa()
        print("\n" +"="*150 + "\n")
        self.get_resumen_letras()

    def get_resumen_acciones(self):
        total = 0
        for accion in self.movimientos_por_accion:
            print(f" {accion}: ==================")
            total_accion = 0

            for movimiento in self.movimientos_por_accion[accion]:
                total_accion += movimiento["monto"]
                print(f" {movimiento['fecha']} {movimiento['accion']} {movimiento['monto']}")

            total += total_accion
            print(f" Total {accion}: {total_accion}")
        print(f"TOTAL: {total}")

    def get_resumen_bonos(self):
        total = {
            "ARS": 0,
            "USD": 0
        }
        for bono in self.movimientos_por_bono:
            print(f" {bono}: ==================")
            total_bono = {"ARS": 0, "USD": 0}

            for movimiento in self.movimientos_por_bono[bono]:
                total_bono[movimiento["moneda"]] += movimiento["monto"]
                print(f" {movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto']:>15.2f} ({movimiento['cantidad']}) ")

            total["ARS"] += total_bono["ARS"]
            total["USD"] += total_bono["USD"]
            print(f" Total {bono}: ARS {total_bono['ARS']} | USD {total_bono['USD']} ")
        print(f"TOTAL: {total}")

    def get_resumen_compra_venta_divisa(self):
        for movimiento in self.movimientos_compra_venta_divisas:
            if movimiento["moneda"] == "ARS":
                continue
            print(f"{movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto']:15.2f}  (ARS {movimiento['precio']})")

    def get_resumen_letras(self):
        total = { "ARS": 0, "USD": 0}
        for movimiento in self.movimientos_letras:
            print(f"{movimiento['fecha']} {movimiento['accion']:>25} {movimiento['activo']:>10} {movimiento['moneda']} {movimiento['monto']:15.2f}")
            total[movimiento['moneda']] += movimiento['monto']
        print(f"ARS: {total['ARS']} | USD: {total['USD']} ")

    def get_resumen_movimientos_fondos(self):
        total = {
            "ARS": 0,
            "USD": 0,
        }
        for movimiento in self.movimientos_fondos:
            print(f" {movimiento['fecha']} {movimiento['accion']:>25} {movimiento['moneda']} {movimiento['monto']:>15.2f}")
            if "DEPOSITO" in movimiento['accion']:
                total[movimiento['moneda']] -= movimiento['monto']
            elif "EXTRACCION" in movimiento['accion']:
                total[movimiento['moneda']] += movimiento['monto']
        print(f"ARS: {total['ARS']} | USD: {total['USD']} ")