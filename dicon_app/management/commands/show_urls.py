from django.core.management.base import BaseCommand
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver


def iter_url_patterns(urlpatterns, prefix=""):
    """
    URLPattern / URLResolver を再帰的にたどって、
    (path, name) をyieldする
    """
    for p in urlpatterns:
        if isinstance(p, URLPattern):
            path = prefix + str(p.pattern)
            name = p.name  # name="xxx" があれば入る（なければ None）
            yield (path, name)
        elif isinstance(p, URLResolver):
            yield from iter_url_patterns(p.url_patterns, prefix + str(p.pattern))


class Command(BaseCommand):
    help = "Show URL patterns (optionally hide admin) with their name"

    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", help="Include admin urls too")
        parser.add_argument("--only-named", action="store_true", help="Show only named urls")

    def handle(self, *args, **options):
        rows = list(iter_url_patterns(get_resolver().url_patterns))

        # adminを隠す（デフォルト）
        if not options["all"]:
            rows = [(path, name) for (path, name) in rows if not path.startswith("admin/")]

        # nameがあるものだけ表示
        if options["only_named"]:
            rows = [(path, name) for (path, name) in rows if name]

        # 表示を安定させるため並び替え
        rows = sorted(set(rows), key=lambda x: (x[0], str(x[1])))

        display_path = "/" if path == "" else path
        self.stdout.write(f"{display_path}    name={label}")

        for path, name in rows:
            label = name if name else "-"
            self.stdout.write(f"{path}    name={label}")
            
