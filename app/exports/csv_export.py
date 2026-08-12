class CSVExporter:

    @staticmethod
    def export(df, filename):

        df.to_csv(

            filename,

            index=False

        )
