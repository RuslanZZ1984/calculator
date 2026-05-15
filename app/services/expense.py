from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import expense as expense_crud
from app.crud import event as event_crud
from app.crud import participant as participant_crud

from app.schemas.expense import ExpenseCreate, ExpenseUpdate 


async def create_expense_service(session: AsyncSession, data: ExpenseCreate): 
    # Проверяем событие 
    event = await event_crud.get_event(session, data.event_id) 
    if not event: 
        raise ValueError("Событие не найдено") 
    
    # Проверяем участника плательщика 
    payer = await participant_crud.get_participant(
        session, 
        data.payer_id
    ) 
    if not payer: 
        raise ValueError("Плательщик не найден") 
    
    # Проверяем принадлежность к событию 
    if payer.event_id != data.event_id: 
        raise ValueError("Плательщик не пренадлежит событию") 
    
    # Создаём расход 
    return await expense_crud.create_expense(session, data) 


async def get_participant_expenses_service(session: AsyncSession, payer_id: int): 
    # можно ещё бизнес логику добавить 
    return await expense_crud.get_expenses_by_user(session, payer_id) 


async def update_expense_service(
    session: AsyncSession, 
    expense_id: int, 
    data: ExpenseUpdate 
): # и сюда 
    return await expense_crud.update_expense(session, expense_id, data) 


async def delete_expense_service(session: AsyncSession, expense_id: int): 
    return await expense_crud.delete_expense(session, expense_id)




# from sqlalchemy.ext.asyncio import AsyncSession

# from app.crud import expense as expense_crud
# from app.crud import event as event_crud
# from app.crud import participant as participant_crud

# from app.schemas.expense import ExpenseCreate, ExpenseUpdate
# from app.schemas.split import SplitCreate

# from app.services.split import create_split_service


# async def create_expense_service(
#     session: AsyncSession,
#     data: ExpenseCreate
# ):
#     # Проверяем событие
#     event = await event_crud.get_event(session, data.event_id)

#     if not event:
#         raise ValueError("Событие не найдено")

#     # Проверяем плательщика
#     payer = await participant_crud.get_participant(
#         session,
#         data.payer_id
#     )

#     if not payer:
#         raise ValueError("Плательщик не найден")

#     # Проверяем принадлежность событию
#     if payer.event_id != data.event_id:
#         raise ValueError("Плательщик не принадлежит событию")

#     # 1. Создаём expense
#     expense = await expense_crud.create_expense(
#         session,
#         data
#     )

#     # 2. Получаем участников события
#     participants = await participant_crud.get_event_participants(
#         session,
#         data.event_id
#     )

#     # 3. Делим сумму
#     split_amount = round(
#         expense.amount / len(participants),
#         2
#     )

#     # 4. Создаём splits
#     for participant in participants:

#         split_data = SplitCreate(
#             expense_id=expense.id,
#             participant_id=participant.id,
#             amount=split_amount
#         )

#         await create_split_service(
#             session,
#             split_data
#         )

#     return expense


# async def get_participant_expenses_service(
#     session: AsyncSession,
#     payer_id: int
# ):
#     return await expense_crud.get_expenses_by_user(
#         session,
#         payer_id
#     )


# async def update_expense_service(
#     session: AsyncSession,
#     expense_id: int,
#     data: ExpenseUpdate
# ):
#     return await expense_crud.update_expense(
#         session,
#         expense_id,
#         data
#     )


# async def delete_expense_service(
#     session: AsyncSession,
#     expense_id: int
# ):
#     return await expense_crud.delete_expense(
#         session,
#         expense_id
#     )