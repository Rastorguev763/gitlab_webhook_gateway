from fastapi import APIRouter, Depends, HTTPException, status

from src.core.logger import logger
from src.exceptions.base_exceptions import ObjectNotFound
from src.schemas.merge_request_schemas import WebhookPayload
from src.service.create_message_service import CreateMessageService, get_create_message_service

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Получние вэбхука от Gitlab, расшифровка его и отправка сообщения в Телеграм",
    response_description="Successful Response",
    response_model=None,
)
async def receive_webhook(
    payload: WebhookPayload,
    service: CreateMessageService = Depends(get_create_message_service),
):
    try:
        match payload.event_type:
            case "merge_request":
                responce = await service.create_message_merge_request(data=payload)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error create message merge request: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

    return {"status": responce}
