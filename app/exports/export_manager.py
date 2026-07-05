from app.exports.pdf_export import PDFExporter
from app.exports.excel_export import ExcelExporter
from app.exports.csv_export import CSVExporter
from app.exports.word_export import WordExporter


class ExportManager:

    @staticmethod
    def export_pdf(data, filename):

        PDFExporter.export(data, filename)

    @staticmethod
    def export_excel(df, filename):

        ExcelExporter.export(df, filename)

    @staticmethod
    def export_csv(df, filename):

        CSVExporter.export(df, filename)

    @staticmethod
    def export_word(text, filename):

        WordExporter.export(text, filename)