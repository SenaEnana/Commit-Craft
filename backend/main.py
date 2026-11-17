import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from date_utils import parse_relative_date
from git_utils import get_repo_status, execute_external_commit

app = FastAPI(title="Commit Craft API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommitRequest(BaseModel):
    repo_path: str
    commit_type: str
    scope: str = ""
    is_breaking: bool = False
    message: str
    body: str = ""
    date_offset: str = ""
    files: list[str] = ["all"]
    push: bool = False

@app.get("/api/status")
def check_status(repo_path: str):
    try:
        files = get_repo_status(repo_path)
        return {"repo_path": repo_path, "changes": files}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/commit")
def create_commit(req: CommitRequest):
    try:
        scope_str = f"({req.scope})" if req.scope else ""
        breaking_mark = "!" if req.is_breaking else ""
        header = f"{req.commit_type}{scope_str}{breaking_mark}: {req.message}"
        full_payload = f"{header}\n\n{req.body}" if req.body else header

        # 2. Handle Custom/Relative Date Environment
        commit_env = os.environ.copy()
        if req.date_offset:
            dt = parse_relative_date(req.date_offset)
            formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
            commit_env["GIT_AUTHOR_DATE"] = formatted_date
            commit_env["GIT_COMMITTER_DATE"] = formatted_date

        # 3. Execute Git Operations on Target Repo
        execute_external_commit(
            repo_path=req.repo_path,
            files=req.files,
            full_payload=full_payload,
            commit_env=commit_env,
            push=req.push
        )
        return {"status": "success", "commit_message": header}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))