

from pprint import pprint
from dockerfile_parse import DockerfileParser


dfp = DockerfileParser('Dockerfile')

pprint(dfp.structure)
pprint(dfp.json)
pprint(dfp.labels)
