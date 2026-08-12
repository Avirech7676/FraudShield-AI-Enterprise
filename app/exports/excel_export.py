from openpyxl import Workbook


class ExcelExporter:

    @staticmethod
    def export(df, filename):

        wb = Workbook()

        ws = wb.active

        ws.append(list(df.columns))

        for row in df.values.tolist():

            ws.append(row)

        wb.save(filename)
