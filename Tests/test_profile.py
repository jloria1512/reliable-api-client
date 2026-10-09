from typing import cast

import pytest
from pydantic import ValidationError

from Scripts.perfil import Profile, Skill, create_profile, profile_to_json


def test_create_profile():
    profile = create_profile(
        name="John Doe", experience=10, skills=["Python", "SQL", "Git", "Docker", "CI/CD"]
    )
    assert profile.name == "John Doe"
    assert profile.experience == 10
    assert profile.skills == ["Python", "SQL", "Git", "Docker", "CI/CD"]
    assert profile.rol == "AI Automation Engineer"
    assert profile.active == True

def test_create_profile_boundary_values():
    profile_min = create_profile(name="Junior", experience=0)
    profile_max = create_profile(name="Senior", experience=50)
    assert profile_min.experience == 0
    assert profile_max.experience == 50

def test_create_profile_invalid_experience():
    with pytest.raises(ValidationError):
        create_profile(name="John Doe", experience=-1)
    with pytest.raises(ValidationError):
        create_profile(name="John Doe", experience=51)

def test_create_profile_empty_skills():
    profile = create_profile(name="John Doe", experience=10, skills=[])
    assert profile.skills == []

def test_create_profile_invalid_skills():
    with pytest.raises(ValidationError) as exc_info:
        create_profile(
            name="John Doe",
            experience=10,
            skills=cast(list[Skill], ["Python", "SQL", "Git", "Docker", "Java"]),
        )
    errors = exc_info.value.errors()
    print(errors)
    assert errors[0]["loc"] == ("skills", 4)
    assert errors[0]["input"] == "Java"

def test_create_profile_invalid_name():
    with pytest.raises(ValidationError):
        create_profile(name="", experience=10, skills=["Python", "SQL", "Git", "Docker", "CI/CD"])