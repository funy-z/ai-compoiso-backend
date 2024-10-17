def stream_response(resp):
    for chunk in resp:
        yield chunk.content


async def astream_response(resp):
    async for chunk in resp:
        yield chunk.content

def get_history_config(user_id: str):
    return {"configurable": {"session_id": user_id}}
