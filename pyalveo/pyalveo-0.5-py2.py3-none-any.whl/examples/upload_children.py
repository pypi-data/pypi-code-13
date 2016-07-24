import sys,os,random
import pyalveo
import time
from glob import glob

# disable insecure HTTPS warnings from the staging servers
import requests
requests.packages.urllib3.disable_warnings()

EXT_MAP = {
    '.wav': "Audio",
    '.txt': "Text",
    '.sf0': "Pitch Track",
    '.sfb': "Formant Track",
    '.lab': "Annotation",
    '.trg': "Annotation",
    '.hlb': "Annotation",
}

def process(basedir):
    """Process the files in this corpus"""

    client = pyalveo.Client(configfile="examples/alveo-pc.config" ,verifySSL=False,cache_dir="wrassp_cache")

    collection_uri = client.api_url + "catalog/sc_cw_children"

    # delete any existing items
    print "Deleting items: ", list(client.get_items(collection_uri))
    for itemuri in client.get_items(collection_uri):
        client.delete_item(itemuri)


    count = 0
    for itemid, meta, files in corpus_items(basedir):
        start = time.time()
        item = client.add_item(collection_uri, itemid, meta)
        print "Item: ", itemid, time.time()-start

        for file in files:
            docname = os.path.basename(file)
            root, ext = os.path.splitext(docname)
            if ext in EXT_MAP:
                doctype = EXT_MAP[ext]
            else:
                doctype = "Other"

            docmeta = {
                       "dcterms:title": docname,
                       "dcterms:type": doctype
                      }
            client.add_document(item, docname, docmeta, file=file)
            print "\tDocument: ", docname, time.time()-start

        count += 1
        if count > 1000:
            return



def corpus_items(basedir):
    """Return an iterator over items in the corpus,
    each item is returned as a tuple: (itemid, metadata, [file1, file2, file3])
    where itemid is the identifier
    metadata is a dictionary of metadata
    fileN are the files to attach to the item
    """
    meta = {
            'dcterms:creator': 'C. Watson and S. Cassidy',
            "ausnc:mode": "spoken",
            "ausnc:communication_context": "face-to-face",
            "olac:language": "eng",
            "ausnc:interactivity": "read",
            "ausnc:audience": "individual",
            }


    for spkr in os.listdir(basedir):
        # iterate over wav files
        for wav in os.listdir(os.path.join(basedir, spkr, 'data')):
            meta['olac:speaker'] = spkr
            files = []
            (sp, prompt, ext) = wav.split('.')

            if ext == 'wav':
                meta['dcterms:title'] = prompt
                meta['austalk:prompt'] = prompt

                # gather the files
                files.extend(glob(os.path.join(basedir, spkr, 'data', sp+'.'+prompt+'.*')))
                files.extend(glob(os.path.join(basedir, spkr, 'labels', sp+'.'+prompt+'.*')))

                yield (spkr + "." + prompt, meta, files)



if __name__=='__main__':

    basedir = sys.argv[1]

    process(basedir)
