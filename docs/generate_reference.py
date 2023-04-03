"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("yafti").rglob("*.py")):
    print(path)
    module_path = path.with_suffix("")
    print(module_path)
    doc_path = path.relative_to("yafti").with_suffix(".md")
    print(doc_path)
    full_doc_path = Path("reference", doc_path)
    print(full_doc_path)

    parts = tuple(module_path.parts)

    print(parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    print(doc_path)

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        if len(parts) < 1:
            fd.write("")
            continue

        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)

with mkdocs_gen_files.open("reference/SUMMARY.txt", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
