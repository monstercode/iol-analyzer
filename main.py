from parser import IOLFileParser
from analyzer import IOLAnalyzer

parser = IOLFileParser(filename="MovimientosHistoricos.xls")

parser.parse_file()

analyzer = IOLAnalyzer(**parser.get_parsed_data())
analyzer.get_resume()