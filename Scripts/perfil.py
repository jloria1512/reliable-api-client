import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

Skill = Literal["Python", "SQL", "Git", "Docker", "CI/CD"]

class Profile(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    experience: int = Field(ge=0, le=50)
    skills: list[Skill] = Field(max_length=5)
    rol: str
    active: bool

def create_profile(
    name: str, experience: int, skills: list[Skill] | None = None
) -> Profile:

    normalized_skills: list[Skill] = [] if skills is None else skills
    # Create a profile dictionary
    profile = Profile(
        name=name,
        experience=experience,
        skills=normalized_skills,
        rol="AI Automation Engineer",
        active=True,
    )
    return profile

def profile_to_json(profile: Profile) -> str:
    return json.dumps(profile.model_dump(), indent=2, ensure_ascii=False)

# Main execution block
if __name__ == "__main__":
   
    input_name = input("Write your name: ")
    input_skills: list[Skill] = ["Python", "SQL", "Git", "Docker", "CI/CD"]
    while True:
        try:
           
            input_experience = int(input("Write your experience: "))

            profile = create_profile(
                name=input_name, experience=input_experience, skills=input_skills
            )

            json_result = profile_to_json(profile)
            print(json_result)
            break
        except ValidationError as e:
            print("Validation error:")
            for error in e.errors():
                print(f"Field: {error['loc'][0]}")
                print(f"Error type: {error['type']}")
                if error['type'] == "greater_than_equal":
                    print("The value must be greather than 1")
                elif error['type'] == "less_than_equal":
                    print("The value must be less than 51")

        except ValueError:
            print("Experience must be a number")
