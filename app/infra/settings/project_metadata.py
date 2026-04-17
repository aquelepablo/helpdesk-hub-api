import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast


def load_pyproject_data() -> dict[str, str]:
    pyproject_path = Path(__file__).resolve().parents[3] / "pyproject.toml"

    with pyproject_path.open("rb") as file:
        data: dict[str, object] = tomllib.load(file)

    raw_project = data["project"]

    if not isinstance(raw_project, Mapping):
        raise ValueError("Missing [project] section in pyproject.toml")

    project = cast(Mapping[str, object], raw_project)

    result: dict[str, str] = {}

    metadata_keys = {"name", "version", "description"}

    for key in metadata_keys:
        value = project.get(key, "")
        if isinstance(value, str):
            result[key] = value

    return result


@dataclass(frozen=True)
class ProjectMetadata:
    title: str
    name: str
    description: str
    version: str

    @classmethod
    def load(cls) -> "ProjectMetadata":
        project = load_pyproject_data()

        return cls(
            title="HelpDesk Hub API",
            name=project["name"],
            description=project["description"],
            version=project["version"],
        )


project_metadata = ProjectMetadata.load()
