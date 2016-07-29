__author__ = "David Rusk <drusk@uvic.ca>"

CANDS_TASK = "cands"
REALS_TASK = "reals"
TRACK_TASK = "track"
TARGET_TASK = "target"
STATIONARY_TASK = "vetting"

task_list = [CANDS_TASK, REALS_TASK, TRACK_TASK, TARGET_TASK, STATIONARY_TASK]

suffixes = {
    CANDS_TASK: ".cands.astrom",
    REALS_TASK: ".reals.astrom",
    TRACK_TASK: ".ast",
    TARGET_TASK: ".ssois",
    STATIONARY_TASK: ".vetting"
}


def get_suffix(task):
    return suffixes[task]
