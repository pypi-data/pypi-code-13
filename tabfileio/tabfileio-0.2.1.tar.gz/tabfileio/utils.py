import numpy as np


def concatenate(head1, data1, head2, data2):
    """ Appends head2 and data2 to head1 and data1 """

    if len(set(head1) & set(head2)) > 0:
        raise Exception("Cannot concatenate because of repeated headers")

    if len(data1) != len(data2):
        raise Exception("Cannot concatenate due to row-number mismatch")


    out_head = list(head1) + list(head2)
    out_data = np.concatenate((np.array(data1), np.array(data2)), axis=1)

    return out_head, out_data


def intersecting_columns_are_close(*, head1, data1, head2, data2,
                                      atol=1.0e-13, rtol=1.0e-13):

     # Find shared headers and preserve head_1's ordering
     head = sorted(set(head1) & set(head2), key=head1.index)

     if len(head) == 0:
         raise Exception("Cannot compare the data files because no two "
                         "columns share a header")

     if np.array(data1).shape[0] != np.array(data2).shape[0]:
         raise Exception("Cannot compare exactly because data shapes are "
                         "different (data1.shape[0]={0}, data2[0].shape={1})"
                         .format(data1.shape[0], data2.shape[0]))

     for idx in range(len(data1)):
         for key in head:
             val1 = data1[idx, head1.index(key)]
             val2 = data2[idx, head2.index(key)]
             if (not np.isclose(val1, val2, atol=atol, rtol=rtol) or
                 not np.isclose(val2, val1, atol=atol, rtol=rtol)):
                 return False

     return True
