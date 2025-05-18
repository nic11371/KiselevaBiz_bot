from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters.command import Command
from aiogram.types import ChatMemberUpdated
from utils.db import update_block_status


router = Router()
router.my_chat_member.filter(F.chat.type == 'private')
router.message.filter(F.chat.type == 'private')


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    update_block_status(event.from_user.id, True)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated):
    update_block_status(event.from_user.id, False)
