from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import uuid
import json, os, boto3
from typing import Optional,Any
from langgraph.graph import StateGraph,END
from modules.nodes import PersonaGenerator,InterviewConductor,InformationEvaluator,PresentationGenerator
from modules.models import InterviewState,Persona,Presentation,PersonaList
from langgraph.checkpoint.postgres import PostgresSaver

from modules.config import get_db_url

#checkpointer = PostgresSaver.from_conn_string(get_db_url())
class PresentationAgent:
    def __init__(self, llm:ChatOpenAI,common_background:str,k:int|None=None,checkpointer:PostgresSaver|None=None):
        self.llm = llm
        self.persona_list = []
        self.persona_generator = PersonaGenerator(llm=llm,common_background=common_background,k=k)
        self.interview_conductor = InterviewConductor(llm=llm)
        self.information_evaluator = InformationEvaluator(llm=llm)
        self.presentation_generator = PresentationGenerator(llm=llm)
        self.checkpointer = checkpointer

        # グラフの作成
        self.graph = self._create_graph()
       



    def start(self,user_request:str,persona_list:list[Persona]) -> str:
        print("start")
        thread_id = str(uuid.uuid4())
        self.persona_list = persona_list
        config = {"configurable": {"thread_id":thread_id}}
        initial_state = InterviewState(user_request=user_request,persona_list=persona_list,request_id=thread_id)
        wait_confirm_state = self.graph.invoke(initial_state,config)
        return wait_confirm_state

    def restart(self,thread_id:str,persona_list:list[Persona]) -> Presentation:
        # persona_listが空は許されない
        if len(persona_list) == 0:
            raise ValueError("persona_listが空です")
        print("restart")
        update_state = {
            "persona_confirmed":True,
            "persona_list":persona_list
        }
        final_state = self.graph.invoke(update_state,config = {"configurable": {"thread_id":thread_id}})
        return final_state
    
    def run(self,user_request:str,thread_id:str,persona_list:list[Persona]) -> Presentation:
        print("thread_id",thread_id)
        if thread_id == "" or thread_id == None:
            return self.start(user_request,persona_list)
        else:
            return self.restart(thread_id,persona_list)

    def _create_graph(self) -> StateGraph:
        workflow = StateGraph(InterviewState)
        # エントリーポイント
        # 最初の分岐：persona_list が空かどうかで分岐
        workflow.set_conditional_entry_point(
            lambda state: len(state.persona_list) > 0,
            {
                True: "conduct_interview",
                False: "generate_persona"
            }
        )
        # ノードの追加
        workflow.add_node("generate_persona",self._generate_persona)
        workflow.add_node("conduct_interview",self._conduct_interview)
        workflow.add_node("evaluate_information",self._evaluate_information)
        workflow.add_node("generate_presentation",self._generate_presentation)
        workflow.add_node("user_confirm_persona",self._user_confirm_persona)
        

        

        # エッジの追加
        workflow.add_edge("generate_persona","user_confirm_persona")
        # workflow.add_edge("user_confirm_persona","conduct_interview")
        workflow.add_edge("conduct_interview","evaluate_information")

        # 条件付きエッジの追加
        workflow.add_conditional_edges(
            "evaluate_information",
            lambda state: not state.is_satisfied and state.iteration < 3,
            {
                True:"generate_presentation",
                False:"generate_presentation"
            }
        )
        workflow.add_edge("generate_presentation",END)
        return workflow.compile(checkpointer=self.checkpointer)

    def _user_confirm_persona(self,state: InterviewState) -> dict[str,Any]:
        print("_user_confirm_persona")
        return {}

    def _generate_persona(self,state: InterviewState) -> dict[str,Any]:
        # ペルソナリストが与えられている場合にはそれを使用し、与えられていない場合には新しく生成する
        new_persona_list:PersonaList = self.persona_list if len(self.persona_list) > 0 else self.persona_generator.run(state.user_request)
        print("_generate_persona")
        return {
            "persona_list":new_persona_list.personas,
            "iteration": state.iteration + 1
        }

    def _conduct_interview(self,state: InterviewState) -> dict[str,Any]:
        print("_conduct_interview")
        new_interview_result = self.interview_conductor.run(state.persona_list[-3:],state.user_request)
        return {
            "interview_result":new_interview_result.interview_contents
        }

    def _evaluate_information(self,state: InterviewState) -> dict[str,Any]:
        print("_evaluate_information")
        evaluation_result = self.information_evaluator.run(state.interview_result,state.user_request)
        return {
            "is_satisfied":evaluation_result.is_satisfied,
            "reason":evaluation_result.reason
        }

    def _generate_presentation(self,state: InterviewState) -> dict[str,Any]:
        print("_generate_presentation")
        presentation = self.presentation_generator.run(state.interview_result,state.user_request)
        return {
            "presentation":presentation
        }
    

        
        
    
