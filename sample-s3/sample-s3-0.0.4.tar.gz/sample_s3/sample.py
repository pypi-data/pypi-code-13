import random
import boto3
import sys

# How many bytes should we keep looking for header length?
MAX_HEADER_OFFSET = 100000
CR = "\r\n"


def get_s3_client():
    """ Simply return a boto s3 client. """
    return boto3.client('s3')


def get_headers(client, bucket, key, delimiter, sample_bytes=1000):
    """ Try to get the header of an object. """
    header_sample = ""
    offset = 0
    while True:
        header_sample += get_sample(client, bucket, key, offset=offset, sample_bytes=sample_bytes)
        if CR in header_sample:
            break
        elif offset > MAX_HEADER_OFFSET:
            raise ValueError('Could not find a line break in the first {} bytes.'.format(sample_bytes + offset))

        offset = offset + sample_bytes

    header_str = header_sample[:header_sample.index(CR)]

    return header_str


def get_sample(client, bucket, key, offset=0, sample_bytes=1000):
    response = client.get_object(Bucket=bucket, Key=key, Range='bytes={}-{}'.format(offset, offset + sample_bytes))
    body_string = response['Body'].read()

    # We don't want binary. Give me something useful, like unicode.
    body_string = body_string.decode('utf8')

    return body_string


def build_sample_file(bucket, key, headers, delimiter, lines, out=sys.stdout):
    client = get_s3_client()

    head_object = client.head_object(Bucket=bucket, Key=key)

    content_length = head_object['ContentLength']

    sample_offset = 0
    sample_bytes = 10000

    # use the first line to guess at number of fields.
    header_row = get_headers(client, bucket, key, delimiter)

    number_of_fields = len(header_row.split(delimiter))

    if headers:
        # Because this is included,
        # we need to make sure we do not include this in our sample.
        out.write(header_row + CR)
        sample_offset = len(header_row.encode('utf8'))

    sample_lines = 0

    while sample_lines < lines:
        # Grab a sample
        random_offset = random.randrange(sample_offset, content_length - sample_bytes)
        sample = get_sample(client,
            bucket,
            key,
            offset=random_offset,
            sample_bytes=sample_bytes)
        for line in sample.split(CR):
            # only give me complete lines.
            if len(line.split(delimiter)) == number_of_fields:
                out.write(line + CR)
                sample_lines += 1
