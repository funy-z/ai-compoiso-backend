def stream_response(resp):
    for chunk in resp:
        yield chunk.content


async def astream_response(resp):
    async for chunk in resp:
        yield chunk.content
