def prep_mail_for_yad2_information(data: list[dict]) -> str:
    # TODO- Will need to replace raw strings to dedicated html and css

    table_html = f"""
        <table style="width:100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: lightgray;">
                    <th>כותרת</th>
                    <th>פירוט</th>
                    <th>מחיר</th>
                    <th>מס' חדרים</th>
                    <th>שטח הדירה</th>
                    <th>פרטי מוכר</th>
                </tr>
            </thead>
            <tbody>
                {"".join([
        f"<tr><td>{item['title']}</td><td>{item['description']}</td><td>{item['price_element']}</td><td>{item['rooms']}</td><td>{item['area']}</td><td>{item['merchant']}</td></tr>"
        for item in data
    ])}
            </tbody>
        </table>
        """

    body = f"""
           <html>
           <head>
               <style>
                   body {{ font-family: Arial, sans-serif; }}
                   h1, h2 {{ text-align: center; }}
                   table {{ margin: 0 auto; }}
                   th, td {{ padding: 10px; border: 1px solid black; }}
               </style>
               <h1>פירוט כל הדירות שנמצאו</h1>
           </head>
           <body>
               <h2>Data:</h2>
               <hr />
               {table_html}
               <hr />
           </body>
           </html>
           """
    return body
