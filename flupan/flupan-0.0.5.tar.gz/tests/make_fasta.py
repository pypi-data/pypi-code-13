
from Bio import SeqIO

infile = "gisaid_epiflu_sequence_Jan13_2016.fasta"
outfile = open("reduced_gisaid_sequences.fasta", "w")
for record in SeqIO.parse(infile, "fasta"):
   outfile.write(record.id + "\n")
   reduced_seq = record.seq[0:20]
   outfile.write(str(reduced_seq) +"\n")

outfile.close()











