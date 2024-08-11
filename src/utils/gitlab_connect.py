from typing import List
from gitlab import Gitlab

from core.settings import settings

from utils.utils_schemas.gitlab_schemas import ProjectCommit, Project

# from gitlab.v4.objects.projects import Project


class GitlabConnect:

    def __init__(self):
        self.gl = Gitlab(url=settings.URL_GITLAB, private_token=settings.PRIVATE_TOKEN)
        self.gl.auth()

    def get_projects(self, project_id: int) -> Project:
        project = self.gl.projects.get(project_id)
        return project

    def get_commits(self, project: Project, branch_name: str) -> List[ProjectCommit]:
        commits = project.commits.list(ref_name=branch_name)
        return commits

    def example_usage(self):
        project = self.get_projects(6)  # Получаем проект с ID 1
        commits = self.get_commits(project, "test_branch")  # Получаем коммиты для ветки "master"
        return commits


gitlab_connect = GitlabConnect()
