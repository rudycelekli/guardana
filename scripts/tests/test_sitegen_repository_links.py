"""Repository links retain the section a documentation author selected."""

from pathlib import Path

import pytest

from sitegen.links import LinkResolver
from sitegen.page import Page


@pytest.mark.parametrize(
    ("href", "expected"),
    [
        ("../CONTRIBUTING.md#principles", "blob/main/CONTRIBUTING.md#principles"),
        ("../examples/#setup", "tree/main/examples#setup"),
        ("attachment.json#section", "blob/main/docs/attachment.json#section"),
        ("../CONTRIBUTING.md", "blob/main/CONTRIBUTING.md"),
    ],
)
def test_repository_link_retains_its_fragment(tmp_path: Path, href: str, expected: str) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (tmp_path / "CONTRIBUTING.md").write_text("# Principles\n", encoding="utf-8")
    (tmp_path / "examples").mkdir()
    (docs / "attachment.json").write_text("{}", encoding="utf-8")
    page = Page(Path("index.md"), "Docs", 1, "Docs", "stable", "")
    resolver = LinkResolver(tmp_path, docs, {})

    assert resolver.for_page(page)(href) == f"https://github.com/guardana/guardana/{expected}"
    assert resolver.problems == []


def test_rendered_page_fragment_still_resolves_locally(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    page = Page(Path("index.md"), "Docs", 1, "Docs", "stable", "")
    resolver = LinkResolver(tmp_path, docs, {Path("other.md"): frozenset({"section"})})

    assert resolver.for_page(page)("other.md#section") == "other.html#section"
    assert resolver.problems == []


def test_external_fragment_is_unchanged(tmp_path: Path) -> None:
    page = Page(Path("index.md"), "Docs", 1, "Docs", "stable", "")
    resolver = LinkResolver(tmp_path, tmp_path / "docs", {})
    href = "https://example.test/page#section"

    assert resolver.for_page(page)(href) == href
    assert resolver.problems == []
