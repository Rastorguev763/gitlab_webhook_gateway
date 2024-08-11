from typing import Optional

from pydantic import BaseModel


class ProjectCommit(BaseModel):

    id: str
    short_id: str
    created_at: str
    parent_ids: str
    title: str
    message: str
    author_name: str
    author_email: str
    authored_date: str
    committer_name: str
    committer_email: str
    committed_date: str
    trailers: Optional[dict]
    extended_trailers: Optional[dict]
    web_url: str


class Namespace(BaseModel):
    id: int
    name: str
    path: str
    kind: str
    full_path: str
    parent_id: Optional[int]
    avatar_url: Optional[str]
    web_url: str


class Links(BaseModel):
    self: str
    issues: str
    merge_requests: str
    repo_branches: str
    labels: str
    events: str
    members: str
    cluster_agents: str


class ContainerExpirationPolicy(BaseModel):
    cadence: str
    enabled: bool
    keep_n: int
    older_than: str
    name_regex: str
    name_regex_keep: Optional[str]
    next_run_at: str


class Project(BaseModel):
    id: int
    description: Optional[str]
    name: str
    name_with_namespace: str
    path: str
    path_with_namespace: str
    created_at: str
    default_branch: str
    tag_list: list
    topics: list
    ssh_url_to_repo: str
    http_url_to_repo: str
    web_url: str
    readme_url: str
    forks_count: int
    avatar_url: Optional[str]
    star_count: int
    last_activity_at: str
    namespace: Namespace
    container_registry_image_prefix: str
    _links: Links
    packages_enabled: bool
    empty_repo: bool
    archived: bool
    visibility: str
    resolve_outdated_diff_discussions: bool
    container_expiration_policy: ContainerExpirationPolicy
    repository_object_format: str
    issues_enabled: bool
    merge_requests_enabled: bool
    wiki_enabled: bool
    jobs_enabled: bool
    snippets_enabled: bool
    container_registry_enabled: bool
    service_desk_enabled: bool
    service_desk_address: Optional[str]
    can_create_merge_request_in: bool
    issues_access_level: str
    repository_access_level: str
    merge_requests_access_level: str
    forking_access_level: str
    wiki_access_level: str
    builds_access_level: str
    snippets_access_level: str
    pages_access_level: str
    analytics_access_level: str
    container_registry_access_level: str
    security_and_compliance_access_level: str
    releases_access_level: str
    environments_access_level: str
    feature_flags_access_level: str
    infrastructure_access_level: str
    monitor_access_level: str
    model_experiments_access_level: str
    model_registry_access_level: str
    emails_disabled: bool
    emails_enabled: bool
    shared_runners_enabled: bool
    lfs_enabled: bool
    creator_id: int
    import_url: Optional[str]
    import_type: str
    import_status: str
    import_error: Optional[str]
    open_issues_count: int
    description_html: str
    updated_at: str
    ci_default_git_depth: int
    ci_forward_deployment_enabled: bool
    ci_forward_deployment_rollback_allowed: bool
    ci_job_token_scope_enabled: bool
    ci_separated_caches: bool
    ci_allow_fork_pipelines_to_run_in_parent_project: bool
    build_git_strategy: str
    keep_latest_artifact: bool
    restrict_user_defined_variables: bool
    runners_token: str
    runner_token_expiration_interval: Optional[str]
    group_runners_enabled: bool
    auto_cancel_pending_pipelines: str
    build_timeout: int
    auto_devops_enabled: bool
    auto_devops_deploy_strategy: str
    ci_config_path: Optional[str]
    public_jobs: bool
    shared_with_groups: list
    only_allow_merge_if_pipeline_succeeds: bool
    allow_merge_on_skipped_pipeline: Optional[str]
    request_access_enabled: bool
    only_allow_merge_if_all_discussions_are_resolved: bool
    remove_source_branch_after_merge: bool
    printing_merge_request_link_enabled: bool
    merge_method: str
    squash_option: str
    enforce_auth_checks_on_uploads: bool
    suggestion_commit_message: Optional[str]
    merge_commit_template: Optional[str]
    squash_commit_template: Optional[str]
    issue_branch_template: Optional[str]
    warn_about_potentially_unwanted_characters: bool
    autoclose_referenced_issues: bool
    permissions: dict
