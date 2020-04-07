import os

from axelrod import all_strategies
from axelrod.classifier import all_classifiers, rebuild_classifier_table

if __name__ == "__main__":
    # Change to relative path inside axelrod folder
    rebuild_classifier_table(all_classifiers, all_strategies)
