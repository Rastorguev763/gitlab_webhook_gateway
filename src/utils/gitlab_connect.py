from typing import List

from gitlab import Gitlab

from src.core.settings import settings
from src.utils.utils_schemas.gitlab_schemas import Project, ProjectCommit

# from gitlab.v4.objects.projects import Project


class GitlabConnect:
    """
    def example_usage(self):
        project = self.get_projects(1)  # Получаем проект с ID 1
        commits = self.get_commits(project, "main")  # Получаем коммиты для ветки "master"
        return commits
    """

    def __init__(self):
        self.gl = Gitlab(url=settings.URL_GITLAB, private_token=settings.PRIVATE_TOKEN)
        self.gl.auth()

    def get_projects(self, project_id: int) -> Project:
        project = self.gl.projects.get(project_id)
        return project

    def get_commits(self, project: Project, branch_name: str) -> List[ProjectCommit]:
        commits = project.commits.list(ref_name=branch_name)
        return commits


gitlab_connect = GitlabConnect()
