# Script to build the Audubon Core term list page using Markdown.
# Steve Baskauf 2018-06-12
# This script merges static Markdown header and footer documents with term information tables (in Markdown) generated from data in the rs.tdwg.org repo from the TDWG Github site

# Note: this script calls a function from http_library.py, which requires importing the requests, csv, and json modules
import http_library

# constants
headerFileName = 'termlist-header.md'
footerFileName = 'termlist-footer.md'
outFileName = 'termlist.md'
namespaceAbbreviation = 'ac:'
namespaceUri = 'http://rs.tdwg.org/ac/terms/'

# retrieve term metadata from Github
dataUrl = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/split_ac_terms/audubon/audubon.csv'
accept = 'csv'
param1 = ','  # for csv use delimiter
table = http_library.retrieveData(dataUrl, accept, param1)
header = table[0]

# determine which column contains the specified metadata field
for column in range(len(header)):
    if header[column] == 'term_localName':
        localNameColumn = column
    if header[column] == 'label':
        labelColumn = column
    if header[column] == 'tdwgutility_layer':
        layerColumn = column
    if header[column] == 'tdwgutility_required':
        requiredColumn = column
    if header[column] == 'tdwgutility_repeatable':
        repeatableColumn = column
    if header[column] == 'rdfs_comment':
        definitionColumn = column
    if header[column] == 'dcterms_description':
        notesColumn = column

# generate the Markdown for the terms table
text = ''
text += '| property | value |\n'
text += '|----------|-------|\n'
for row in range(1,len(table)):    #skip the header row
    text += '| **Term Name:** | **' + namespaceAbbreviation + table[row][localNameColumn] + '** |\n'
    text += '| Normative URI: | ' + namespaceUri + table[row][localNameColumn] + ' |\n'
    text += '| Label: | ' + table[row][labelColumn] + ' |\n'
    text += '| | **Layer:** ' + table[row][layerColumn] + ' -- **Required:** ' + table[row][requiredColumn] + ' -- **Repeatable:** ' + table[row][repeatableColumn] + ' |\n'
    text += '| Definition: | ' + table[row][definitionColumn] + ' |\n'
    if table[row][notesColumn] != '':
        text += '| Notes: | ' + table[row][notesColumn] + ' |\n'
    text += '| | |\n'
text += '| | |\n'

# read in header and footer, merge with terms table, and output
headerObject = open(headerFileName, 'rt')
header = headerObject.read()
headerObject.close()

footerObject = open(footerFileName, 'rt')
footer = footerObject.read()
footerObject.close()

outputObject = open(outFileName, 'wt')
outputObject.write(header + text + footer)
outputObject.close()