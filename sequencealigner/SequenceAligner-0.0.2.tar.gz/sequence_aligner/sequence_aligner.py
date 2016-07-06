#!/usr/bin/python
# coding= utf8

""" In this module resides the engine of the Sequence Aligner."""
from collections import defaultdict
from progress.bar import Bar


class SequenceAligner(object):
    """ The SequenceAligner is a machine that takes a list of sequence
    fragments and constructs them into one read based on the overlaps.
    """

    def __init__(self, sequence_list):
        self.anchor_sequence = sequence_list[0]
        self.sequence_list = sequence_list[1:]
        self.__current_sequence = None
        self.align_progress = Bar('Aligning...', max=len(self.sequence_list),
                                  suffix='%(percent)d%%')
        self.sub_sequences_progress = Bar('Generating subsequences...',
                                          max=len(self.sequence_list),
                                          suffix='%(percent)d%%')
        self.subseq_combinations = self.__generate_subsequence_combos()

    def get_aligned_sequence(self):
        """
        Method that takes a list of overlapping sequences and returns a
        single, algined sequence
            - the first seq in the list is designated the 'anchor seq'
            - 'score' based on the amount of overlap with anchor seq generated
            - the seq with max overlap with anchor sequence is aligned with the
                anchor sequence and subsequently removed from the sequence_list
            - iteration occurs until sequence list is empty
        :return: aligned anchor sequence: string
        """
        while len(self.sequence_list) > 0:
            self.align_progress.next()
            # generate score card
            score_card = self.generate_score_card(self.sequence_list)

            # pull item with highest 'score', or rather, longest overlap with
            #  the anchor_sequence
            matched_seq_info = max(score_card.iteritems(),
                                   key=lambda x: len(x[1][0]))

            # align the sequence
            self.anchor_sequence = self.__add_right_left_hang(matched_seq_info)

            # remove recently aligned sequence from sequence_list
            self.sequence_list.remove(matched_seq_info[0])

        self.align_progress.finish()
        return self.anchor_sequence

    def generate_score_card(self, sequence_list):
        """
        In order to determine which sequence from sequence_list should be
        selected to align with the anchor sequence at a given iteration,
        each sequence in the list is given a score based on total overlap
        with anchor sequence at that state.
        :param sequence_list: list
        :return: score_card: dictionary
        """
        score_card = dict()
        for list_index in xrange(len(sequence_list)):

            self.__current_sequence = sequence_list[list_index]

            # generate subsequences of the current sequence
            cs = current_subsequences = \
                self.subseq_combinations[self.__current_sequence]

            # filter out those not found in anchor sequence
            # only need to check the length of the subseq into the anchor
            # sequence; since in the first iteration, it is possible that the
            # len(anchor_sequence) < len(
            sa = self.anchor_sequence
            matched_sub_seqs = set([s for s in cs if s
                                    in sa[:min(len(sa), len(s))]
                                    or s in sa[-min(len(sa), len(s)):]])

            if not matched_sub_seqs:
                continue

            # find the subseq from the list of matched combos with max length
            max_sub_seq = max(matched_sub_seqs, key=len)

            # exclude matches with non-matching overhangs
            if not self.__check_for_false_match(max_sub_seq):
                continue

            # store info about the current seq in the 'score card'
            # this includes the left and right index of the current_sequence
            # where the current subsequence overlaps (important for final
            # alignment with anchor_sequence)
            score_card[self.__current_sequence] = [max_sub_seq,
                                                   self.__curr_idx_left]

        return score_card

    def __generate_subsequence_combos(self):
        """
        Since the aligned sequences need to overlap by more than half,
        all of the possible current_sequence sub-sequences from the range of
        more-than-half- to full- length are generated.
        :return:
        """
        current_sub_seqs = defaultdict(set)
        for sequence in self.sequence_list:
            self.sub_sequences_progress.next()
            range_start = len(sequence)/2 + 1
            range_end = len(sequence) + 1
            for start in xrange(range_start, range_end + 1):
                the_range = xrange(start, range_end)
                combos = set([sequence[left:right] for
                              left, right in enumerate(the_range, 0)])
                current_sub_seqs[sequence].update(combos)

        self.sub_sequences_progress.finish()
        return current_sub_seqs

    def __check_for_false_match(self, max_sub_seq):
        """
        It could be the case that the max_sub_seq is a repeating sequence.
        In order to confirm that the correct sub_seq has been selected to
        align into the anchor sequence, a check must occur to ensure that
        exist no non-matching overhangs between current_sequence's
        max_sub_seq and the anchor_sequence
        :param max_sub_seq: string
        :return: Boolean
        """
        anchor_idx_left = self.anchor_sequence.find(max_sub_seq)
        self.__curr_idx_left = self.__current_sequence.find(max_sub_seq)
        if self.__current_sequence[:self.__curr_idx_left] and \
                self.anchor_sequence[:anchor_idx_left]:
            return False
        anchor_idx_right = anchor_idx_left + len(max_sub_seq)
        curr_idx_right = self.__curr_idx_left + len(max_sub_seq)
        if self.anchor_sequence[anchor_idx_right:] and \
                self.__current_sequence[curr_idx_right:]:
            return False
        return True

    def __add_right_left_hang(self, curr_seq_info):
        """
        Now that the max_sub_seq of the current_sequence has been established
        and verified, the alignment of the current sequence with the anchor
        sequence will occur.
        The structure of the curr_seq_info (current_sequence info) is the
        following:
        (current_sequence, [max_sub_seq, index left])
        index left is the index where the subsequence starts in the current
        sequence
        :param curr_seq_info:
        :return: curr_sub_seq (the newest anchor_sequence)
        """

        curr_idx_left = curr_seq_info[1][1]
        curr_idx_right = curr_idx_left + len(curr_seq_info[1][0])
        curr_sub_seq = curr_seq_info[1][0]
        curr_seq = curr_seq_info[0]
        anchor_idx_left = self.anchor_sequence.find(curr_sub_seq)
        anchor_right = anchor_idx_left + len(curr_sub_seq)
        # now the concatenations begin...
        if self.anchor_sequence[:anchor_idx_left]:
            curr_sub_seq = \
                self.anchor_sequence[:anchor_idx_left] + curr_sub_seq
        if curr_seq[:curr_idx_left]:
            curr_sub_seq = \
                curr_seq[:curr_idx_left] + curr_sub_seq

        if self.anchor_sequence[anchor_right:]:
            curr_sub_seq = \
                curr_sub_seq + self.anchor_sequence[anchor_right:]
        if curr_seq[curr_idx_right:]:
            curr_sub_seq = \
                curr_sub_seq + curr_seq[curr_idx_right:]

        return curr_sub_seq
