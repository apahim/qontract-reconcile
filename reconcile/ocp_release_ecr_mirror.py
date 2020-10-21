import logging
import tempfile

from reconcile import queries
from utils import secret_reader


_LOG = logging.getLogger(__name__)

QONTRACT_INTEGRATION = 'ocp-release-ecr-mirror'

ECR_PULL_SECRET = {'path': 'app-sre/integrations-output/aws-ecr-image-pull-secrets/app-sre/us-east-1/dockercfg'}


class OcpReleaseEcrMirror:

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.settings = queries.get_app_interface_settings()


    def run(self):
        dockerconfig_content = self._get_dockerconfig()
        _, filename = tempfile.mkstemp()
        import pydevd
        pydevd.settrace()
        with open(filename, 'w') as file_obj:
            file_obj.write(dockerconfig_content)



        print('Yay!')

    def _get_dockerconfig(self):
        raw_data = secret_reader.read_all(ECR_PULL_SECRET,
                                          settings=self.settings)
        return raw_data['.dockerconfigjson']


def run(dry_run):
    quay_mirror = OcpReleaseEcrMirror(dry_run)
    quay_mirror.run()
