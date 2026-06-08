"""generate_report.py
Generates a comprehensive Word report for the LanyingHSK web project.
It reads three reference .docx files, extracts project code information,
and writes a combined report to `FullProjectReport_LanyingHSK.docx`.
"""
import os
from pathlib import Path

from docx import Document

# Helper to extract text from a .docx file
def extract_docx_text(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join([para.text for para in doc.paragraphs])

def read_requirements(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def summarize_code(dir_path: Path) -> str:
    summary = []
    for py_file in dir_path.rglob("*.py"):
        rel = py_file.relative_to(dir_path)
        summary.append(f"### {rel}\n")
        content = py_file.read_text(encoding="utf-8")
        # Extract first docstring or comment block as description
        lines = content.splitlines()
        desc_lines = []
        in_doc = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                in_doc = True
                # Remove the opening triple quotes
                desc_lines.append(stripped.strip('"\'"'))
                continue
            if in_doc:
                if stripped.endswith('"""') or stripped.endswith("'''"):
                    # Remove the closing triple quotes
                    desc_lines.append(stripped.rstrip('"\'"'))
                    break
                desc_lines.append(stripped)
        summary.append("\n".join(desc_lines) if desc_lines else "(No module docstring found)")
        summary.append("\n")
    return "\n".join(summary)

def main():
    base = Path(__file__).parent
    # Reference documents
    refs = {
        "ProjectReport": base / "ProjectReport_LanyingHSK.docx",
        "Guideline": base / "Huong dan thuc hien CUON BAO ĐA.docx",
        "ProgressReport": base / "Bao_cao_tien_do_do_an_nganh_website_sach.docx",
    }
    doc = Document()
    doc.add_heading('LanyingHSK Web Project Comprehensive Report', level=0)
    # Introduction
    doc.add_heading('Introduction', level=1)
    doc.add_paragraph(extract_docx_text(refs["ProjectReport"]))
    # Guidelines
    doc.add_heading('Guidelines', level=1)
    doc.add_paragraph(extract_docx_text(refs["Guideline"]))
    # Progress Summary
    doc.add_heading('Progress Summary', level=1)
    doc.add_paragraph(extract_docx_text(refs["ProgressReport"]))
    # Technical Requirements
    doc.add_heading('Technical Requirements', level=1)
    req_path = base / "backend" / "requirements.txt"
    if req_path.exists():
        doc.add_paragraph(read_requirements(req_path))
    # Backend Overview
    doc.add_heading('Backend Overview', level=1)
    backend_dir = base / "backend"
    doc.add_paragraph(summarize_code(backend_dir))
    # Frontend Overview
    doc.add_heading('Frontend Overview', level=1)
    frontend_dir = base / "frontend"
    if frontend_dir.exists():
        doc.add_paragraph(summarize_code(frontend_dir))
    else:
        # Include top-level static files if no separate frontend folder
        for fname in ["index.html", "style.css", "script.js"]:
            fpath = base / fname
            if fpath.exists():
                doc.add_heading(fname, level=2)
                doc.add_paragraph(fpath.read_text(encoding="utf-8"))
    out_path = base / "FullProjectReport_LanyingHSK.docx"
    doc.save(str(out_path))
    print(f"Report generated at {out_path}")

if __name__ == "__main__":
    main()
