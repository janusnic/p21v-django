from fixture import DataSet
class Authors(DataSet):
    class frank_herbert:
        first_name = "Frank"
        last_name = "Herbert"

from fixture.dataset.converter import dataset_to_json
print (dataset_to_json(Authors))