from codecs import open

class Node:
    """
    A node in a SCRDR tree
    """

    def __init__(
        self,
        feature,
        tag,
        father=None,
        except_child=None,
        else_child=None,
        cornerstone_cases=[],
        depth=0,
    ):
        self.feature = feature
        self.tag = tag
        self.except_child = except_child
        self.else_child = else_child
        self.cornerstone_cases = cornerstone_cases
        self.father = father
        self.depth = depth

class FeatureVector:
    """
    A feature vector with features representing the context around a word
    """

    def __init__(self, initialize=False):
        self.prevWord2 = "<W>" if initialize else None   # 0
        self.prevTag2 = "<T>" if initialize else None    # 1
        self.prevWord1 = "<W>" if initialize else None   # 2
        self.prevTag1 = "<T>" if initialize else None    # 3
        self.word = "<W>" if initialize else None        # 4
        self.tag = "<T>" if initialize else None         # 5
        self.nextWord1 = "<W>" if initialize else None   # 6
        self.nextTag1 = "<T>" if initialize else None    # 7
        self.nextWord2 = "<W>" if initialize else None   # 8
        self.nextTag2 = "<T>" if initialize else None    # 9
        self.suffixL2 = "<SFX>" if initialize else None  # 10
        self.suffixL3 = "<SFX>" if initialize else None  # 11
        self.suffixL4 = "<SFX>" if initialize else None  # 12

    def matches(self, other):
        return (
            (other.prevWord2 is None or self.prevWord2 == other.prevWord2) and
            (other.prevTag2 is None or self.prevTag2 == other.prevTag2) and
            (other.prevWord1 is None or self.prevWord1 == other.prevWord1) and
            (other.prevTag1 is None or self.prevTag1 == other.prevTag1) and
            (other.word is None or self.word == other.word) and
            (other.tag is None or self.tag == other.tag) and
            (other.nextWord1 is None or self.nextWord1 == other.nextWord1) and
            (other.nextTag1 is None or self.nextTag1 == other.nextTag1) and
            (other.nextWord2 is None or self.nextWord2 == other.nextWord2) and
            (other.nextTag2 is None or self.nextTag2 == other.nextTag2) and
            (other.suffixL2 is None or self.suffixL2 == other.suffixL2) and
            (other.suffixL3 is None or self.suffixL3 == other.suffixL3) and
            (other.suffixL4 is None or self.suffixL4 == other.suffixL4)
        )

    def set_key(self, key, value):
        self.__dict__[key] = value

    @classmethod
    def build(cls, tagged_sentence, index):
        feature = FeatureVector(True)
        word, tag = tagged_sentence[index]
        feature.word = word
        feature.tag = tag

        if len(word) >= 4:
            feature.suffixL2 = word[-2:]
            feature.suffixL3 = word[-3:]

        if len(word) >= 5:
            feature.suffixL4 = word[-4:]

        if index > 0:
            feature.prevWord1, feature.prevTag1 = tagged_sentence[index - 1]

        if index > 1:
            feature.prevWord2, feature.prevTag2 = tagged_sentence[index - 2]

        if index < len(tagged_sentence) - 1:
            feature.nextWord1, feature.nextTag1 = tagged_sentence[index + 1]

        if index < len(tagged_sentence) - 2:
            feature.nextWord2, feature.nextTag2 = tagged_sentence[index + 2]

        return feature

class SCRDRTree:
    """
    Single Classification Ripple Down Rules tree for Part-of-Speech and morphological tagging
    """

    def __init__(self, root=None):
        self.root = root

    # Build tree from file containing rules using FeatureVector
    def tree_from_file(self, rules_file_path):
        self.root = Node(FeatureVector(False), "NN", None, None, None, [], 0)
        current_node = self.root
        current_depth = 0

        rules_file = open(rules_file_path, "r", encoding="utf-8")
        lines = rules_file.readlines()

        for i in xrange(1, len(lines)):
            line = lines[i]
            depth = 0
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue

            temp = line.find("cc")
            if temp == 0:
                continue

            condition, conclusion = line.split(" : ", 1)
            feature = self.parse_feature(condition)
            tag = self.parse_tag(conclusion)

            node = Node(feature, tag, None, None, None, [], depth)

            if depth > current_depth:
                current_node.except_child = node
            elif depth == current_depth:
                current_node.else_child = node
            else:
                while current_node.depth != depth:
                    current_node = current_node.father
                current_node.else_child = node

            node.father = current_node
            current_node = node
            current_depth = depth

    def dictionary_from_file(self, dictionary_file_path):
        with open(dictionary_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        dictionary = {}
        for line in lines:
            wordtag = line.strip().split()
            dictionary[wordtag[0]] = wordtag[1]

        return dictionary

    def find_fired_node(self, feature):
        current_node = self.root
        fired_node = None
        while True:
            # Check whether object satisfying the current node's feature
            satisfied = feature.matches(current_node.feature)

            if satisfied:
                fired_node = current_node
                except_child = current_node.except_child
                if except_child is None:
                    break
                else:
                    current_node = except_child
            else:
                else_child = current_node.else_child
                if else_child is None:
                    break
                else:
                    current_node = else_child

        return fired_node

    def parse_feature(self, condition):
        condition = condition.strip()

        feature = FeatureVector(False)
        for rule in condition.split(" and "):
            rule = rule.strip()
            key = rule[rule.find(".") + 1: rule.find(" ")]
            value = self.parse_tag(rule)
            feature.set_key(key, value)

        return feature

    def parse_tag(self, conclusion):
        conclusion = conclusion.strip()

        if conclusion.find('""') > 0:
            if conclusion.find("Word") > 0:
                return "<W>"
            elif conclusion.find("suffixL") > 0:
                return "<SFX>"
            else:
                return "<T>"

        return conclusion[conclusion.find("\"") + 1: len(conclusion) - 1]
