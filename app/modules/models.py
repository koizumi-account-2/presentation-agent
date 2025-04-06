
from pydantic import BaseModel, Field
from typing import Annotated
import operator

# ペルソナのデータモデル
class Persona(BaseModel):
    name: str = Field(...,description="ペルソナの名前")
    background: str = Field(...,description="ペルソナの背景")

# ペルソナのリストのデータモデル
class PersonaList(BaseModel):
    personas: list[Persona] = Field(...,description="ペルソナのリスト")

# インタビュー内容を表すデータモデル
class InterviewContent(BaseModel):
    persona: Persona = Field(...,description="インタビュー対象のペルソナ")
    question: str = Field(...,description="インタビューの質問")
    answer: str = Field(...,description="インタビューの回答")

# インタビュー結果のリストのデータモデル
class InterviewResult(BaseModel):
    interview_contents: list[InterviewContent] = Field(default_factory=list,description="インタビューの内容のリスト")

class EvaluationResult(BaseModel):
    is_satisfied: bool = Field(...,description="インタビューの内容がユーザーの要件を満たしているかどうか")
    reason: str = Field(...,description="判断理由")

# プレゼンテーションのコンテンツ
class PresentationContent(BaseModel):
    content_name: str = Field(...,description="プレゼンテーションのコンテンツ名")    
    content_purpose: str = Field(...,description="プレゼンテーションのコンテンツの目的")
    content_detail: str = Field(...,description="プレゼンテーションのコンテンツの詳細")
    content_time: int = Field(...,description="プレゼンテーションのコンテンツの時間")

# プレゼンテーションのデータモデル
class Presentation(BaseModel):
    title: str = Field(...,description="プレゼンテーションのタイトル")
    contents: list[PresentationContent] = Field(default_factory=list,description="プレゼンテーションのコンテンツのリスト")

# AIエージェントのステート
class InterviewState(BaseModel):
    thread_id: str = Field(...,description="リクエストのID")
    user_request: str = Field(...,description="ユーザーのリクエスト")
    common_background: str = Field(...,description="共通の背景")
    persona_list: Annotated[list[Persona], operator.add] = Field(default_factory=list,description="ペルソナのリスト")
    persona_confirmed: bool = Field(default=False,description="ペルソナのユーザによる確認")
    interview_result: Annotated[list[InterviewContent], operator.add]  = Field(default_factory=list,description="実施されたインタビューのリスト")
    iteration: int = Field(default=0,description="ペルソナ生成とインタビューの反復回数")
    is_satisfied: bool = Field(default=False,description="情報が充分かどうか")
    presentation: Presentation = Field(default=None,description="プレゼンテーションのコンテンツ")