def msg_body_for_yad2_info(data: list[dict]) -> str:
    # TODO- Will need to replace raw strings to dedicated html and css
    """
    This is the body of the mail intended for yad2 scraping. It accepts a list of dictionaries that contain all
    relevant data

    :param data: List of dictionaries with relevant keys
    :return: the body as a string object
    """

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
        f"<tr><td>{item['title']}</td>"
        f"<td>{item['description']}</td>"
        f"<td>{item['price_element']}</td>"
        f"<td>{item['rooms']}</td>"
        f"<td>{item['area']}</td>"
        f"<td>{item['merchant']}</td></tr>"
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
