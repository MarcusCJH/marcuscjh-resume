# tests/test_sync_cv.py
import json
from pathlib import Path

import sync_resume as sr


def load_fixture():
    fixture = Path(__file__).parent / "fixtures" / "cv_sample.json"
    return json.loads(fixture.read_text(encoding="utf-8"))


def test_infer_density_uses_explicit_cv_field():
    entry = {"company": "X", "cv": {"density": "oneliner"}}
    assert sr.infer_cv_density(entry) == "oneliner"

def test_infer_density_defaults_by_company_heuristics():
    assert sr.infer_cv_density({"company": "Accenture", "modalContent": {}}) == "featured"
    assert sr.infer_cv_density({"company": "Whale Cloud", "modalContent": {}}) == "compact"
    assert sr.infer_cv_density({"company": "Hitachi", "modalContent": {}}) == "oneliner"

def test_select_featured_certs_prefers_flag_then_limit():
    timeline = [
        {"category": "certification", "order": 1, "title": "Old", "cv": {}},
        {"category": "certification", "order": 2, "title": "Feat", "cv": {"featured": True}},
        {"category": "certification", "order": 3, "title": "Feat2", "cv": {"featured": True}},
    ]
    selected = sr.select_featured_certs(timeline, limit=6)
    assert [c["title"] for c in selected] == ["Feat2", "Feat"]


def test_select_cv_certs_all_includes_every_cert():
    timeline = [
        {"category": "certification", "order": 1, "title": "Old", "cv": {}},
        {"category": "certification", "order": 2, "title": "Feat", "cv": {"featured": True}},
        {"category": "work", "order": 9, "title": "Skip"},
    ]
    selected = sr.select_cv_certs(timeline, mode="all")
    assert [c["title"] for c in selected] == ["Feat", "Old"]

def test_extract_cv_bullets_prefers_cv_bullets():
    entry = {"cv": {"bullets": ["A", "B", "C"]}, "modalContent": {"details": ["• ignore"]}}
    assert sr.extract_cv_bullets(entry, max_bullets=2) == ["A", "B"]

def test_extract_cv_bullets_falls_back_to_modal_details():
    entry = {
        "modalContent": {
            "details": [
                "• Bullet 1",
                "  • Nested 2",
                "Ignored line"
            ]
        }
    }
    bullets = sr.extract_cv_bullets(entry, max_bullets=5)
    assert bullets == ["Bullet 1", "Nested 2"]

def test_format_oneliner_prefers_cv_line():
    entry = {
        "company": "Hitachi",
        "title": "Intern",
        "startDate": "2013",
        "endDate": "2013",
        "cv": {"line": "Hitachi · Intern · 2013 — graph viz"},
    }
    assert sr.format_oneliner(entry) == "Hitachi · Intern · 2013 — graph viz"


def test_sync_cv_experience_contains_featured_and_earlier_oneliner(tmp_path):
    syncer = sr.ResumeSyncer()
    syncer.data = load_fixture()
    syncer.resume_sections_dir = tmp_path

    syncer.update_cv_experience()

    text = (tmp_path / "experience.tex").read_text(encoding="utf-8")
    assert "\\cvExperience{Accenture}" in text
    assert "\\cvRole{Technical Lead}" in text
    assert "\\cvEarlier{" in text
    assert "Veev" in text


def test_resolve_use_local_source_selection():
    assert sr.resolve_use_local("local", local_exists=False) is True
    assert sr.resolve_use_local("remote", local_exists=True) is False
    assert sr.resolve_use_local("auto", local_exists=True) is True
    assert sr.resolve_use_local("auto", local_exists=False) is False


def test_main_remote_source_does_not_use_local(monkeypatch):
    calls = {}

    def fake_sync_all(self, use_local=False, target="all"):
        calls["use_local"] = use_local
        calls["target"] = target
        return True

    monkeypatch.setattr(sr.ResumeSyncer, "sync_all", fake_sync_all)
    sr.main(["--source", "remote", "--target", "cv"])
    assert calls == {"use_local": False, "target": "cv"}
