# Conditional Exercise

codon = 'AUG'

if codon == 'AUG':
    print('This codon is the start codon.')
elif codon == 'UAA' or codon == 'UAG' or codon == 'UGA':
    print('This codon is a stop codon.')
else:
    print('This codon is not the start codon.')
