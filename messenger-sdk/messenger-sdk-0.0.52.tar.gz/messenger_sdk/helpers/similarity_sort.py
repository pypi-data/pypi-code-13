from jellyfish import jaro_distance
import logging


class SimilaritySort(object):
    @staticmethod
    def sorted_by(data: list, value, sorting_property=None, similarity_threshold=0, reverse=True):
        similarity_list = SimilaritySort._calculate_similarity(data=data,
                                                               sorting_property=sorting_property,
                                                               value=value)
        zipped = zip(data, similarity_list)
        sorted_data = sorted(zipped, key=lambda k: k[1], reverse=reverse)

        data = list()
        for entry in sorted_data:
            if entry[1] > similarity_threshold:
                data.append(entry[0])

        return data

    @staticmethod
    def _calculate_similarity(data: list, value, sorting_property=None):
        similarity_list = list()
        for entry in data:
            if isinstance(entry, str):
                if sorting_property is not None:
                    logging.warning('"sorting_property" is not necessary in string sorting.')
                attr = entry
            else:
                if sorting_property is None:
                    raise ValueError('Sorting property must be defined.')
                if isinstance(entry, dict):
                    attr = entry.get(sorting_property)
                    if not attr:
                        raise ValueError(
                            'Value of property {property} is missing in given dict.'.format(property=sorting_property))
                elif isinstance(entry, list):
                    raise NotImplementedError()
                else:
                    attr = getattr(entry, sorting_property)
            similarity_list.append(jaro_distance(attr, value))

        return similarity_list
