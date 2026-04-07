import tomllib
from dataclasses import dataclass
from pathlib import Path


def load_pyproject_data() -> dict[str, str]:
    pyproject_path = Path(__file__).resolve().parents[3] / "pyproject.toml"

    with pyproject_path.open("rb") as file:
        data = tomllib.load(file)

    return data["project"]


@dataclass(frozen=True)
class ProjectMetadata:
    title: str
    description: str
    version: str

    @classmethod
    def load(cls) -> "ProjectMetadata":
        project = load_pyproject_data()

        return cls(
            title="HelpDesk Hub API",
            description=project["description"],
            version=project["version"],
        )


project_metadata = ProjectMetadata.load()
