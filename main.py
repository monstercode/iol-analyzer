from parser import IOLFileParser
from analyzer import IOLAnalyzer

parser = IOLFileParser(filename="MovimientosHistoricos.xls")

parser.parse_file()

analyzer = IOLAnalyzer(parser.get_movimientos())
analyzer.get_resumen_movimientos_fondos()

#analyzer.get_totals()

analyzer.write_to_file()