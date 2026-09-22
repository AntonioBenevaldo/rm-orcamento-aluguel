from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentType
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


def iter_block_items(parent):
    if isinstance(parent, DocumentType):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        return

    for child in parent_elm.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("}tbl"):
            table = Table(child, parent)
            yield table


def walk_container(parent, prefix):
    paragraph_index = 0
    table_index = 0
    for block in iter_block_items(parent):
        if isinstance(block, Paragraph):
            paragraph_index += 1
            yield f"{prefix}/p{paragraph_index}", block
        else:
            table_index += 1
            for r_idx, row in enumerate(block.rows, 1):
                for c_idx, cell in enumerate(row.cells, 1):
                    yield from walk_container(
                        cell, f"{prefix}/t{table_index}/r{r_idx}/c{c_idx}"
                    )


def points(value):
    return None if value is None else round(value.pt, 2)


def paragraph_record(location, paragraph):
    text = paragraph.text
    fmt = paragraph.paragraph_format
    issues = []
    if text.startswith((" ", "\t", "\u00a0")):
        issues.append("leading_whitespace")
    if text.endswith((" ", "\t", "\u00a0")):
        issues.append("trailing_whitespace")
    if re.search(r" {2,}", text):
        issues.append("multiple_spaces")
    if "\t" in text:
        issues.append("tab_character")
    if "\u00a0" in text:
        issues.append("nonbreaking_space")

    return {
        "location": location,
        "style": paragraph.style.name if paragraph.style else None,
        "text": text,
        "issues": issues,
        "format": {
            "alignment": str(paragraph.alignment),
            "left_indent_pt": points(fmt.left_indent),
            "right_indent_pt": points(fmt.right_indent),
            "first_line_indent_pt": points(fmt.first_line_indent),
            "space_before_pt": points(fmt.space_before),
            "space_after_pt": points(fmt.space_after),
            "line_spacing": (
                round(fmt.line_spacing, 3)
                if isinstance(fmt.line_spacing, float)
                else points(fmt.line_spacing)
            ),
        },
        "runs": [
            {
                "text": run.text,
                "bold": run.bold,
                "italic": run.italic,
                "underline": run.underline,
                "font": run.font.name,
                "size_pt": points(run.font.size),
            }
            for run in paragraph.runs
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    doc = Document(args.input)
    records = []
    records.extend(
        paragraph_record(location, paragraph)
        for location, paragraph in walk_container(doc, "body")
    )

    for section_index, section in enumerate(doc.sections, 1):
        records.extend(
            paragraph_record(location, paragraph)
            for location, paragraph in walk_container(
                section.header, f"section{section_index}/header"
            )
        )
        records.extend(
            paragraph_record(location, paragraph)
            for location, paragraph in walk_container(
                section.footer, f"section{section_index}/footer"
            )
        )

    body_records = [r for r in records if r["location"].startswith("body/")]
    empty_runs = []
    current = []
    for rec in body_records:
        if rec["text"].strip() == "":
            current.append(rec["location"])
        else:
            if len(current) >= 2:
                empty_runs.append(current)
            current = []
    if len(current) >= 2:
        empty_runs.append(current)

    issue_records = [r for r in records if r["issues"]]
    styles = {}
    for rec in records:
        styles[rec["style"]] = styles.get(rec["style"], 0) + 1

    payload = {
        "input": str(Path(args.input).resolve()),
        "paragraph_count": len(records),
        "table_count": len(doc.tables),
        "inline_shape_count": len(doc.inline_shapes),
        "section_count": len(doc.sections),
        "style_counts": dict(sorted(styles.items(), key=lambda item: (-item[1], str(item[0])))),
        "whitespace_issue_count": len(issue_records),
        "whitespace_issues": issue_records,
        "consecutive_empty_paragraph_groups": empty_runs,
        "all_paragraphs": records,
    }
    Path(args.json).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "paragraph_count": payload["paragraph_count"],
                "table_count": payload["table_count"],
                "inline_shape_count": payload["inline_shape_count"],
                "section_count": payload["section_count"],
                "whitespace_issue_count": payload["whitespace_issue_count"],
                "consecutive_empty_paragraph_groups": len(empty_runs),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
