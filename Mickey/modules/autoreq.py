from pyrogram.types import Message, ChatJoinRequest
from pyrogram import filters
from Abg.chat_status import adminsOnly
from Abg.helpers import ikb
from Mickey import MickeyBot
from pyrogram.errors import UserAlreadyParticipant, UserIsBlocked, PeerIdInvalid





@MickeyBot.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve_join_chat(c, m):
    try:
        await c.send_message(
            m.from_user.id,
            f"<b>ʏᴏᴜ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛᴏ Jᴏɪɴ {m.chat.title}</b>\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ, ᴀᴅᴍɪɴs ᴏғ {m.chat.title} ᴡɪʟʟ ᴀᴄᴄᴇᴘᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴠᴇʀʏ sᴏᴏɴ!",
        )
    except (UserIsBlocked, PeerIdInvalid):
        pass
    await c.send_message(
        m.chat.id,
        text=f"#ᴊᴏɪɴ_ʀᴇǫᴜᴇsᴛ\nᴜsᴇʀ <b>:</b> {m.from_user.mention}\nɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ғᴏᴜɴᴅ",
        reply_markup=ikb(
            [
                [
                    ("ᴄᴏɴғɪʀᴍ ✅", f"approve_{m.from_user.id}"),
                    ("ᴄᴀɴᴄᴇʟ ❌", f"declined_{m.from_user.id}"),
                ]
            ],
        ),
    )
    return


@MickeyBot.on_callback_query(filters.regex(r"^approve"))
@adminsOnly("can_invite_users")
async def approve_chat(c, q):
    i, user = q.data.split("_")
    try:
        user_id = int(user)  # Convert user ID to integer
        new_member = await c.get_users(user_id)  # Fetch details of the new member
        mention = new_member.mention(style="html")  # Get mention format of the user ID

        await q.message.edit(f"#ɴᴇᴡ_ᴊᴏɪɴ\n✨ {mention} join request has been accepted by || {q.from_user.mention} ||")
        await c.approve_chat_join_request(q.message.chat.id, user_id)
    except UserAlreadyParticipant:
        await q.message.edit("User is already in the group.")
    except Exception as err:
        await q.message.edit(str(err))


@MickeyBot.on_callback_query(filters.regex(r"^declined"))
@adminsOnly("can_invite_users")
async def decline_chat(c, q):
    i, user = q.data.split("_")
    try:
        await q.message.edit(f"#ᴅᴇᴄʟɪɴᴇᴅ\n💔ᴜsᴇʀ Jᴏɪɴ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ ʙʏ ||{q.from_user.mention}||")
        await c.decline_chat_join_request(q.message.chat.id, user)
    except UserAlreadyParticipant:
        await q.message.edit("ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ɢʀᴏᴜᴘ !.")
    except Exception as err:
        await q.message.edit(err)
 
