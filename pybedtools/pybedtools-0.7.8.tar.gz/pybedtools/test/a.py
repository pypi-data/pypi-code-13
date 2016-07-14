# Example for https://www.biostars.org/p/193145
#
import pybedtools
import pysam

# Use an example BAM file shipped with pybedtools
fn = pybedtools.example_filename('x.bam')
bam = pysam.Samfile(fn, 'r')

# filter reads
length_limit = 60
with pysam.Samfile('z.bam', 'wb', template=bam) as fout:
    for read in bam:
        if read.qlen < length_limit:
            fout.write(read)

# Then do downstream stuff with pybedtools/bedtools -- here, a histogram of
# read counts in each interval
z = pybedtools.BedTool('z.bam')
bed = pybedtools.example_bedtool('Cp190_Kc_Bushey_2009.bed')
result = bed.coverage(z, counts=True).to_dataframe(names=['chrom', 'start', 'end', 'count'])
print(result['count'].value_counts())
