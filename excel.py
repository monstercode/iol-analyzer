import xlsxwriter

class ExcelWriter:
    def __init__(self, filename):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.bold = self.workbook.add_format({'bold': True})
        self.worksheet = self.workbook.add_worksheet()
        self.init_column = 1
        self.init_row = 1
        self.current_row = 1
        self.current_col = 1


    def write_contents(self, columns, rows, total=False):

        column_name_position = {}
        #worksheet.set_column('A:A', 20)
        for i in range(len(columns)):
            column_name_position[columns[i]] = i + self.init_column
            self.worksheet.write(self.current_row, self.current_col, columns[i].capitalize())
            self.current_col += 1

        self.current_col = self.init_column
        self.current_row +=1
        for row in rows:
            for i in range(len(columns)):
                col_name = columns[i]
                if col_name in row:
                    self.worksheet.write(self.current_row, column_name_position[col_name], row[col_name])
            self.current_row +=1 

        if total:
            for col_name in total: 
                self.worksheet.write(self.current_row, column_name_position[col_name], total[col_name], self.bold)
            self.current_row +=1 

        self.current_row +=1
        self.current_col = self.init_column

    def save(self):
        self.workbook.close()
