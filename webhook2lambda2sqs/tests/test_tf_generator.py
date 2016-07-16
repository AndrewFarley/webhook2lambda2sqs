"""
The latest version of this package is available at:
<http://github.com/jantman/webhook2lambda2sqs>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of webhook2lambda2sqs, also known as webhook2lambda2sqs.

    webhook2lambda2sqs is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    webhook2lambda2sqs is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with webhook2lambda2sqs.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/webhook2lambda2sqs> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""
import sys

from webhook2lambda2sqs.tf_generator import TerraformGenerator
from webhook2lambda2sqs.version import VERSION, PROJECT_URL

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'webhook2lambda2sqs.tf_generator'


class TestTerraformGenerator(object):

    def setup(self):
        self.conf = {}

        def se_get(k):
            return self.conf.get(k, None)

        config = Mock()
        config.get.side_effect = se_get
        self.cls = TerraformGenerator(config)

    def test_init(self):
        config = Mock()
        cls = TerraformGenerator(config)
        assert cls.config == config

    def test_get_tags_none(self):
        res = self.cls._get_tags()
        assert res == {
            'Name': 'webhook2lambda2sqs',
            'created_by': 'webhook2lambda2sqs v%s <%s>' % (VERSION, PROJECT_URL)
        }

    def test_get_tags(self):
        self.conf = {
            'aws_tags': {
                'Name': 'myname',
                'other': 'otherval',
                'foo': 'bar'
            }
        }
        res = self.cls._get_tags()
        assert res == {
            'Name': 'myname',
            'other': 'otherval',
            'foo': 'bar',
            'created_by': 'webhook2lambda2sqs v%s <%s>' % (VERSION, PROJECT_URL)
        }
