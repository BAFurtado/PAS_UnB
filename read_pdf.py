""" Extracting and analysing data from UNB results PAS """
import PyPDF2
import pandas as pd


def reading(pdf_doc):
    # Extract text from PDF and outputs results as a list
    outputs = list()
    for p in range(pdf_doc.getNumPages()):
        page = pdf_doc.getPage(p)
        outputs.append(page.extractText())
    return outputs


def data_into_lists(l):
    # Process the list to prepare target the necessary info
    out = list()
    for each in range(len(l)):
        t = l[each].strip()
        out.append(t.split('/'))
    return out


def into_database(ls):
    # Extract groups of results as lists and dumps onto a DataFrame
    # Create DataFrame
    df = pd.DataFrame(columns=['register', 'name', 'n1', 'n_text'])
    ind = 0
    # Go through list in lists of lists
    for i in ls:
        for j in i:
            # Mitigates extra characters
            t = j.strip('\n').replace('\n', '')
            # Use comma to separate target info
            t = t.split(',')
            # Restrict data to correct 4-group information
            # Registration number, candidates name, first grade, text grade
            if len(t) == 4:
                # Dump into DataFrame
                df.loc[ind] = t
                ind += 1
    # Force into float
    df['n1'] = df['n1'].astype('float')
    df['n_text'] = pd.to_numeric(df['n_text'], errors='coerce')
    return df


if __name__ == "__main__":
    # File to read
    pdf_file = open('redacao.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    res = reading(read_pdf)
    r2 = data_into_lists(res)
    # Manipulate DataFrame
    r3 = into_database(r2)

    # Save as CSV
    r3.to_csv('redacao_pas.csv')

