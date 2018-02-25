""" Extracting and analysing data from UNB results PAS """
import PyPDF2
import pandas as pd
import re


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
    unused = list()
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
            else:
                unused.append(t)
    return df, unused


def into_float(df):
    # Force into float
    df['n1'] = df['n1'].astype('float')
    df['n_text'] = pd.to_numeric(df['n_text'], errors='coerce')
    return df


def treating_leftovers(u):
    us = [item for sublist in u for item in sublist]
    u2 = us[9:-46]
    u2 = fixing_data(u2)
    df = pd.DataFrame(columns=['register', 'name', 'n1', 'n_text'])
    ind = 0
    for i in range(0, len(u2), 4):
        for each in ['name', 'n1', 'n_text', 'register']:
            if each == 'register':
                ind += 1
            try:
                df.loc[ind, each] = u2[i]
                i += 1
            except IndexError:
                return df
    return df


def fixing_data(lt):
    # Joining candidates' names separated by page breaks
    a = list()
    skip = False
    for i in range(len(lt)):
        if skip:
            skip = False
            continue
        else:
            if re.search('[a-zA-Z]', lt[i]) and re.search('[a-zA-Z]', lt[i + 1]):
                a.append(lt[i] + lt[i + 1])
                skip = True
            else:
                a.append(lt[i])

    # Further cleaning. Extracting empty spaces
    b = list()
    for each in a:
        if each != '':
            b.append(each)
    return b


if __name__ == "__main__":
    # File to read
    pdf_file = open('redacao.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    res = reading(read_pdf)
    r2 = data_into_lists(res)
    # Manipulate DataFrame
    r3, unused = into_database(r2)
    # Treating broken links due to page turns in PDF
    df2 = treating_leftovers(unused)
    # df2.to_csv('unused.csv', sep=';')

    # Manually treat df2
    df2 = pd.read_csv('unused.csv', sep=';')
    res = pd.concat([r3, df2])
    # Save as CSV
    res.to_csv('redacao_pas.csv', sep=';')

