from axelrod import all_strategies
from axelrod.classifier import all_classifiers, rebuild_classifier_table

if __name__ == "__main__":
    rebuild_classifier_table(all_classifiers, all_strategies)
