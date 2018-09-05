import pandas as pd
import argparse, sys

#Valid arguments
options = list('AaJjBbKkCcLlDdMmEeNnFfOoGgPpHhQqIiRrSsTtUuVvWwYyZz9876543210*X+#$&/=?')

if len(sys.argv) > 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inFile', help='Path to input file', default='Data Grab for DMAP.txt')
    parser.add_argument('-o', '--outFile', help="Path for output file", default='DMAP OUT.txt')
    parser.add_argument('-d', '--date', type=int, help='Cut off date', default=1960)
    parser.add_argument('--before', choices=options, help='Symbol to display in DMAP for grid references before cut off date', default='G')
    parser.add_argument('--after', choices=options, help='Symbol to display in DMAP for grid references after cut off date', default='A')
    parser.add_argument('--both', choices=options, help='Symbol to display in DMAP for grid references both sides of cut off date', default='D')
    args = parser.parse_args()

    if args.inFile:
        inFile = args.inFile
    if args.outFile:
        outFile = args.outFile
    if args.date:
        cutDate = args.date
    if args.before:
        beforeSymbol = args.before
    if args.after:
        afterSymbol = args.after
    if args.both:
        bothSymbol = args.both
else:
    #Get user inputs, default options are defined
    inFile = str(input('Enter input file path: ')) or 'Data Grab for DMAP.txt'
    outFile = str(input('Enter output file path: ')) or 'DMAP OUT.txt'
    cutDate = input('Enter the cut off date: ') or 1960
    beforeSymbol = str(input('Enter symbol code for before date data: ')) or 'G'
    afterSymbol = str(input('Enter symbol code for after date data: ')) or 'A'
    bothSymbol = str(input('Enter symbol code for both date data: ')) or 'D'


#Takes row as input and returns Grid reference with correct DMAP symbol appended
def f(row):
    index = row.name
    if options[index] == -1:
        return row['Gr'] + ' ' + beforeSymbol
    if options[index] == 0:
        return row['Gr'] + ' ' + afterSymbol
    if options[index] == 1:
        return row['Gr'] + ' ' + bothSymbol


#Convert cutDate to int, needed if default not used
cutDate = int(cutDate)

#Read in data
df = pd.read_csv(inFile, names=['Sp', 'Gr', 'Year'])

#Drop any nan and na rows (Grid ref not present)
df = df.dropna(axis=0, how='any')

#Remove any spaces and non-alphanumeric characteres from Grid ref
df['Gr'] = df['Gr'].str.replace('\s+', '')
df['Gr'] = df['Gr'].str.replace('[^\w\s]','')

#print(df.head(7))
#Remove duplicates - pointless processing
df = df.drop_duplicates()

#Reindex dataframe, drop old index
df.reset_index(drop=True, inplace=True)
#print(df.head(7))


offset = 0 #Index of first element in group
rows = [] #Indexs of rows to output
options = [] #Codes for before after or both, indecis correspond in rows and options

#Iterate groups
for name, group in df.groupby(['Sp', 'Gr'], sort = False):
    #print(name)
    #print(group)

    beforeRow = -1
    afterRow = -1

    groupSize = len(group)

    BEFORE = False
    AFTER = False
    BOTH = False

    #Iterate rows in group
    for x in range(groupSize):
        #Select row
        row = df.iloc[offset+x]
        #print('Row({}): {}'.format(offset+x, row))

        #Store if row is before, after or both
        if row['Year'] <= cutDate:
            BEFORE = True
            beforeRow = offset+x
        else:
            AFTER = True
            afterRow = offset+x

        BOTH = BEFORE and AFTER
        if BOTH:
            rows.append(offset+x)
            options.append(1) #Both
            break

    #print('BEFORE = {}\nAFTER = {}\nBOTH = {}\n'.format(BEFORE, AFTER, BOTH))

    #If not both add appropriate elements to lists
    if not BOTH:
        if beforeRow != -1:
            rows.append(beforeRow)
            options.append(-1) #Before
        if afterRow != -1:
            rows.append(afterRow)
            options.append(0) #After

    #Set ofset to first element in next group
    offset += groupSize


#print(rows)
#print(df.iloc[rows])

#Select only the wanted rows
df = df.iloc[rows]
df.reset_index(drop=True, inplace=True)

#Add DMAP symbols to grid references
df['Gr'] = df.apply(f, axis=1)
#print(df.head())

#Generate an ordered list of species
species = sorted(list(set(df['Sp'].tolist())))

#Write data to file
with open(outFile, 'w') as file:
    for sp in species:
        GRlist = df.loc[df['Sp'] == sp, 'Gr'].tolist()
        file.write(' ' + str(int(sp)) + '\n')
        for GR in GRlist:
            file.write(str(GR) + '\n')
        file.write('-1\n')
