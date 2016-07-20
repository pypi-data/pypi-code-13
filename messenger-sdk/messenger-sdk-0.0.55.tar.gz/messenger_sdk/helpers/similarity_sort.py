from jellyfish import jaro_distance
import logging


class SimilaritySort(object):
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
                sorting_property = str(sorting_property)
                if isinstance(entry, dict):
                    if sorting_property not in entry:
                        raise ValueError(
                            'Key {property} is missing in given dict.'.format(property=sorting_property))
                    attr = entry.get(sorting_property)
                elif isinstance(entry, list):
                    raise NotImplementedError()
                else:
                    attr = getattr(entry, sorting_property)
                if attr is None:
                    attr = ''
            similarity_list.append(jaro_distance(str(attr), str(value)))

        return similarity_list

    @staticmethod
    def sorted_by(data: list, value, sorting_property=None, similarity_threshold=0, reverse=True):
        if not isinstance(reverse, bool):
            raise ValueError('Reverse value must be type of boolean.')
        similarity_list = SimilaritySort._calculate_similarity(data=data,
                                                               sorting_property=sorting_property,
                                                               value=value)
        zipped = zip(data, similarity_list)
        sorted_data = sorted(zipped, key=lambda k: k[1], reverse=reverse)

        data = list()
        for entry in sorted_data:
            if entry[1] >= similarity_threshold:
                data.append(entry[0])

        return data
