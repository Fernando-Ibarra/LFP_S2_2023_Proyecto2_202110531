from models.Error import errorsList

titles = [
    "Tipo",
    "Lexema",
    "Fila",
    "Columna",
]

class HtmlError():
    
    def __init__(self) -> None:
        pass

    def make_head(self):
        head = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset='utf-8'>
                <meta name='viewport' content='width=device-width, initial-scale=1'>
                <title>Reporte Proyecto 2 | Errores </title>
                <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN' crossorigin='anonymous'>
            </head>
        """
        return head

    def make_footer(self):
        footer = f"""
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
            </body>
        </html>
        """
        return footer
    
    
    def make_body(self):
        body = f"""
        <body>
            <p class="fs-1">Errores</p>
            <div class="container text-center">
                <table class='table table-bordered border-primary'>
                <thead>
                    <tr>
        """ 
        for title in titles:
            body += f"<th scope='col'>{ title }</th>"
        """
                    </tr>
                </thead>
                <tbody>
        """
        for error in errorsList:
            body += "<tr>"
            body += f"<td>{ error.tipo }</td>"
            body += f"<td>{ error.lexema }</td>"
            body += f"<td>{ error.row }</td>"
            body += f"<td>{ error.column }</td>"
            body += "</tr>"
        """
                </tbody>
                </table>
            </div>
        """
        return body

    def make_html(self):
        html = f"{self.make_head()}{self.make_body()}{self.make_footer()}"
        return html
