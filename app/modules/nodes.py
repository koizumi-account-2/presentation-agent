from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from modules.models import Persona,PersonaList,InterviewResult,InterviewContent,EvaluationResult,Presentation,PresentationContent

# ペルソナの生成
class PersonaGenerator:
    def __init__(self,llm:ChatOpenAI, common_background:str,k:int=3):
        self.llm = llm.with_structured_output(PersonaList)
        self.k = k
        self.common_background = common_background
    def run(self,user_request:str) -> PersonaList:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","あなたはユーザインタビュー用の多様なペルソナを作成する専門家です"),
                ("human",f"""
                以下のようなユーザーリクエストに関するインタビュー用に、多様なペルソナを{self.k}個作成してください。
                                  
                ユーザーリクエスト：
                 ```
                {user_request}
                 ```
                各ペルソナには名前と簡単な背景を含めてください。年齢、性別、部門、技術的専門知識において多様性を持たせてください。
                また、各ペルソナには以下の共通の背景を持つ用にして下さい。
                 
                共通の背景：
                ```
                {self.common_background}
                ```
                """)
            ]
        )
        
        
        chain = prompt | self.llm
        result = chain.invoke({"query": user_request})
        return result
    

class InterviewConductor:
    def __init__(self,llm:ChatOpenAI):
        self.llm = llm

    def run(self,personas:list[Persona],user_request:str) -> InterviewResult:

        questions = self._generate_question(personas,user_request)
        print(questions)
        answers = self._generate_answer(personas,questions)
        print(answers)
        interviews = self._create_interviews(personas,questions,answers)
        print(interviews)
        return InterviewResult(
            interview_contents=interviews
        )

    # インタビューの質問の生成
    def _generate_question(self,personas:list[Persona],user_request:str) -> list[str]:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","あなたはユーザ要件に基づいて適切な質問を生成する専門家です。"),
                ("human","以下のようなペルソナに関するユーザーリクエストに基づいて、１つの質問を生成してください。\n"
                 "ユーザーリクエスト：{user_request}\n"
                 "ペルソナ：{persona_name} -- {persona_background}\n"
                 "質問は具体的で、このペルソナの視点から重要な情報を引き出す用に設計してください"
                )
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        question_queries =  [
            {
                "user_request":user_request,
                "persona_name":persona.name,
                "persona_background":persona.background
            }
            for persona in personas
        ]
        return chain.batch(question_queries)
    
    
    
    # インタビューの回答の生成
    def _generate_answer(self,personas:list[Persona],questions:list[str]) -> list[str]:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","あなたはペルソナとして回答しています:{persona_name} -- {persona_background}"),
                ("human","質問:{question}"),
            ]
        )
        chain = prompt | self.llm | StrOutputParser()
        answer_queries = [
            {
                "persona_name":persona.name,
                "persona_background":persona.background,
                "question":question
            }
            for persona,question in zip(personas,questions)
        ]
        return chain.batch(answer_queries)

    def _create_interviews(self,personas:list[Persona],questions:list[str],answers:list[str]) -> list[InterviewContent]:
        return [
            InterviewContent(
                persona=persona,
                question=question,
                answer=answer
            )
            for persona,question,answer in zip(personas,questions,answers)
        ]
    

class InformationEvaluator:
    def __init__(self,llm:ChatOpenAI):
        self.llm = llm.with_structured_output(EvaluationResult)

    def run(self,interview_contents:list[InterviewContent],user_request:str) -> EvaluationResult:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","あなたはプレゼンテーションのレジュメを作成するための情報の十分性を評価する専門家です。"),
                ("human","以下のようなユーザーリクエストとインタビューの結果に基づいて、レジュメを作成するために必要な情報が十分に含まれているかどうかを判断してください。\n"
                 "ユーザーリクエスト：{user_request}\n"
                 "インタビュー内容：{interview_result_str}\n"
                 "判断理由を記述してください。"
                )
            ]
        )
        chain = prompt | self.llm

        return chain.invoke({
            "user_request":user_request,
            "interview_result_str":"\n".join([
                f"ペルソナ：{interview.persona.name} -- {interview.persona.background}\n"
                f"質問：{interview.question}\n"
                f"回答：{interview.answer}\n"
                for interview in interview_contents
            ])
        })
            
class PresentationGenerator:
    def __init__(self,llm:ChatOpenAI):
        self.llm = llm.with_structured_output(Presentation)

    def run(self,interview_contents:list[InterviewContent],user_request:str,time_limit:int=60) -> Presentation:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","あなたはプレゼンテーションの構成を作成する専門家です。"),
                ("human","以下のようなユーザーリクエストと複数のペルソナへのインタビューの結果に基づいて、制限時間以内に終了するような量のプレゼンテーションの構成を作成してください。また、ユーザーの背景も考慮してください。\n"
                 "ユーザーリクエスト：{user_request}\n\n"
                 "インタビュー内容：{interview_result_str}\n\n"
                 "ユーザーの背景：入社3年目のエンジニア\n\n"
                 "制限時間: {time_limit}分\n"
                 "構成は順番に並べてください。\n"
                 "プレゼンテーションの構成はタイトルと複数のコンテンツから構成されます。\n"
                 "各コンテンツはコンテンツ名、コンテンツの目的、コンテンツの詳細とコンテンツにかかる時間から構成されます。"
                )
            ]
        )
        chain = prompt | self.llm
        return chain.invoke({
            "user_request":user_request,
            "interview_result_str":"\n".join([
                f"ペルソナ：{interview.persona.name} -- {interview.persona.background}\n"
                f"質問：{interview.question}\n"
                f"回答：{interview.answer}\n"
                for interview in interview_contents
            ]),
            "time_limit":time_limit
        })