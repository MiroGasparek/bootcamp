# Make a list of stop codons
stop_codons = ['UAA','UAG','UGA']

# Specify codon
codon = 'UGG'

# Check to see if this is start or stop codon
if codon == 'AUG':
    print('This codon is the start codon.')
elif  codon in stop_codons:
    print('This codon is a stop codon.')
else:
    print('This codon is neither a start nor stop codon.')
