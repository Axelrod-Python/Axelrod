import os

from axelrod import all_strategies
from axelrod.classifier import ALL_CLASSIFIERS_PATH, all_classifiers, \
    rebuild_classifier_table

if __name__ == "__main__":
    # Change to relative path inside axelrod folder
    axelrod_path = os.path.join("axelrod", ALL_CLASSIFIERS_PATH)
    rebuild_classifier_table(all_classifiers, all_strategies, path=axelrod_path)
