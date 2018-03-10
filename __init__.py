# Copyright 2016 Mycroft AI, Inc.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import feedparser
import time
from os.path import dirname
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util import play_mp3
from mycroft.util.log import getLogger


__author__ = 'fernandez'

LOGGER = getLogger(__name__)


class RadioOe1Skill(MycroftSkill):
    def __init__(self):
        super(RadioOe1Skill, self).__init__(name="RadioOe1Skill")
        self.process = None

    def initialize(self):
        intent = IntentBuilder("RadioOe1Intent").require(
                "RadioOe1Keyword").build()
        self.register_intent(intent, self.handle_intent)


    def handle_intent(self, message):
        try:

            data = feedparser.parse("http://static.orf.at/podcast/oe1/oe1_journale.xml")
            self.speak_dialog('oe1.news')
            time.sleep(5)

            self.process = play_mp3(
                re.sub(
                    'https', 'http', data['entries'][0]['enclosures'][0]['href']))

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))


    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('oe1.news.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return RadioOe1Skill()
