from refextract import extract_references_from_file

references = extract_references_from_file('./Already_Read/A-Bayesian-modeling-framework-for-crash-severity-effe_2020_Accident-Analysis.pdf')
for ref in references:
    print (ref)
    print ()
