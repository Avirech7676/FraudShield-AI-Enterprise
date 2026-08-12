import zipfile


class ZIPExporter:

    @staticmethod
    def create(files, output):

        with zipfile.ZipFile(

            output,

            "w"

        ) as zipf:

            for file in files:

                zipf.write(file)
