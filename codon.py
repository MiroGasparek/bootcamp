# Program asks whether or not a codon is canonical start codon

# Make a list of stop codons
stop_codons = ['UAA','UAG','UGA']
# Specify codon
codon = 'UGG'

# Check to see if it is a start or stop codon
if codon == 'AUG':
    print('This codon is the start codon.')
    print('This will also be evaluated.')
elif codon in stop_codons:
        print('This codon is a stop codon.')
else:
        print('This codon is neither start nor stop codon.')
