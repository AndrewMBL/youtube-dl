# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import ExtractorError
from .nexx import NexxIE
from ..compat import compat_urlparse


class Tele5IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?tele5\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _TESTS = [{
        'url': 'https://www.tele5.de/filme/mega-alligators/',
        'note': 'Test movie downlaod',
        'info_dict': {
            'id': '1679012',
            'ext': 'mp4',
            'upload_date': '20200317',
            'timestamp': 1584429063,
            'title': 'Mega Alligators',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.tele5.de/kalkofes-welt/best-of-clips/politik-und-gesellschaft/?ve_id=9MD418FO',
        'note': 'Test clip download from second item in playlist',
        'info_dict': {
            'id': '1489567',
            'ext': 'mp4',
            'upload_date': '20180424',
            'timestamp': 1524567086,
            'title': 'Panorama - Merkel muss weg!',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.tele5.de/fsk-sex/',
        'note': 'Test show download from second first in playlist',
        'info_dict': {
            'id': '1675622',
            'ext': 'mp4',
            'upload_date': '20200315',
            'timestamp': 1584256259,
            'title': 'Sleeping Beauty',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.tele5.de/filme/schlefaz-dragon-crusaders/',
        'only_matching': True,
    }, {
        'url': 'https://www.tele5.de/filme/making-of/avengers-endgame/',
        'only_matching': True,
    }, {
        'url': 'https://www.tele5.de/star-trek/raumschiff-voyager/ganze-folge/das-vinculum/',
        'only_matching': True,
    }, {
        'url': 'https://www.tele5.de/kalkofes-welt/',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        qs = compat_urlparse.parse_qs(compat_urlparse.urlparse(url).query)
        video_id = (qs.get('vid') or qs.get('ve_id') or [None])[0]

        if not video_id:
            display_id = self._match_id(url)
            webpage = self._download_webpage(url, display_id)
            video_id = self._html_search_regex(
                (r'id\s*=\s*["\']video-player["\'][^>]+data-id\s*=\s*["\']([^"\']+)',
                 r'\s+id\s*=\s*["\']player_([^"\']{6,})',
                 r'\bdata-id\s*=\s*["\']([^"\']{6,})'), webpage, 'JWplayer video id')  # NEW: get new JWplayer video id

        # NEW: translate the new JWplayer video id into the old nexx video id:
        info = self._download_json('https://cdn.jwplayer.com/v2/media/%s' % video_id, self._match_id(url))  # when video id is in the url display id isn't initialised
        video_id = info['playlist'][0]['nexx_id']  # TODO: no idea, how to use: info.get()
        if not video_id:
            error = '%s: Cannot get nexx video id' % display_id
            raise ExtractorError(error, expected=True)  # Needs: from ..utils import ExtractorError

        return self.url_result(
            'https://api.nexx.cloud/v3/759/videos/byid/%s' % video_id,
            ie=NexxIE.ie_key(), video_id=video_id)
