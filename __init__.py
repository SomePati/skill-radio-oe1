# Copyright 2016 Mycroft AI, Inc.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

# http://api.rtve.es/api/programas/1750/audios.rss
# http://api.rtve.es/api/programas/36019/audios.rss

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


class RadioRneSkill(MycroftSkill):
    def __init__(self):
        super(RadioRneSkill, self).__init__(name="RadioRneSkill")
        self.process = none

    def initialize(self):
        intent = IntentBuilder("RadioRneIntent").require(
                "RadioRneKeyword").build()
        self.register_intent(intent, self_handle_intent)


    def handle_intent(self, message):
        try:

            data = feedparser.parse("http://api.rtve.es/api/programas/36019/audios.rss")
            self.speak_dialog('rne.news')
            time.sleep(5)

            self.process = play_mp3(
                re.sub(
                    'https', 'http', data['entries'][0]['links'][0]['href']))

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))


    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('rne.news.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return RadioRneSkill()
