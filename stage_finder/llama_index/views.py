from fastapi import APIRouter, Query

from stage_finder.models import ServerResponse, ResponseTypes

router = APIRouter()


@router.get('/ask_question')
def ask_question(question: str = Query("", description="The question you want to aks")) -> ServerResponse:
    # get answer here
    # response = agent.invoke({"input": question})
    return ServerResponse(response_type=ResponseTypes.ANSWER, message=f"You wrote: `{question}`")
