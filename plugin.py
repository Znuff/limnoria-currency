###
# Copyright (c) 2017, Bogdan Ilisei
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Currency')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import json


class Currency(callbacks.Plugin):
    """Currency conversion"""
    threaded = True

    def convert(self, irc, msg, args, number, curr1, curr2):
        """[<number>] <currency1> to <currency2>

        Converts from <currency1> to <currency2>. If number isn't given, it
        defaults to 1.
        """

        api_key = self.registryValue('apikey')

        if not api_key:
            irc.error('No API Key configured.')

        if len(curr1) !=3 and len(curr2) != 3:
            irc.error('You must use three-letter symbols for currencies.')

        url = 'http://api.apilayer.com/currency_data/convert?to={curr2}&from={curr1}&amount={amount}&apikey={apikey}'.format(curr2=curr2.upper(), curr1=curr1.upper(), amount=number, apikey=api_key);

        try:
            content = utils.web.getUrl(url)
        except utils.web.Error as e:
            irc.error(str(e), Raise=True)

        content = utils.web.getUrl(url)

        data = json.loads(content.decode('utf-8'))

        if data['success']:
            try:
                # better ides?
                # from_amount = str(data['query']['amount']).format('{:.06f}').rstrip("0")
                from_amount = data['query']['amount']
                # to_amount = str(data['result']).format('{:.06f}').rstrip("0")
                to_amount = data['result']
                irc.reply( format('%.2f %s == %.2f %s', from_amount, data['query']['from'], to_amount, data['query']['to']) )
            except Exception as e:
                irc.error('I have no idea. Something fucked up: {}'.format(str(e)))

    convert = wrap(convert, [optional('float', 1.0), 'lowered', 'to', 'lowered'])


Class = Currency


# vim:set shiftwidth=4 softtabstop=4 expandtab :
