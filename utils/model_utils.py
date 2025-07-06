from pydantic import BaseModel, HttpUrl
import mcp

class CreatePRURLArgs(BaseModel):
    github_url:   HttpUrl  # ex) https://github.com/octocat/hello-world
    head_branch:  str      # ex) feature/login-ui
    base_branch:  str | None = "main"     # ex) main
    title:        str
    body:         str 