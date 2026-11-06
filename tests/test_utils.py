import json
import sys
from types import ModuleType
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# utils.py also imports application configuration and a terminal banner library;
# neither is needed by extract_field, so isolate these tests from app startup.
sys.modules.setdefault("config", ModuleType("config"))
if "pyfiglet" not in sys.modules:
    pyfiglet = ModuleType("pyfiglet")
    pyfiglet.Figlet = object
    sys.modules["pyfiglet"] = pyfiglet

from utils import extract_field


class ExtractFieldTests(unittest.TestCase):
    @staticmethod
    def vinext_push(chunk):
        return (
            '<script>((self[Symbol.for("vinext.navigationRuntime")]??='
            '{bootstrap:{routeManifest:null},functions:{}}).bootstrap.rsc??='
            '{rsc:[]}).rsc.push('
            f"{json.dumps(chunk)}"
            ")</script>"
        )

    @staticmethod
    def raw_vinext_push(argument):
        return (
            '<script>((self[Symbol.for("vinext.navigationRuntime")]??='
            '{bootstrap:{routeManifest:null},functions:{}}).bootstrap.rsc??='
            '{rsc:[]}).rsc.push('
            f"{argument}</script>"
        )

    def test_reassembles_media_url_split_between_vinext_pushes(self):
        first = (
            '{"media_url":"https://api.platzi.com/mdstrm/v1/video/'
            '6ada35acedc11f91018d6cca.m3u8?subtitles=english-spanish-'
        )
        second = (
            'portuguese.vtt","materialId":"material-123"}'
        )
        html = self.vinext_push(first) + self.vinext_push(second)

        self.assertEqual(
            extract_field(html, "media_url"),
            "https://api.platzi.com/mdstrm/v1/video/"
            "6ada35acedc11f91018d6cca.m3u8?subtitles=english-spanish-"
            "portuguese.vtt",
        )
        self.assertEqual(extract_field(html, "materialId"), "material-123")

    def test_reassembles_raw_fragment_ending_at_script_boundary(self):
        first = self.raw_vinext_push(
            r'{\"media_url\":\"https://api.platzi.com/mdstrm/v1/video/'
            r'6ada35acedc11f91018d6cca.m3u8?subtitles='
            r'W3sibmFtZSI6ICJFbmdsaXNoIiwgImxhbmd1YWdlIjogImVuIiwgInVyaSI6'
            r'ICJodHRwczovL3N0YXRpYy5wbGF0emkuY29tL21lZGlhL3N1YnRpdGxlLzEz'
            r'OTIwZGM3OTcwNDU1YzhlZGQyNGUxMGIxMzQzOTRmOTQ2YzFlNDVkNGFlYzJj'
            r'NjA1YzUwMGVhMjA3MmFlYWEtZW4udnR0In0'
            '" )'
        )
        second = self.vinext_push(
            'sIHsibmFtZSI6ICJTcGFuaXNoIiwgImxhbmd1YWdlIjogImVzIiwgInVyaSI6'
            'ICJodHRwczovL3N0YXRpYy5wbGF0emkuY29tL21lZGlhL3N1YnRpdGxlLzRk'
            'MTNiYWQ4MjcwOTVhMzc2MjJjMmE0OTg0NzQ5YmMzMmI5MDg0NmU2MTI4OTcw'
            'ZTY3NWNhMTgyYzA1ZjEzMTYtZXMudnR0In0sIHsibmFtZSI6ICJCcmF6aWxpYW'
            '4gUG9ydHVndWVzZSIsICJsYW5ndWFnZSI6ICJwdCIsICJ1cmkiOiAiaHR0cHM6'
            'Ly9zdGF0aWMucGxhdHppLmNvbS9tZWRpYS9zdWJ0aXRsZS85ZmM5MzEyZDkw'
            'YzE0ZGEzY2VmNTU4MTk4OWZhZDk1YzA3YzBhZDQ4ZTI4NzVjODU5ZWZjNjZi'
            'ZGM4OTA0MzgyLXB0LnZ0dCJ9XQ=="}'
        )

        self.assertEqual(
            extract_field(first + second, "media_url"),
            "https://api.platzi.com/mdstrm/v1/video/"
            "6ada35acedc11f91018d6cca.m3u8?subtitles="
            "W3sibmFtZSI6ICJFbmdsaXNoIiwgImxhbmd1YWdlIjogImVuIiwgInVyaSI6"
            "ICJodHRwczovL3N0YXRpYy5wbGF0emkuY29tL21lZGlhL3N1YnRpdGxlLzEz"
            "OTIwZGM3OTcwNDU1YzhlZGQyNGUxMGIxMzQzOTRmOTQ2YzFlNDVkNGFlYzJj"
            "NjA1YzUwMGVhMjA3MmFlYWEtZW4udnR0In0"
            "sIHsibmFtZSI6ICJTcGFuaXNoIiwgImxhbmd1YWdlIjogImVzIiwgInVyaSI6"
            "ICJodHRwczovL3N0YXRpYy5wbGF0emkuY29tL21lZGlhL3N1YnRpdGxlLzRk"
            "MTNiYWQ4MjcwOTVhMzc2MjJjMmE0OTg0NzQ5YmMzMmI5MDg0NmU2MTI4OTcw"
            "ZTY3NWNhMTgyYzA1ZjEzMTYtZXMudnR0In0sIHsibmFtZSI6ICJCcmF6aWxpYW"
            "4gUG9ydHVndWVzZSIsICJsYW5ndWFnZSI6ICJwdCIsICJ1cmkiOiAiaHR0cHM6"
            "Ly9zdGF0aWMucGxhdHppLmNvbS9tZWRpYS9zdWJ0aXRsZS85ZmM5MzEyZDkw"
            "YzE0ZGEzY2VmNTU4MTk4OWZhZDk1YzA3YzBhZDQ4ZTI4NzVjODU5ZWZjNjZi"
            "ZGM4OTA0MzgyLXB0LnZ0dCJ9XQ=="
        )

    def test_keeps_extracting_next_flight_chunks(self):
        html = (
            '<script>self.__next_f.push([1,'
            '"{\\"media_url\\":\\"https://cdn.example/video.m3u8\\"}"])'
            "</script>"
        )

        self.assertEqual(
            extract_field(html, "media_url"), "https://cdn.example/video.m3u8"
        )

    def test_extracts_plain_html_field(self):
        self.assertEqual(
            extract_field('<script>{"materialId":"plain-123"}</script>', "materialId"),
            "plain-123",
        )

    def test_malformed_vinext_push_does_not_hide_later_valid_field(self):
        malformed = (
            '<script>runtime.rsc.push("incomplete payload</script>'
        )
        html = malformed + self.vinext_push('{"materialId":"recovered"}')

        self.assertEqual(extract_field(html, "materialId"), "recovered")


if __name__ == "__main__":
    unittest.main()
