import pandas as pd
import re

class IOLFileParser:

    NUM_MOVIMIENTO      = 'Nro. de Mov.'
    NUM_BOLETO          = 'Nro. de Boleto'
    TIPO_MOVIMIENTO     = 'Tipo Mov.'
    FECHA_CONCERTADO    = 'Concert.'
    FECHA_LIQUIDACION   = 'Liquid.'
    ESTADO              = 'Est'
    CANTIDAD_TITULOS    = 'Cant. titulos'
    PRECIO              = 'Precio'
    COMISION            = 'Comis.'
    IVA_COMISION        = 'Iva Com.'
    OTROS_IMPUESTOS     = 'Otros Imp.'
    MONTO               = 'Monto'
    OBSERVACIONES       = 'Observaciones'
    TIPO_CUENTA         = 'Tipo Cuenta'

    MONEDA = {
        "Inversion Argentina Pesos": "ARS",
        "Inversion Argentina Dolares": "USD",
    }

    BONOS = ["AY24","AC17","AF20","A2M2","TC20","PARA","DICA","TJ20","AO20","PARY","PR15","AY24D","TO21","AA37","TC21","AL36","AM20","AA25","DICY","PR13","A2E2","PBA25","TO23","BDC28","DICP","DICAD","A2E7","PBY22","AO20D","AC17D","DIA0","AF20D","AA21D","AE48D","DICYD","AA22","TVPP","AA37D","PARYD","PAY0","PARP","YPCUO","CO26","TVPA","PUM21","BDC20","AA25D","A2E8","BPLD","PMJ21","A2E2D","A2E7D","DIP0","CO26D","PARAD","TVPY","TC23","DIA0D","PAA0","TO26","BPLDD","CUAP","PAA0D","TVPE","A2E3","A2E3D","A2E8D","A2J9","A2J9D","AA21","AA26","AA26D","AA46","AA46D","AE48","AMX9","BBN19","BD2C9","BDC19","BDC22","BP21","BP28","BPLE","BPMD","BPMDD","BPME","CEDI","CH24D","CHSG1","CHSG2","CSFQO","DICE","DIY0","DIY0D","FORM3","IRC1O","NO20","NRH2","ONCTG_6","PAP0","PAY0D","PBD19","PBF23","PBJ21","PBJ27","PBM24","PF23D","PMY24","PUL26","PUO19","RHC20","RPC4O","SA24D","SARH","SUC1P","TC25P","TFU27","TN20","TVPYD","TVY0","VSC1O","VSC2O"]
    ACCIONES = ["AGRO","ALUA","APBR","AUSO","BBAR","BHIP","BMA","BOLT","BPAT","BRIO","BYMA","CADO","CAPU","CAPX","CARC","CECO2","CELU","CEPU","CGPA2","COLO","COME","CRES","CTIO","CVH","DGCU2","DYCA","EDN","ESME","FERR","FIPL","GAMI","GARO","GBAN","GCLA","GGAL","GRIM","HARG","HAVA","INAG","INDU","INTR","INVJ","IRCP","IRSA","LEDE","LOMA","LONG","MERA","METR","MIRG","MOLA","MOLI","MORI","OEST","PAMP","PATA","PATY","PGR","POLL","RICH","RIGO","ROSE","SAMI","SEMI","SUPV","TECO2","TGLT","TGNO4","TGSU2","TRAN","TXAR","VALO","YPFD"]
    LETRAS = ["LTDL9-3L8", "UL9D"]
    FONDOS = ["CNXPOPA"]

    TIPOS_MOVIMIENTOS = [
        {
            "tipo": "COMPRA_ACTIVO",
            "regex": r"Compra\((?P<activo>.+)\)",
        },
        {
            "tipo": "VENTA_ACTIVO",
            "regex": r"Venta\((?P<activo>.+)\)",
        },
        {
            "tipo": "PAGO_RENTA",
            "regex": r"Pago de Renta\((?P<activo>.+)\)",
        },
        {
            "tipo": "PAGO_AMORTIZACION",
            "regex": r"Pago de Amortización\((?P<activo>.+)\)",
        },
        {
            "tipo": "SUSCRIPCION_FCI",
            "regex": r"Suscripción FCI\((?P<activo>.+)\)",
        },
        {
            "tipo": "RESCATE_FCI",
            "regex": r"Rescate FCI\((?P<activo>.+)\)",
        },
        {
            "tipo": "SUSCRIPCION_LETRA",
            "regex": r"Suscripción Primaria\((?P<activo>.+)\)",
        },
        {
            "tipo": "DEBITO_PRODUCTO",
            "regex": r"Débito - Producto",
            # pago por mantenimiento cuenta
        },
        {
            "tipo": "COMPRA_DOLAR",
            "regex": r"Compra de Dólares",
        },
        {
            "tipo": "DEPOSITO_FONDOS",
            "regex": r"Depósito de Fondos",
        },
        {
            "tipo": "EXTRACCION_FONDOS",
            "regex": r"Extracción de Fondos",
            # pago por mantenimiento cuenta
        },
    ]

    def __init__(self, filename):
        self.xls = pd.read_html(filename, decimal=",", thousands='.', parse_dates=True)[0]
        self.movimientos_por_accion = {}
        self.movimientos_por_bono = {}
        self.movimientos_letras = []
        self.movimientos_fondos = []
        self.movimientos_compra_venta_divisas = []

    def parse_file(self):
        for idx in reversed(range(0, len(self.xls))):
            matched = False
            if self.xls[self.ESTADO][idx] == "Cancelada":
                continue

            for movimiento in self.TIPOS_MOVIMIENTOS:
                
                search = re.search(movimiento["regex"], self.xls[self.TIPO_MOVIMIENTO][idx])
                if search is not None:
                    matched = True
                    tipo_movimiento = movimiento["tipo"]
                    try:
                        activo = search.group('activo')
                        activo = activo.replace(" US$", "")
                        # Chequear bonos duales, unificar en version no D
                        if activo[-1:] == "D" and activo[:-1] in self.BONOS:
                            activo = activo[:-1]
                    except IndexError:
                        activo = ""
                    print(f"{tipo_movimiento} {activo}")

                    self.parse_row(self.xls.iloc[idx], tipo_movimiento, activo)

    def get_parsed_data(self):
        return {
            "movimientos_por_accion": self.movimientos_por_accion,
            "movimientos_por_bono": self.movimientos_por_bono,
            "movimientos_letras": self.movimientos_letras,
            "movimientos_fondos": self.movimientos_fondos,
            "movimientos_compra_venta_divisas": self.movimientos_compra_venta_divisas,
        }

    def get_moneda(self, row):
        return self.MONEDA[row[self.TIPO_CUENTA]]

    def parse_row(self, row, tipo_movimiento, activo):
        if activo in self.BONOS:
            self.parse_bono(row, tipo_movimiento, activo)
        elif activo in self.ACCIONES:
            self.parse_accion(row, tipo_movimiento, activo)
        elif activo in self.LETRAS:
            self.parse_letra(row, tipo_movimiento, activo)
        elif activo in self.FONDOS:
            self.parse_fondo(row, tipo_movimiento, activo)
        elif tipo_movimiento in ["DEPOSITO_FONDOS", "EXTRACCION_FONDOS"]:
            self.parse_movimiento_fondos(row, tipo_movimiento)
        elif tipo_movimiento in ["COMPRA_DOLAR", "VENTA_DOLAR"]:
            self.parse_compra_venta_divisa(row, tipo_movimiento)

    def parse_bono(self, row, tipo_movimiento, activo):
        if activo not in self.movimientos_por_bono:
            self.movimientos_por_bono[activo] = []
                
        if row[self.CANTIDAD_TITULOS] == 0:
            self.movimientos_por_bono[activo].append(
                {
                    "accion": tipo_movimiento,
                    "monto":  float(row[self.MONTO]),
                    "fecha": row[self.FECHA_LIQUIDACION],
                    "cantidad": row[self.CANTIDAD_TITULOS],
                    "moneda": self.get_moneda(row)
                }
            )
        
        else:
            if self.get_moneda(row) == "USD":
                self.movimientos_por_bono[activo].append(
                    {
                        "accion": f"{tipo_movimiento}_COMISION",
                        "monto": float(row[self.MONTO]),
                        "fecha": row[self.FECHA_LIQUIDACION],
                        "cantidad": row[self.CANTIDAD_TITULOS],
                        "moneda": "ARS",
                    }
                )

            self.movimientos_por_bono[activo].append(
                {
                    "accion": tipo_movimiento,
                    "monto": row[self.CANTIDAD_TITULOS] * float(row[self.PRECIO])/100 * (-1 if "COMPRA" in tipo_movimiento else 1),
                    "fecha": row[self.FECHA_LIQUIDACION],
                    "cantidad": row[self.CANTIDAD_TITULOS],
                    "moneda": self.get_moneda(row)
                }
            )
                

    def parse_accion(self, row, tipo_movimiento, activo):
        if activo not in self.movimientos_por_accion:
            self.movimientos_por_accion[activo] = []
                
        self.movimientos_por_accion[activo].append(
            {
                "accion": tipo_movimiento,
                "monto": float(row[self.MONTO]),
                "fecha": row[self.FECHA_LIQUIDACION],
                "cantidad": row[self.CANTIDAD_TITULOS],
                "moneda": self.get_moneda(row),
            }
            
        )

    def parse_letra(self, row, tipo_movimiento, activo):
        self.movimientos_letras.append(
            {
                "accion": tipo_movimiento,
                "moneda": self.get_moneda(row),
                "monto": row[self.MONTO],
                "fecha": row[self.FECHA_LIQUIDACION],
                "numero_movimiento": row[self.NUM_MOVIMIENTO],
                "precio": row[self.PRECIO],
                "activo": activo,
            }
        )

    def parse_fondo(self, row, tipo_movimiento, activo):
        pass

    def parse_compra_venta_divisa(self, row, tipo_movimiento):
        self.movimientos_compra_venta_divisas.append(
            {
                "accion": tipo_movimiento,
                "moneda": self.get_moneda(row),
                "monto": row[self.MONTO],
                "fecha": row[self.FECHA_LIQUIDACION],
                "numero_movimiento": row[self.NUM_MOVIMIENTO],
                "precio": row[self.PRECIO],
            }
        )

    def parse_movimiento_fondos(self, row, tipo_movimiento):
        self.movimientos_fondos.append(
            {
                "accion": tipo_movimiento,
                "moneda": self.get_moneda(row),
                "monto": abs(row[self.MONTO]),
                "fecha": row[self.FECHA_LIQUIDACION],
            }
        )

