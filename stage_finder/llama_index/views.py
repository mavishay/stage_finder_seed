import asyncio
import logging

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from stage_finder.llama_index.service import agent
from stage_finder.models import ServerResponse, ResponseTypes, StateChange
from stage_finder.utils import websocket_manager

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get('/ask_question')
def ask_question(question: str = Query("", description="The question you want to aks")) -> ServerResponse:
    # get answer here
    response = agent.query(question)
    return ServerResponse(response_type=ResponseTypes.ANSWER, message=response)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket_manager.connect(websocket)
    logger.info(f"connected")

    try:
        while True:
            data = await websocket.receive_text()
            try:
                logger.info(f"You wrote: {data}")
                await websocket_manager.send_message(
                    ServerResponse(response_type=ResponseTypes.QUESTION, message=data,
                                   change=StateChange(param="loading", value=True)),
                    websocket,
                )
                await asyncio.sleep(0)
                response = agent.query(data)
                await websocket_manager.send_message(
                    ServerResponse(response_type=ResponseTypes.ANSWER, message=response,
                                   change=StateChange(param="loading", value=False)),
                    websocket,
                )
            except Exception as e:
                logger.error(e)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        await websocket_manager.send_message(
            ServerResponse(response_type=ResponseTypes.STATE_CHANGE,
                           change=StateChange(param="connected", value=False)),
            websocket,
        )
