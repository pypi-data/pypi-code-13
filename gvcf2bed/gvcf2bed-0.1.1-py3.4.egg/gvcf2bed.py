"""
gvcf2bed tool
~~~~~~~~~~~~~


:copyright: (c) 2016 Sander Bollen
:copyright: (c) 2016 Leiden University Medical Center
:license: MIT
"""

import argparse
from collections import namedtuple
import vcf


class BedLine(namedtuple("BedLine", ["chromosome", "start", "end"])):

    def __str__(self):
        return "{0}\t{1}\t{2}".format(self.chromosome, self.start, self.end)


def get_gqx(record, sample):
    """
    Get GQX value from a pyvcf record
    :param record: an instance of a pyvcf Record
    :param sample: sample name
    :return: float
    """
    fmt = record.genotype(sample)
    if hasattr(fmt.data, "GQ") and record.QUAL:
        return min(float(fmt.data.GQ), record.QUAL)
    elif hasattr(fmt.data, "GQ"):
        return float(fmt.data.GQ)
    elif record.QUAL:
        return record.QUAL
    else:
        return 0.0


def vcf_record_to_bed(record):
    """
    Convert a VCF record to a BED record
    :param record: vcf record
    :return: BedLine record
    """
    if "END" in record.INFO:
        return BedLine(record.CHROM, record.start, record.INFO['END'])
    return BedLine(record.CHROM, record.start, record.end)


def main():
    desc = """
    Create a BED file from a gVCF.
    Regions are based on a minimum genotype quality.
    The gVCF file must contain a GQ field in its FORMAT fields.
    """
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-I", "--input", type=str, required=True, help="Input gVCF")
    parser.add_argument("-O", "--output", type=str, required=True, help="Output bed file")
    parser.add_argument("-s", "--sample", type=str, required=False, help="Sample name in VCF file to use. "
                                                                         "Will default to first sample "
                                                                         "(alphabetically) if not supplied")
    parser.add_argument("-q", "--quality", type=int, default=20, help="Minimum genotype quality (default 20)")

    args = parser.parse_args()

    reader = vcf.Reader(filename=args.input)
    if not args.sample:
        args.sample = sorted(reader.samples)[0]

    with open(args.output, "w") as ohandle:
        for record in reader:
            if get_gqx(record, args.sample) >= args.quality:
                ohandle.write(str(vcf_record_to_bed(record)) + "\n")

if __name__ == "__main__":
    main()
