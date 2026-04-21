# Тестируем подключение к БД пока без подключения FastAPI

# !!! Запускаем из корня (у меня E:\Python\Calculator) командой python -m scripts.test_db

import asyncio
from app.db.session import AsyncSessionLocal

from app.schemas.user import UserCreate
from app.schemas.event import EventCreate
from app.schemas.participant import ParticipantCreate

from app.services.user import create_user_service
from app.services.event import create_event_service
from app.services.split import create_split_service
from app.services.participant import (
    create_participant_service,
    get_event_participants_service
)

print("******BEGIN*******")

async def test():
    print("*****IN_FUNCTION*****")
    async with AsyncSessionLocal() as session:
        
        user1 = await create_user_service(
            session,
            UserCreate(username="Ruslan")
        )

        user2 = await create_user_service(
            session,
            UserCreate(username="Svetlana")
        )

        event = await create_event_service(
            session,
            EventCreate(
                title="Dinner",
                owner_id=user1.id
                )
        )
        
        p1 = await create_participant_service(
            session,
            ParticipantCreate(
                event_id=event.id,
                user_id=user1.id,
                display_name="Руслан"
            )
        )

        p2 = await create_participant_service(
            session,
            ParticipantCreate(
                event_id=event.id,
                user_id=user2.id,
                display_name="Светлана"
            )
        )

        participants = await get_event_participants_service(
            session,
            event.id
        )

        print("EVENT:", event.title)
        print("PARTICIPANTS:")

        for p in participants:
            print(p.id, p.display_name)
        
        split1 = await create_split_service(...)
        split2 = await create_split_service(...)


print("******END*******")

if __name__ == "__main__":
    asyncio.run(test())
    