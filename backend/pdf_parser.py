import pdfplumber


def extract_contacts_from_pdf(pdf_path):

    contacts = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if table:

                for row in table[1:]:

                    try:

                        name = row[1]
                        email = row[2]
                        title = row[3]
                        company = row[4]

                        contacts.append({
                            "name": name,
                            "email": email,
                            "title": title,
                            "company": company
                        })

                    except:
                        pass

    return contacts