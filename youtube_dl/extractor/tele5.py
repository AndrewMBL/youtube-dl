# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .jwplatform import JWPlatformIE
from ..compat import compat_urlparse


class Tele5IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?tele5\.de/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _TESTS = [{
        'url': 'https://www.tele5.de/filme/mega-alligators/',
        'info_dict': {
            'id': 'X7QbljEQ',
            'ext': 'mp4',
            'upload_date': '20200330',
            'timestamp': 1585605000,
            'title': 'Mega Alligators',
            'description': 'md5:c9797a326f95f97fd466d453d63a92c1',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.tele5.de/kalkofes-welt/best-of-clips/politik-und-gesellschaft/?ve_id=9MD418FO',
        'info_dict': {
            'id': '9MD418FO',
            'ext': 'mp4',
            'upload_date': '20200326',
            'timestamp': 1585189280,
            'title': 'Panorama - Merkel muss weg!',
            'description': 'md5:3bdf72fb093d1e8b01f515b0ee1dec9e',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.tele5.de/fsk-sex/?ve_id=1662408',
        'only_matching': True,
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
            video_id = self._search_regex(
                (r'id\s*=\s*["\']video-player["\'][^>]+data-id\s*=\s*["\']([^"]+)',
                 r'\s+id\s*=\s*["\']player_([^"]{6,})',
                 r'\bdata-id\s*=\s*["\']([^"]{6,})'), webpage, 'video_id')

        return self.url_result(
            'jwplatform:%s' % video_id, ie=JWPlatformIE.ie_key())
