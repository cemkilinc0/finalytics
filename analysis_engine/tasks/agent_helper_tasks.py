app_name = "analysis_engine"

import structlog
from router.celery import app
from openai import OpenAI
from decouple import config

logger = structlog.get_logger(__name__)


@app.task
def openai_call(data: list[dict], prompt: str) -> dict:
    logger.info("Calling OpenAI API", prompt=prompt, data=data)

    openai_api_key = config("OPENAI_API_KEY", default="", cast=str)
    client = OpenAI(api_key=str(openai_api_key))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "user",
                "content": prompt + "\n\n" + str(data),
            }
        ],
        temperature=1,
    )
    analysis = completion.choices[0].message.content
    number_of_tokens = 0
    if completion.usage is not None:
        number_of_tokens = completion.usage.total_tokens
    else:
        logger.warn("Usage returned None.", prompt=prompt, data=data)

    logger.info("Analysis generated", analysis=analysis)
    return {
        "prompt": prompt,
        "data": data,
        "analysis": analysis,
        "usage": number_of_tokens,
        "finish reason": completion.choices[0].finish_reason,
    }
