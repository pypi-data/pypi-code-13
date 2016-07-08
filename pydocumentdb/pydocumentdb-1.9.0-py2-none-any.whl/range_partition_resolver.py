﻿#The MIT License (MIT)
#Copyright (c) 2014 Microsoft Corporation

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import pydocumentdb.range as range

class RangePartitionResolver(object):
    """RangePartitionResolver implements partitioning based on the ranges, allowing you to
    distribute requests and data across a number of partitions.
    """
    def __init__(self, partition_key_extractor, partition_map):
        """
        :Parameters:
            - `partition_key_extractor`: lambda, returning the partition key from the document passed.
            - `partition_map`: dict, the dictionary of ranges mapped to their associated collection
        """
        if partition_key_extractor is None:
            raise ValueError("partition_key_extractor is None.")
        if partition_map is None:
            raise ValueError("partition_map is None.")

        self.partition_key_extractor = partition_key_extractor
        self.partition_map = partition_map

    def ResolveForCreate(self, document):
        """Resolves the collection for creating the document based on the partition key.

        :Parameters:
            - `document`: dict, the document to be created.

        :Returns:
            str, collection Self link or Name based link which should handle the Create operation.
        """
        if document is None:
            raise ValueError("document is None.")

        partition_key = self.partition_key_extractor(document)
        containing_range = self._GetContainingRange(partition_key)
        
        if containing_range is None:
            raise ValueError("A containing range for " + str(partition_key) + " doesn't exist in the partition map.")
        
        return self.partition_map.get(containing_range)

    def ResolveForRead(self, partition_key):
        """Resolves the collection for reading/querying the documents based on the partition key.

        :Parameters:
            - `document`: dict, the document to be read/queried.

        :Returns:
            list, collection Self link(s) or Name based link(s) which should handle the Read operation.
        """
        intersecting_ranges = self._GetIntersectingRanges(partition_key)

        collection_links = list()
        for keyrange in intersecting_ranges:
            collection_links.append(self.partition_map.get(keyrange))

        return collection_links

    def _GetContainingRange(self, partition_key):
        """Gets the containing range based on the partition key.
        """
        for keyrange in self.partition_map.keys():
            if keyrange.Contains(partition_key):
                return keyrange

        return None

    def _GetIntersectingRanges(self, partition_key):
        """Gets the intersecting ranges based on the partition key.
        """
        partitionkey_ranges = set()
        intersecting_ranges = set()

        if partition_key is None:
            return partition_map.keys()

        if isinstance(partition_key, range.Range):
            partitionkey_ranges.add(partition_key)
        elif isinstance(partition_key, list):
            for key in partition_key:
                if key is None:
                    return self.partition_map.keys()
                elif isinstance(key, range.Range):
                    partitionkey_ranges.add(key)
                else:
                    partitionkey_ranges.add(range.Range(key, key))
        else:
            partitionkey_ranges.add(range.Range(partition_key, partition_key))

        for partitionKeyRange in partitionkey_ranges:
            for keyrange in self.partition_map.keys():
                if keyrange.Intersect(partitionKeyRange):
                    intersecting_ranges.add(keyrange)

        return intersecting_ranges